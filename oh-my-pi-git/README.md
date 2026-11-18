# oh-my-pi-git

AUR-style private build of [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) (omp), pinned to the latest
upstream git tag plus HEAD. This package **is** the harness running in the mypai omp sandbox; its source checkout
under `src/oh-my-pi/` is the ground truth for every harness-behavior claim made elsewhere in the workspace.

Local changes vs. upstream live here as patches; what upstream changed toward this system per upgrade is recorded
in [CHANGELOG.md](CHANGELOG.md) (privacy-neutral, consumable by other mypai infrastructure).

## Local modifications to upstream omp

| Patch | What it does | Upstream touchpoint |
|---|---|---|
| `use-system-opus-pcre2.patch` | Links the system shared `libopus` and `libpcre2-8` instead of building vendored copies: adds a `LIBOPUS_DYNAMIC=1` env + `opusic-sys-dynamic.patch` crate annotation in `MODULE.bazel`, flips `PCRE2_SYS_STATIC` to `0`, and extends the addon verifier's allow-list (`GLIBC_ADDON_NEEDED`) with `libopus.so.0`/`libpcre2-8.so.0` — upstream added a check that rejects any DT_NEEDED outside glibc, assuming static vendored libs; our shared-lib links are intentional. | `MODULE.bazel`, `bazel/patches/opusic-sys-dynamic.patch` (new file — the one prepare() re-creates; see maintenance note), `scripts/bazel-natives.ts` |
| `tree-sitter-no-strict-aliasing.patch` | `-fno-strict-aliasing` for the tree-sitter 0.25 runtime and every statically linked grammar crate: tree-sitter's `array.h` type-puns `Array(T)*` through `Array(void)*`, which miscompiles under `-O2 -fstrict-aliasing` (e.g. tree-sitter-haskell scanner segfault). Fixed upstream only in tree-sitter 0.26.x; the runtime pinned here is 0.25.10. | `MODULE.bazel` crate annotations |
| `skip-native-embed-for-aur.patch` | Honors `PI_SKIP_NATIVE_EMBED=1` in `compile-binary.ts` so native addons ship as loose `.node` files next to the binary (loader falls back to the executable dir) — required for packageable, inspectable installs. | `packages/coding-agent/scripts/compile-binary.ts` |
| `relative-json-asset-paths.patch` | Makes compiled-binary asset ids relative to the build root (`omp-json-asset:` plugin + legacy virtual module), so the installed binary embeds no absolute checkout path. | `packages/coding-agent/scripts/json-parse-plugin.ts`, `legacy-pi-virtual-module.ts` |

PKGBUILD specifics (not patches): tag-based `pkgver()` via `git describe --long --tags`; JDK-21 pin for Bazel 9;
`USE_BAZEL_VERSION=latest` + `CARGO_BAZEL_REPIN=1 bazel fetch @crates//...` in `prepare()` (crate annotations change
the crate graph); `PI_SKIP_NATIVE_EMBED=1 RELEASE_TARGETS=linux-x64` release build; completion generation from the
built binary; Python wheels (`omp-rpc`, `robomp`) installed into system site-packages.

## Maintenance: updating to a new upstream HEAD

Run from this directory. The full procedure, so it can be repeated mechanically each iteration:

1. **Checksums / fetch:** `updpkgsums` (fetches the git source; patch sums are the only real content).
2. **Diff window for the changelog:** read the installed version's commit from its pkgver (`…g<sha>` suffix). In a
   scratch clone (`../scratch/oh-my-pi-sources`, `git fetch` to update), take
   `git log --oneline <last-sha>..HEAD`. Curate user-facing content from
   `packages/coding-agent/CHANGELOG.md` at HEAD: the `[Unreleased]` section plus every release newer than the
   installed tag — that file is the authoritative, already-curated upstream changelog.
3. **Patch regeneration:** do not hand-fix offsets. On a clean checkout of HEAD, create a snapshot chain on a temp
   branch: for each patch in PKGBUILD `prepare()` order → `patch -p1`, `git add -A`, `git commit`; the regenerated
   patch is `git diff <prev-snap> <new-snap>`. Verify each regenerated patch applies with zero offset/fuzz
   (`patch --dry-run`) and that applying all of them onto clean HEAD yields a tree identical to the chain tip
   (`git write-tree` == chain-tip tree). Replace the old files, `updpkgsums`, `makepkg --printsrcinfo > .SRCINFO`.
4. **Build hygiene:** before any real build run `rm -rf src/oh-my-pi pkg`. makepkg reuses a VCS working copy and its
   reset does not remove untracked files; a patch that *creates* a file (opusic-sys-dynamic.patch) then fails in
   prepare() with "already exists". A probe build (`makepkg --nobuild`) leaves exactly this residue.
5. **Changelog:** append a new dated entry at the top of `CHANGELOG.md` — version range, commit range, curated
   system-relevant changes (breaking first). Keep it privacy-neutral: no hostnames/users; refer to "the mypai
   sandbox", "the LifeOS hooks bridge". Other infrastructure consumes that file.
