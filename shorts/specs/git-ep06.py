SKIT = {
    'series': 'git',
    'tag': 'EP 6',
    'banner': 'When you push your .env to a public repo',
    'scenes': [
        {'shot': 'wide', 'set': 'desk_night',
         'cast': [{'who': 'rohan', 'mood': 'tired', 'pose': 'type'}],
         'say': 'Never commit your *.env* file. Bots find leaked keys fast.'},
        {'shot': 'eye', 'who': 'rohan', 'mood': 'shock',
         'say': 'Rohan just noticed .env in a public repo. Cloud keys inside.'},
        {'shot': 'phone', 'time': '2:14',
         'alert': {'title': 'ALERT', 'lines': ['Unusual cloud usage', 'on your access key']},
         'say': 'Minutes later, his phone lights up with a *warning*.'},
        {'shot': 'wide', 'set': 'desk_night',
         'cast': [{'who': 'rohan', 'mood': 'panic', 'pose': 'headhold', 'x': 380, 'fx': ['sweat']},
                  {'who': 'meera', 'mood': 'calm', 'pose': 'point', 'stand': True, 'x': 790}],
         'laptop_x': 380, 'mug': False,
         'say': 'Meera stays calm. Two steps, and the *order* matters.'},
        {'shot': 'screen', 'cmd': 'git rm --cached .env', 'out': ["rm '.env'"], 'hl': "rm '.env'",
         'say': 'First, *git rm --cached* stops tracking it. The file stays local.'},
        {'shot': 'screen', 'cmd': 'echo ".env" >> .gitignore', 'badge': 'So it never comes back',
         'say': 'Then add it to *.gitignore* so it never returns.'},
        {'shot': 'face', 'who': 'rohan', 'mood': 'worried',
         'say': 'But the key is still in the old *history*.'},
        {'shot': 'face', 'who': 'meera', 'mood': 'determined',
         'say': 'So step two is the real fix. *Rotate* the keys.'},
        {'shot': 'card', 'set': 'plain', 'big': 'Leaked = rotate', 'sub': 'ignore .env first, always',
         'say': 'Save this. A leaked key is a dead key. *Rotate* it.'},
    ],
    'cta': {'set': 'office'},
    'cover_at': 1.2,
    'upload': {
        'title': 'When You Push Your .env to a Public Repo #shorts #git',
        'description': (
            'Add .env to .gitignore before your first commit. If it was already pushed: git rm --cached .env, '
            'then rotate every key in it. Deleting the file does not remove it from history.\n\n'
            'Full episode: ".gitignore: never commit secrets again" on the Tech-dev channel.\n\n'
            '#shorts #Git #GitHub #DevOps #Security #TechDev'),
        'tags': ['git', 'gitignore', '.env', 'git rm --cached', 'leaked secrets', 'rotate keys',
                 'git for beginners', 'shorts', 'github', 'devops', 'tech-dev'],
    },
}
