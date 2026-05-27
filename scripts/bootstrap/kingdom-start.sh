#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# kingdom-start.sh — bring a fresh session up to a working state.
#
# Handles the post-reboot rituals: start Postgres, load the SSH key into the
# agent (once), and report status. Optionally launches the API.
#
# IMPORTANT: to load the SSH key into YOUR shell, SOURCE this script:
#     source ~/kingdom/scripts/bootstrap/kingdom-start.sh
# Running it as ./kingdom-start.sh still starts Postgres etc., but the ssh key
# only lives for the script's own subshell (agent won't persist to your shell).
#
# Flags:
#   --api      after setup, launch the API in the foreground (Ctrl+C to stop)
#   --no-ssh   skip the ssh-agent/key step
# ─────────────────────────────────────────────────────────────────────────────

KINGDOM_ROOT="${KINGDOM_ROOT:-$HOME/kingdom}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"
_START_API=0
_DO_SSH=1
for _arg in "$@"; do
  case "$_arg" in
    --api) _START_API=1 ;;
    --no-ssh) _DO_SSH=0 ;;
    --help|-h)
      sed -n '3,17p' "${BASH_SOURCE[0]:-$0}" | sed 's/^# \{0,1\}//'
      return 0 2>/dev/null || exit 0 ;;
  esac
done

_klog()  { printf '  \033[0;32m✓\033[0m %s\n' "$1"; }
_kwarn() { printf '  \033[0;33m!\033[0m %s\n' "$1"; }
_kinfo() { printf '\033[1m%s\033[0m\n' "$1"; }

_kinfo "Kingdom session start"

# 1. PostgreSQL — start only if not already accepting connections.
if pg_isready -q 2>/dev/null; then
  _klog "PostgreSQL already running"
else
  sudo service postgresql start >/dev/null 2>&1
  if pg_isready -q 2>/dev/null; then
    _klog "PostgreSQL started"
  else
    _kwarn "PostgreSQL did not come up — check: sudo service postgresql status"
  fi
fi

# 2. SSH agent + key (only meaningful when SOURCED).
if [ "$_DO_SSH" -eq 1 ]; then
  if ssh-add -l 2>/dev/null | grep -q .; then
    _klog "SSH key already loaded in agent"
  else
    if [ -z "${SSH_AUTH_SOCK:-}" ] || ! ssh-add -l >/dev/null 2>&1; then
      eval "$(ssh-agent -s)" >/dev/null
    fi
    if [ -f "$SSH_KEY" ]; then
      ssh-add "$SSH_KEY"   # prompts for passphrase once
      _klog "SSH key loaded ($SSH_KEY)"
    else
      _kwarn "SSH key not found at $SSH_KEY"
    fi
  fi
  case "$0" in
    *bash|*sh|-bash|-sh) : ;;                      # sourced — good
    *) _kwarn "Not sourced — SSH key will NOT persist to your shell. Use: source <script>" ;;
  esac
fi

# 3. Status summary.
_kinfo "Status"
echo "  workspace : $KINGDOM_ROOT"
echo "  postgres  : $(pg_isready -q 2>/dev/null && echo up || echo DOWN)"
echo "  ssh agent : $(ssh-add -l >/dev/null 2>&1 && echo 'key loaded' || echo 'no key')"
echo "  git remote: $(git -C "$KINGDOM_ROOT" remote get-url origin 2>/dev/null || echo none)"

# 4. Optional API launch (foreground).
if [ "$_START_API" -eq 1 ]; then
  _kinfo "Launching API (Ctrl+C to stop)"
  ( cd "$KINGDOM_ROOT" && uv run kingdom-api )
else
  echo
  echo "Next:  cd $KINGDOM_ROOT && uv run kingdom-api      # start API"
  echo "       cd $KINGDOM_ROOT && claude                  # Claude Code session"
fi
