# Strata conversation-cache disk spill — draft plan (parked)

Status: dropped from the build on 2026-11-18; **the `CLEAR_CACHE` sub-function was split back out** the same day as its own patch (`strata-clear-cache.patch`, active in this package — stdin command that drops parked conversations and trims the heap, used by the pre-suspend hook). What remains parked here is the KV spill itself. The old scaffold never persisted KV bytes — it wired flags and logged evictions; upstream supersedes its memory half (#5697 RAM release on eviction, segment/checkpoint park pools with budget accounting).

Goal: when a long parked conversation is evicted from the in-RAM conversation cache under pressure, persist it so the next request touching it does not re-prefill — write once to NVMe, restore as a parked conversation later.

Baseline for the design: Strata v0.2.15 (c775728), `include/strata/core/conversation_cache.hpp` + `src/program/generate.cpp` serve loop. Re-anchor every line reference against the release being packaged; upstream moves weekly.

## What must persist

An evicted entry is a `SavedConversation`: token ids, slot/KV bookkeeping, and the host K/V bytes for its prompt (the expensive part — re-prefill is what we avoid). The model fingerprint + config fingerprint machinery in `conversation_file.hpp` already defines "what saved KV bytes are valid for" (rope, control vectors, per-role model inputs) — reuse it; do not invent a second validity rule.

## Design sketch

1. Spill trigger: inside the eviction walk (`ConversationCache::evict`, today around the `entries_[i].pinned() || guarded_` skip), when `disk_spill_ && ids.size() >= min_tokens`: serialize `{token ids, kv bytes, fingerprints, slot layout}` to `<dir>/conv-<id>.bin`, then evict as upstream does (which now also releases RAM — the two mechanisms compose).
2. Restore: on a new request whose prefix matches a spilled conversation (the same matcher that today finds in-RAM parked prefixes), map the file (mmap, page-in lazily) and re-register it as a parked entry with its budget charged; unspill on first touch. A spilled entry must count 0 against the RAM budget while cold.
3. Interaction with park pools: spilled bytes bypass the segment/checkpoint pools entirely (they are disk-resident); restore may refuel them from the restored KV. Budget accounting (`set_pool`, `pool_`) needs a "cold" state so the filler does not race the unspill.
4. Eviction policy stays upstream's (oldest unpinned first, pools given back first) — spill is an outcome of eviction, not a new policy.
5. Flags: add `--disk-spill`, `--disk-spill-dir` (default under `$XDG_CACHE_HOME`/strata), `--disk-spill-min-tokens`; nothing user-visible beyond that — the serve-side `CLEAR_CACHE` command is already its own patch (`strata-clear-cache.patch`).
6. Files: 2–3 hunks in `conversation_cache.hpp/.cpp` (spill/restore + cold state), ~4 in `generate.cpp` (flags, wiring at the constructor site, restore hook in the request path). Expect a new `src/core/conversation_spill.cpp`; keep it out of upstream headers where possible so future rebases touch one file.

## Risks

- Upstream velocity: 950+ commits in five days on this repo; treat the patch as re-based per release, and keep the diff surface minimal (one new TU).
- K/V format stability: upstream checkpoints (`STRATA_CKPT_POOL_READY`) already serialize KV host state — check whether a checkpoint file plus "cold park" gets the feature for free before writing our own format; that is the cheapest real implementation.
- Disk space: 70–120 GB models, long conversations are hundreds of MB of KV each; cap with a spill-dir budget (LRU over files), default off like today.

## Verification when implemented

Build via this PKGBUILD (`makepkg`), then serve on gfx1100: run a >min-token conversation past eviction (watch the "spilled" line), restart requests at that prefix, assert zero re-prefill tokens in the engine's prompt accounting and bounded RSS. A pytest-style harness exists upstream (`test_*` under repo root) — add the spill case there so it survives rebases.

## Next step

Re-open when an upstream release makes checkpoint files loadable cold (watch `STRATA_CKPT_POOL`, `conversation_file.hpp`) or when re-prefill after eviction shows up in real use of the Qwen3.8-Flash-Next serve setup.
