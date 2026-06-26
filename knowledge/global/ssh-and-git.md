# SSH & Git identity (true every session)

- **GitHub account:** `TechCorp25` (personal). Org: `techcorp-DevApps`. Same key for both.
- **Key:** `~/.ssh/id_ed25519` (has a passphrase). One account key, titled
  `claude-kingdom` on GitHub.
- **Greeting check:** `ssh -T git@github.com` → `Hi TechCorp25!`
  - A **username** greeting = an account key that can push to all your repos. ✅
  - A **repo-name** greeting (`Hi org/repo!`) = a deploy key locked to one repo —
    useless for anything else. If you see that, the wrong key is loaded.
- **HTTPS push is dead** (GitHub killed password auth). Always use the SSH remote
  `git@github.com:...`, never `https://github.com/...`.
- **git identity:** `user.name = techcorp2024`, `user.email = techcorp2024@gmail.com`.
  A placeholder email means commits don't link to the account — fix with
  `git commit --amend --reset-author` after correcting config.

## Load the key after a reboot (the agent starts empty)
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519        # prompts for passphrase once
ssh -T git@github.com            # expect: Hi TechCorp25!
```
`kstart` (source `scripts/bootstrap/kingdom-start.sh`) does this for you.

## Repos
- Control plane: `git@github.com:TechCorp25/kingdom.git` (branch `main`).
- Tracked app repos live under `techcorp-DevApps/` and are checked out in
  `projects/<slug>/` (gitignored). Each has its own push discipline — see the per-project
  brief in `knowledge/projects/<slug>.md`.

## Hygiene
- **Push before you duplicate.** Unpushed local commits are how work gets stranded.
- Merge/squash discipline: `knowledge/policies/merge-hygiene.md`.
