# Environment — Crostini / ChromeOS facts (true every session)

Machine: ChromeOS, Crostini (Penguin) Linux container. User `techcorp2024`.
Workspace root: `~/kingdom` (= `/home/techcorp2024/kingdom`). Single btrfs volume (~17 GB).

## Gotchas that bite repeatedly (each one has cost a session)

- **Services do NOT auto-start.** After every reboot: `sudo service postgresql start`.
  Use `service`, **never** `systemctl` (Crostini has no systemd).
- **Keep everything on native disk.** `~/kingdom` is btrfs. Never put venvs / git /
  working copies on `/mnt/chromeos/*` — that bridge is 9p/FUSE with no reliable
  inodes/symlinks. Reading a zip from there to extract is fine; working there is not.
- **GUI zip-extraction drops dotfiles.** The ChromeOS Files app hides `.`-files, so a
  GUI extract loses `.mcp.json`, `.env.example`, `.gitignore`. Always extract from the
  terminal with `unzip`.
- **Browser downloads strip the executable bit.** `chmod +x` scripts after saving, or
  run them via `bash script.sh`.
- **`cd` does not persist** across CC's ephemeral bash subprocesses. Each Bash call
  starts fresh — use absolute paths or `cd` within the same compound command. Do not
  rely on a previous call's working directory.
- **`uv` may re-sync to the system Python.** If `uv run` rebuilds `.venv` (e.g. a newer
  Python is detected), that is normal; `uv sync` restores the `kingdom-mcp` console
  script that `.mcp.json` points at.
- **`.env` survives a zip overwrite, but is not shipped.** Extracting a build over
  `~/kingdom` lays down `.env.example`, not `.env`. After a stack change:
  `cp .env.example .env`, then reset `DATABASE_URL` (must be the `+asyncpg` driver).

## First-time rebuild reference
```bash
curl -fsSL https://astral.sh/uv/install.sh | sh      # then re-open terminal
sudo apt install -y postgresql nano zip unzip        # Crostini ships none of these
cd ~/kingdom && ./scripts/bootstrap/bootstrap.sh     # tree + uv sync + .env + git
```
Full procedure: `docs/runbooks/2026-05-24T08-00-00-kingdom-runbook.md`.
