# Helper Utilities


## `aurupgrade.sh`

A simple wrapper for upgrading all local AUR packages within the `aur-packages` repository.

```bash
./scripts/aurupgrade.sh
```

It iterates through all subdirectories containing a `PKGBUILD` and executes the build process.

## `run-on-screen.sh`

Allows running GUI applications (like browser tests or IDEs) from a non-interactive shell (e.g. SSH or a systemd service) by "stealing" the current user's `DISPLAY`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS`.

```bash
./scripts/run-on-screen.sh <executable> [args...]
```


## `tiktoken_count.py`

A Python utility for counting tokens in text files or strings using the `tiktoken` library (consistent with OpenAI models).

```bash
python3 scripts/tiktoken_count.py <file_or_string>
```

## `tiktoken_tps_sim.py`

Simulates token-per-second (TPS) throughput for various models to help calibrate timeout settings and performance expectations.
