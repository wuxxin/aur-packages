# Oh-My-Pi (`omp`) Provider Integration Research & Plan

## Overview
This document details the research findings for integrating **oh-my-pi (`omp`)** (https://github.com/can1357/oh-my-pi) as an executing CLI provider harness in `amux`.

`oh-my-pi` is an AI coding agent CLI (invoked via the binary `omp`). In `amux`, providers allow spawning interactive terminal sessions (via tmux / herdr) and headless sessions for background agent tasks.

---

## Codebase Architecture & Provider Integration Surface

Adding a new provider `oh-my-pi` / `omp` to `amux` requires modifications across several components in `crates/amux-core` and `crates/amux-server`:

### 1. `amux-core`: Domain Types & Fleet Management
- **`crates/amux-core/src/provider.rs`**:
  - `ProviderId`: Defines open provider identity.
  - Document `omp` / `oh-my-pi` as a recognized provider string.
- **`crates/amux-core/src/provider_fleet.rs`**:
  - `ProviderFleetState`: Tracks provider health/availability in the fleet.
  - Ensure provider ID `omp` can be registered or handled in fleet tests if applicable.

### 2. `amux-server`: Provider Adapter & Registry
- **`crates/amux-server/src/provider/static_providers.rs`**:
  - Implement `OmpAdapter` (or `OhMyPiAdapter`) implementing `ProviderAdapter`.
  - `id()` -> `ProviderId::new("omp")`
  - `capabilities()` -> `ProviderCapabilities { hot_model_switch: false, reports_usage: false, structured_events: false, hooks: false }`
  - `usage()` -> `ProviderUsage::unknown(self.id())`
  - `models()` -> Empty or list models if `omp` supports enumeration.
  - `build_command(prompt_mode)` -> `vec!["omp".into()]` (Interactive) or `vec!["omp".into(), "exec".into()]` / non-interactive flags.
- **`crates/amux-server/src/provider/mod.rs`**:
  - Register `OmpAdapter` in `default_registry()`.
  - Add `omp` resolution alias if needed (e.g., `oh-my-pi` -> `omp`).
  - Add conformance tests `conformance_omp()`.

### 3. `amux-server`: Session Launcher & Verbs
- **`crates/amux-server/src/api/session_verbs.rs`**:
  - `launch_base_binary(provider)`: Return `"omp"` for provider `"omp"` (or `"oh-my-pi"`).
  - `default_model_for_provider(provider)`: Define default model for `omp` (e.g. `"auto"` or `""`).
  - `provider_label(provider)`: Return `"Oh-My-Pi"`.
  - `session_verbs.rs` launch arm (`let cmd = match provider.as_str() ...`):
    - Add `"omp" | "oh-my-pi"` arm building the launch command string for `omp` with flags and options.
- **`crates/amux-server/src/invariants/checks.rs`**:
  - Ensure invariant checks for launch binary matching provider adapter pass.

### 4. `amux-server`: API Routes & Validation
- **`crates/amux-server/src/api/workers.rs`** / **`crates/amux-server/src/api/lookup.rs`**:
  - Handle worker creation and model lookups when `provider == "omp"`.

---

## Files to be Edited Summary

1. `crates/amux-core/src/provider.rs`
2. `crates/amux-server/src/provider/static_providers.rs`
3. `crates/amux-server/src/provider/mod.rs`
4. `crates/amux-server/src/api/session_verbs.rs`

---

## Verification & Testing Plan
1. Edit source files in `src/amux/` using `makepkg -e` (or directly in scratch for testing).
2. Download an `omp` binary release from `can1357/oh-my-pi`.
3. Test `omp` execution and non-install testing on `amux-server` and `amux-rs`.
4. Generate clean patch file and update `amux-git` PKGBUILD.
5. Rebuild package and verify final build.
