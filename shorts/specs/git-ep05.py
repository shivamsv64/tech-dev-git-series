SKIT = {
    'series': 'git',
    'tag': 'EP 5',
    'banner': 'When you spot a typo in your commit message',
    'scenes': [
        {'shot': 'wide', 'set': 'desk_day',
         'cast': [{'who': 'rohan', 'mood': 'determined', 'pose': 'type'}],
         'say': 'You can fix your last commit. Before you *push* it.'},
        {'shot': 'screen', 'cmd': 'git log --oneline', 'out': ['a1b2c3d (HEAD -> main) Fixx typo'],
         'hl': 'Fixx', 'say': 'Rohan reads his log and sees *Fixx* with two x.'},
        {'shot': 'eye', 'who': 'rohan', 'mood': 'shock',
         'say': 'It is already committed, and the PR link is *open*.'},
        {'shot': 'wide', 'set': 'desk_day',
         'cast': [{'who': 'rohan', 'mood': 'worried', 'pose': 'facepalm', 'x': 380},
                  {'who': 'tara', 'mood': 'smug', 'pose': 'point', 'stand': True, 'x': 790}],
         'laptop_x': 380,
         'say': 'Tara says, relax. Last commit, not pushed yet? Easy.'},
        {'shot': 'screen', 'cmd': 'git commit --amend -m "Fix typo"', 'badge': 'Rewrites the last commit',
         'say': '*git commit --amend* replaces the last message with a fixed one.'},
        {'shot': 'screen', 'cmd': 'git log --oneline', 'out': ['e4f5a6b (HEAD -> main) Fix typo'],
         'hl': 'Fix typo', 'say': 'Same commit, new message, and a new *hash*.'},
        {'shot': 'face', 'who': 'rohan', 'mood': 'calm', 'fx': ['sparkle'],
         'say': 'Clean history. Nobody ever saw the *typo*.'},
        {'shot': 'face', 'who': 'meera', 'mood': 'worried',
         'say': 'But never amend a commit your team already *pulled*.'},
        {'shot': 'card', 'set': 'plain', 'big': 'amend before push', 'sub': 'never on shared commits',
         'say': 'Save this. Amend *local* commits only.'},
    ],
    'cta': {'set': 'office'},
    'cover_at': 1.2,
    'upload': {
        'title': 'Typo in Your Commit Message? Fix It with --amend #shorts #git',
        'description': (
            'git commit --amend -m "new message" fixes your last commit. It changes the commit hash, so only '
            'do it before you push.\n\n'
            'Full episode: "git log & git commit --amend: fix your last commit" on the Tech-dev channel.\n\n'
            '#shorts #Git #GitHub #DevOps #GitForBeginners #TechDev'),
        'tags': ['git', 'git commit --amend', 'git log', 'fix commit message', 'git for beginners', 'shorts',
                 'github', 'devops', 'tech-dev'],
    },
}
