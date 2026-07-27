# TEI Python Backend — Jina Reranker v3 Support Status

> **Date**: 2026-07-26
> **TEI version**: v1.9.3 (latest release), HEAD on main confirmed identical for reranker codepaths
> **Model**: `jinaai/jina-reranker-v3`
>    - Architecture: `JinaForRanking` (custom, inherits from `Qwen3ForCausalLM`)
>    - Model type: `qwen3`
>    - Config: `auto_map: {"AutoModel": "modeling.JinaForRanking"}` (no `AutoModelForSequenceClassification` entry)
>    - Context: 131K tokens, listwise up to 64 docs per pass
>    - License: CC-BY-NC
>    - Special tokens: `<|rerank_token|>` (151671), `<|embed_token|>` (151670)

---

## Problem Overview

TEI auto-detects reranker (cross-encoder) models by checking whether the model architecture string ends with `"Classification"` (e.g., `XLMRobertaForSequenceClassification`). `jina-reranker-v3` uses `JinaForRanking` — suffix is `"Ranking"`, not `"Classification"`. TEI has no `"Ranking"` detection anywhere.

## Detection Points (Three Layers)

### 1. Rust Router — `router/src/lib.rs`

| Line | Code | Status |
|------|------|--------|
| 425 | `arch.ends_with("Classification")` | **Patched** (`jina-reranker-v3.patch` adds `\|\| arch.ends_with("Ranking")`) |
| 117-133 | `id2label`/`label2id` unwrap (jina-reranker-v3 config.json has neither) | **Patched** (patch adds defaults) |

The Rust router correctly identifies `JinaForRanking` as a Classifier/Reranker model type and handles missing `id2label`/`label2id`.

### 2. Python Backend — `backends/python/server/text_embeddings_server/models/__init__.py`

| Line | Context | Detection | Status |
|------|---------|-----------|--------|
| 112 | Inside `model_type == "bert"` block | `endswith("Classification")` | **Patched** (adds `or endswith("Ranking")`) |
| 125 | `model_type == "qwen3"` block (v1.9.3: HPU only; HEAD: HPU or ROCm) | No classification check | **NOT patched** — see below |
| 132 | Default case (fallthrough) | `endswith("Classification")` | **Patched** (adds `or endswith("Ranking")`) |

**Critical**: On v1.9.3, the qwen3 block (line 125) only fires for `device.type == "hpu"`. On ROCm, jina-reranker-v3 falls through to the default case (line 132), so the patch at line 132 catches it. **However**, HEAD/main (commit `ba265a3`) added `or is_rocm()` to the qwen3 block condition. After upgrading past v1.9.3, jina-reranker-v3 would enter the qwen3 block and NEVER reach the default-case patch at line 132. The patch will need updating at that point to add a classification/ranking check inside the qwen3 block.

### 3. Candle Backend (Rust) — `backends/candle/src/models/`

| File | Line | Code | Status |
|------|------|------|--------|
| `flash_qwen3.rs` | 315 | `candle::bail!("classifier model type is not supported for Qwen3")` | **Unchanged** |
| `qwen3.rs` | 412 | `candle::bail!("classifier model type is not supported for Qwen3")` | **Unchanged** |

The candle backend **explicitly rejects** Qwen3-based classifier/reranker models. A comment at `flash_qwen3.rs:321` references `https://huggingface.co/collections/Qwen/qwen3-reranker` suggesting upstream awareness, but no implementation exists.

---

## The Model Loading Problem (Python Backend)

Even after fixing detection, the Python backend's `ClassificationModel` cannot correctly load `JinaForRanking`.

### How ClassificationModel loads models

```python
# classification_model.py:24
model = AutoModelForSequenceClassification.from_pretrained(
    model_path, trust_remote_code=trust_remote
)
```

### Why this fails for JinaForRanking

1. **No `auto_map` entry**: The config only maps `AutoModel` → `modeling.JinaForRanking`, not `AutoModelForSequenceClassification`. Transformers has no mapping from the auto class to the custom class.

2. **Wrong base class**: `JinaForRanking` inherits from `Qwen3ForCausalLM`, not from any sequence classification model. `AutoModelForSequenceClassification` expects models with a classification head and `.logits` output.

3. **Fallback behavior**: With `trust_remote_code=True` and no `auto_map` match, transformers falls back to `Qwen3ForSequenceClassification` (the default for `model_type: "qwen3"`). This loads the **wrong class** — weights won't map correctly (JinaForRanking has custom projector layers), and the forward method is incompatible.

