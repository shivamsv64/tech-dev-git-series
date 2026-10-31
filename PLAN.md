# Tech-dev · Git & GitHub: Beginner → Advanced — Playlist plan

Channel: Tech-dev (YouTube UCZAlvuJrNlK6ORtuN5x06ZQ) · Presenter: Shivam Singh Verma (DevOps & SRE, 5 yrs)
Format: 2–5 min animated explainers · mascot **Bit** (original robot) · captions + lofi music + SFX · 1080p30
Schedule: **one episode per day, published 4:00 PM IST**. Ep 1 = Sat 31 Oct 2026, Ep 15 = Sat 14 Nov 2026.
Covers all 18 topics of the reference playlist (Engineering Digest) in 15 tighter episodes, every one with real-life analogies + a real DevOps example.

| Ep | Date (IST 4 PM) | Title | Real-life analogy | Real DevOps example | Key commands / scenes |
|---|---|---|---|---|---|
| 1 | Sat 31 Oct | What is Git? Why every developer needs it | resume_final_v2_REAL files; game checkpoints; Google Docs history; Git = camera, GitHub = Instagram | push → Jenkins CI/CD; infra as code; rollbacks | bubble, cards, graph, vs, quiz |
| 2 | Sun 1 Nov | Install & Configure Git (Win/Mac/Linux) + aliases | Name tag on every parcel you send (user.name / email); speed-dial = aliases | Wrong email on commits breaks audit trails & GitHub contribution graph; CI bots have their own identity | `git --version`, winget/brew/apt install, `git config --global user.name/email`, `init.defaultBranch main`, `core.editor`, `git config --list`, `git config --global alias.st status` |
| 3 | Mon 2 Nov | What is a Git Repository? `git init` & the .git folder | A notebook with a hidden CCTV logbook (.git) that records every page change; delete the logbook = history gone | Every microservice / Terraform module lives in its own repo | `mkdir`, `git status` (fatal: not a git repository), `git init`, `ls -la`, `ls .git`, `rm -rf .git` warning |
| 4 | Tue 3 Nov | status, add & commit — the 3 areas of Git | Sending a courier: items on table (working dir) → packed box (staging) → shipped with tracking no. (commit) | Small focused commits = easy code review & safe deploys | lanes scene: new → `git add` → `git commit -m`; `git add .`; `git rm --cached`; `git commit -am` |
| 5 | Wed 4 Nov | git log & git commit --amend — fix your last commit | Editing your last WhatsApp message vs. a sent letter | Fixing a typo'd commit message before pushing; never amend pushed shared commits | `git log`, `--oneline`, `--graph`, `git show`, `git commit --amend -m`, `--amend --no-edit` |
| 6 | Thu 5 Nov | .gitignore — never commit secrets again | Packing for a trip: don't pack your house keys (.env) or the whole kitchen (node_modules) | Real incident type: AWS keys pushed to a public repo get abused within minutes → rotate keys | code scene for .gitignore patterns (`*.log`, `node_modules/`, `.env`, `!keep.log`), `git status` before/after, `git rm --cached .env` |
| 7 | Fri 6 Nov | Branches: create, switch, rename, delete (+ checkout) | Parallel drafts of a speech; road lanes | feature/*, hotfix/* branches; protected main | graph scene; `git branch`, `git switch -c`, `git checkout`, `git branch -m`, `git branch -d/-D` |
| 8 | Sat 7 Nov | Merging branches & fixing merge conflicts | Two people editing the same sentence of a shared doc | Conflicts in config/YAML files during release merges | graph: fast-forward vs merge commit; code scene with conflict markers; resolve → add → commit |
| 9 | Sun 8 Nov | git restore — undo uncommitted changes | Ctrl+Z before you save; un-packing an item from the box | Accidentally edited a prod config file locally — restore it | `git restore file`, `git restore --staged file`, `git restore .`, `git diff` |
| 10 | Mon 9 Nov | git reset — soft vs mixed vs hard | Rewinding a video: soft keeps the edit timeline, hard shreds the footage | Squashing local WIP commits before a PR; danger of --hard | graph reset op + lanes; `git reset --soft HEAD~1`, `--mixed`, `--hard`, ⚠️ reflog teaser |
| 11 | Tue 10 Nov | git revert — the safe undo for shared history | Bank reversal entry instead of tearing a page out of the ledger | Rolling back a bad production release without rewriting history | graph: revert commit C3'; `git revert <hash>`, revert vs reset vs table |
| 12 | Wed 11 Nov | git stash — save work-in-progress | Guests arrive: put the half-cooked curry in the fridge, serve them, then continue | Urgent prod hotfix while mid-feature | `git stash`, `stash -m`, `stash list`, `stash pop`, `stash apply`, `stash drop` |
| 13 | Thu 12 Nov | What is GitHub? Remotes, clone & push | Google Drive for code; "origin" = home address | Jenkins/GitHub Actions pull from the remote on every push | `git remote add origin`, `git push -u origin main`, `git clone`, `git remote -v` |
| 14 | Fri 13 Nov | git fetch vs git pull (+ pull requests) | Fetch = checking your mailbox; pull = opening the letters and acting on them | PR workflow: review + CI checks before merge to main | graph with origin/main; `git fetch`, `git pull`, `git pull --rebase`, PR flow cards |
| 15 | Sat 14 Nov | git rebase & squash — clean history like a pro (series finale) | Re-coupling your train carriages behind the newest engine | Clean linear history on main; trunk-based dev in CI/CD; reflog to rescue | graph rebase + squash ops; `git rebase main`, `git rebase -i`, golden rule, recap of whole series |

## Production rules
- Every episode: title → hook (bubble) → concept with real-life analogy → hands-on (terminal / lanes / graph) → DevOps example → quiz → recap → outro (16 s end-screen area).
- Captions ≤ 18 words, highlight 1–2 key words with `*word*`. Target 2:30–4:30 total.
- Thumbnail: 2–3 big words + emoji + badge, mascot pointing. Title format: `<Topic> Explained Simply | Git & GitHub Ep N`.
- Upload: YouTube via Metricool (brand 7777398), public, scheduled 16:00 Asia/Kolkata, category EDUCATION, not made for kids, not AI-realistic content.
