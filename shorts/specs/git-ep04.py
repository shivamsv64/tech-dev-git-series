SKIT = {
    'series': 'git',
    'tag': 'EP 4',
    'banner': 'When you commit and forget to git add',
    'scenes': [
        {'shot': 'wide', 'set': 'desk_day',
         'cast': [{'who': 'rohan', 'mood': 'happy', 'pose': 'type'}],
         'say': 'Git has *three* areas, and most beginners only see two.'},
        {'shot': 'screen', 'cmd': 'git status',
         'out': ['Changes not staged for commit:', '        modified:   login.py'],
         'hl': 'not staged', 'say': 'Rohan edits a file. Git sees it, but has not *staged* it.'},
        {'shot': 'screen', 'cmd': 'git commit -m "Fix login"',
         'out': ['!no changes added to commit'], 'badge': 'Nothing was staged',
         'say': 'He commits anyway. Git says, nothing is *added*.'},
        {'shot': 'eye', 'who': 'rohan', 'mood': 'worried',
         'say': 'Rohan is sure he saved it. He did. Just not *staged* it.'},
        {'shot': 'wide', 'set': 'desk_day',
         'cast': [{'who': 'rohan', 'mood': 'worried', 'pose': 'headhold', 'x': 380},
                  {'who': 'tara', 'mood': 'smug', 'pose': 'point', 'stand': True, 'x': 790}],
         'laptop_x': 380,
         'say': 'Tara explains it like packing a box before you ship it.'},
        {'shot': 'screen', 'cmd': 'git add login.py', 'badge': 'Working dir -> staging',
         'say': '*git add* puts the file into the box. That is staging.'},
        {'shot': 'screen', 'cmd': 'git commit -m "Fix login"',
         'out': ['[main 3f2a1b9] Fix login', ' 1 file changed, 1 insertion(+)'], 'hl': '[main 3f2a1b9]',
         'say': 'Now *git commit* ships the box, with a tracking number.'},
        {'shot': 'face', 'who': 'rohan', 'mood': 'happy', 'fx': ['sparkle'],
         'say': 'Edit, add, commit. Rohan finally gets the *flow*.'},
        {'shot': 'card', 'set': 'plain', 'big': 'status > add > commit', 'sub': 'check status before every commit',
         'say': 'Save this. Run *git status* before you commit.'},
    ],
    'cta': {'set': 'office'},
    'cover_at': 1.2,
    'upload': {
        'title': 'When You Commit and Forget to git add #shorts #git',
        'description': (
            'Git has three areas: working directory, staging, commit. git add stages a change, git commit saves '
            'it. Run git status before every commit.\n\n'
            'Full episode: "status, add & commit: the 3 areas of Git" on the Tech-dev channel.\n\n'
            '#shorts #Git #GitHub #DevOps #GitForBeginners #TechDev'),
        'tags': ['git', 'git add', 'git commit', 'git status', 'staging area', 'git for beginners', 'shorts',
                 'github', 'devops', 'tech-dev'],
    },
}