4. **Output format mismatch**: Even if the model loaded correctly, `ClassificationModel.predict()` reads `output.logits`:
   ```python
   # classification_model.py:70-72
   output = self.model(**kwargs, return_dict=True)
   all_scores = output.logits.tolist()
   ```
   But `JinaForRanking.forward()` returns `CausalLMOutputWithScores` with `.scores` (cosine similarity), not `.logits`.

### What JinaForRanking actually expects

Looking at `modeling.py` from the model repo:

- **Prompt format**: Requires chat template with `<|im_start|>system\n...<|im_end|>\n<|im_start|>user\n...<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n...`
- **Special tokens**: Embedding positions are marked by `<|rerank_token|>` (query) and `<|embed_token|>` (documents), not standard CLS/pooling
- **Output**: Returns `CausalLMOutputWithScores` where `.scores` are cosine similarities, not logits
- **Projection**: Has a custom 2-layer MLP projector (hidden_size → hidden_size/2 → 512) applied to extracted embeddings before cosine similarity

---

## What's Needed for Full Support

### Minimum viable path (Python backend)

1. **New model class** (`ranking_model.py` or extend `ClassificationModel`):
   - Use `AutoModel.from_pretrained()` with `trust_remote_code=True` (leverages the existing `auto_map: {"AutoModel": ...}` entry)
   - Call `model.forward(**kwargs)` and read `.scores` instead of `.logits`

2. **Prompt formatting**: Format queries and documents using the model's expected template (system prompt + `<|im_start|>` markers + special embedding tokens). This is non-trivial — the `format_docs_prompts_func()` in `modeling.py` handles batching, special token placement, and context window management.

3. **Detection routing**: In `__init__.py`, route `"Ranking"` architectures to the new model class (or `ClassificationModel` after it's extended). On HEAD, also add the check inside the qwen3 block.

### Alternative path (Rust/candle backend)

Remove the bail in `flash_qwen3.rs` and implement a classification head for Qwen3. The upstream comment referencing the Qwen3-Reranker collection suggests this is the intended direction. Benefit: avoids the Python backend entirely, handles tokenization in Rust.

### Tokenizer considerations

- The model's tokenizer must include the special tokens (`<|rerank_token|>`, `<|embed_token|>`) — these are defined in the model's `tokenizer_config.json` and added at load time
- `padding_side` must be `"left"` for correct batch alignment
- The model has a custom `_truncate_texts()` method that manages query/document length balancing

---

## Upstream Status (HEAD as of 2026-07-26)

- **v1.9.3 is the latest release** — 18 unreleased commits on main since then
- The ROCm commit (`ba265a3`) added `is_rocm()` to the qwen3/mistral blocks in `__init__.py`, meaning our v1.9.3-targeted patch will need adjustment when upgrading
- **Zero `"Ranking"` or `"ForRanking"` references** exist anywhere in upstream code
- **Zero changes** to reranker detection logic in either router or Python backend since v1.9.3
- Candle Qwen3 bail remains unchanged
- No open PRs or issues for jina-reranker-v3 support observed in the commit log

---

## Current Patch Coverage (`tei-rocm/jina-reranker-v3.patch`)

| Layer | File | Change | Sufficient? |
|-------|------|--------|-------------|
| Rust router detection | `router/src/lib.rs` | `"Classification"` → `"Classification" \|\| "Ranking"` | ✅ |
| Rust router id2label | `router/src/lib.rs` | Default `HashMap` for missing `id2label`/`label2id` | ✅ |
| Python detection (bert block) | `models/__init__.py:112` | `"Classification"` → `"Classification" or "Ranking"` | ✅ (not reached by jina-reranker-v3) |
| Python detection (default) | `models/__init__.py:132` | `"Classification"` → `"Classification" or "Ranking"` | ✅ (catches jina-reranker-v3 on v1.9.3 ROCm) |
| Python detection (qwen3 block) | `models/__init__.py:125` | No change | ❌ Needed after upgrade past v1.9.3 |
| Python model loading | `classification_model.py` | No change | ❌ Blocked — see "Model Loading Problem" |
| Python predict/output | `classification_model.py` | No change | ❌ Expects `.logits`, model returns `.scores` |
| Prompt formatting | N/A | Not addressed | ❌ Model needs special token placement |

---

## Conclusion

The detection-layer patch is applied and forward-looking. However, **jina-reranker-v3 will not run** on the Python backend without additional work on model loading, output handling, and prompt formatting. The Rust/candle backend also does not support it (explicitly bails for Qwen3 classifiers). For now, `bge-reranker-v2-m3` remains the only reranker that works end-to-end with TEI on ROCm.
