SHORT = {
    'series': 'git',
    'tag': 'EP 2',
    'hook': {'text': '*Git commit* failed? Fix it in 30 seconds', 'sub': 'Git & GitHub, Ep 2 in 30 seconds',
             'who': ['gajju', 'kaalu']},
    'beats': [
        {'who': 'kaalu', 'cmd': 'git commit -m "First"', 'error': True,
         'out': ['Author identity unknown', '', '*** Please tell me', 'who you are.'], 'hl': 'Author identity unknown',
         'say': 'Skipped setup? Git *refuses* to commit!', 'badge': 'Set your name!'},
        {'who': 'ollie', 'big': 'NAME TAG', 'sub': 'like a sender label on a parcel',
         'say': 'Every commit carries your *name and email*, like a parcel label.'},
        {'who': 'gajju', 'cmd': 'git config --global user.name "Shivam"', 'arms': 'point', 'voice': True,
         'out': [], 'hl': 'user.name',
         'say': 'Set your name and email *once*, and I remember them on every commit.'},
        {'who': 'gajju', 'cmd': 'git config --list',
         'out': ['user.name=Shivam', 'user.email=shivam@example.com', 'init.defaultbranch=main'], 'hl': 'user.email',
         'say': 'Check everything with *git config --list*.'},
        {'who': 'ollie', 'cmd': 'git config --global alias.st status', 'out': [],
         'say': 'Aliases are *speed-dial*: now git st runs git status.'},
        {'who': 'bablu', 'cmd': 'git config user.name "jenkins-bot"', 'out': [], 'hl': 'jenkins-bot',
         'say': 'In CI, our *Jenkins bot* uses its own name, so its commits stand out.',
         'badge': 'CI/CD!'},
    ],
    'cta': {'who': ['gajju', 'ollie', 'kaalu'],
            'lines': ['Git & GitHub, Ep 2', 'New episode every day, 4 PM IST']},
    'upload': {
        'title': 'Git commit failed? Set your name in 30 sec #shorts #git',
        'description': (
            'Git refuses to commit until it knows who you are. Set user.name and user.email once, check them with '
            'git config --list, and save typing with aliases like git st.\n\n'
            'Full episode: "Install & Configure Git Explained Simply | Git & GitHub Ep 2" on the Tech-dev channel.\n'
            'New Git episode every day at 4 PM IST.\n\n'
            '#shorts #Git #GitHub #DevOps #TechDev'),
        'tags': ['git', 'git config', 'install git', 'git setup', 'git user.name', 'git alias', 'git tutorial',
                 'git for beginners', 'shorts', 'devops', 'github', 'tech-dev'],
    },
}
