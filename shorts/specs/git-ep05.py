# Companion Short for Git & GitHub Ep 5 (live Wed 11:30 AM IST): hook from the episode, then "full video is on Tech-dev".
SKIT = {
    'series': 'git',
    'tag': 'EP 5',
    'banner': 'When your commit message says "lgoin"',
    'music': 'none',
    'scenes': [
        {'shot': 'hookcard', 'lines': ['TYPO IN', 'YOUR LAST', ('COMMIT?', 'red')], 'bg': 'navy',
         'small': ['git', '--amend', 'EP 5'], 'stamp': 'FIX IT',
         'mp3': 'media/shorts/git-ep05/hook_shivam.mp3',
         'say': "Typo in your last Git commit? Don't make an *oops* commit... fix it in one line."},
        {'shot': 'wide', 'set': 'desk_night', 'cast': [{'who': 'rohan', 'mood': 'tired', 'pose': 'type'}],
         'say': 'Rohan commits his login fix, then checks the *log*.'},
        {'shot': 'screen', 'cmd': 'git log --oneline -2', 'prompt': '$',
         'out': ['!113c861 Fix lgoin bug', '0fff31a Add payment module'], 'hl': 'lgoin',
         'say': 'Fix *lgoin* bug. And the test file never got added.'},
        {'shot': 'eye', 'who': 'rohan', 'mood': 'worried',
         'say': 'His first idea? A second commit called *oops*.'},
        {'shot': 'wide', 'set': 'desk_night', 'cast': [{'who': 'rohan', 'mood': 'worried', 'pose': 'think', 'x': 380},
                                                       {'who': 'meera', 'mood': 'smug', 'pose': 'mug', 'stand': True, 'x': 790}],
         'laptop_x': 380, 'mug': False,
         'say': 'Meera shakes her head. Just *amend* the last commit.'},
        {'shot': 'screen', 'cmd': 'git commit --amend -m "Fix login bug"', 'prompt': '$',
         'out': ['[main 779fc96] Fix login bug'], 'hl': '779fc96', 'badge': 'Message fixed',
         'say': 'Amend minus m swaps the message. See the *new* ID?'},
        {'shot': 'screen', 'cmd': 'git commit --amend --no-edit', 'prompt': '$',
         'out': ['[main a1b1010] Fix login bug', ' 2 files changed,', ' 2 insertions(+)'], 'hl': '2 files', 'badge': 'Test added',
         'say': 'Add the test file, then amend *no edit*. Both files, one commit.'},
        {'shot': 'face', 'who': 'rohan', 'mood': 'shock', 'fx': ['lines', '!'],
         'say': 'One clean commit. No *oops* anywhere.'},
        {'shot': 'screen', 'cmd': 'git push', 'prompt': '$',
         'out': ['! ! [rejected] main -> main', '!   (non-fast-forward)'], 'badge': 'Amended AFTER push',
         'say': 'But only *before* you push. After a push, Git rejects it.'},
        {'shot': 'card', 'set': 'plain', 'big': '--amend', 'sub': 'only before you push',
         'say': 'Want the full story? The *full video* is on Tech-dev.'},
    ],
    'cta': {'set': 'office'},
    'cover_at': 1.2,
    'upload': {
        'title': 'Typo in your last Git commit? Fix it like this #shorts #git',
        'description': (
            'Typo in your commit message or a forgotten file? git commit --amend fixes your last commit, '
            'but only before you push.\n\n'
            'Full video: "Fix Your Last Git Commit (Typo or Missing File) | Git & GitHub Ep 5" on the Tech-dev channel.\n'
            'New episode every Tuesday, 4 PM IST.\n\n'
            '#shorts #Git #GitHub #DevOps #TechDev'),
        'tags': ['git', 'git commit --amend', 'git amend', 'fix last commit', 'change git commit message', 'git log',
                 'git tutorial', 'git for beginners', 'shorts', 'github', 'devops', 'tech-dev'],
    },
}
