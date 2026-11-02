SHORT = {
    'series': 'git',
    'tag': 'EP 3',
    'hook': {'text': 'One command makes a *repo*. One deletes ALL history', 'sub': 'Git & GitHub, Ep 3 in 40 seconds',
             'who': ['gajju', 'kaalu']},
    'beats': [
        {'who': 'gajju', 'cmd': 'git status', 'error': True,
         'out': ['fatal: not a git', 'repository (or any of the', 'parent directories): .git'], 'hl': 'not a git',
         'say': 'A plain folder? Git says *not a repository*.'},
        {'who': 'gajju', 'cmd': 'git init', 'arms': 'point', 'voice': True,
         'out': ['Initialized empty Git', 'repository in', '/home/shivam/shop-api/.git/'], 'hl': 'Initialized',
         'say': 'Run git init, and Git creates a hidden *dot git* folder. That IS the repo.'},
        {'who': 'ollie', 'cmd': 'ls .git',
         'out': ['HEAD  branches  config', 'description  hooks  info', 'objects  refs'], 'hl': 'objects',
         'say': '*Objects* store every version. HEAD says which branch you are on.'},
        {'who': 'ollie', 'big': '.git = LOGBOOK', 'sub': 'a hidden logbook in your notebook',
         'say': 'Like a hidden *logbook* that records every change in your notebook.'},
        {'who': 'kaalu', 'cmd': 'rm -rf .git; git status', 'error': True,
         'out': ['fatal: not a git', 'repository'], 'hl': 'fatal',
         'say': 'Delete dot git and *every commit* is gone. No undo!', 'badge': 'Push a backup!'},
        {'who': 'bablu', 'cmd': 'cd ~ && ls -d repos/*/.git',
         'out': ['repos/infra-terraform/.git', 'repos/payment-svc/.git', 'repos/shop-api/.git'], 'hl': 'shop-api',
         'say': 'In DevOps, every service gets its *own repo* and its own Jenkins pipeline.',
         'badge': 'CI/CD!'},
    ],
    'cta': {'who': ['gajju', 'ollie', 'kaalu'],
            'lines': ['Git & GitHub, Ep 3', 'New episodes Mon, Wed & Fri, 4 PM IST']},
    'upload': {
        'title': 'git init vs rm -rf .git: what is a Git repo? #shorts #git',
        'description': (
            'git init turns any folder into a repository by creating the hidden .git folder, where objects, refs and '
            'HEAD keep your whole history. Delete .git and every commit is gone.\n\n'
            'Full episode: "Git Repository & git init Explained Simply | Git & GitHub Ep 3" on the Tech-dev channel.\n'
            'New Git episodes Mon, Wed & Fri at 4 PM IST.\n\n'
            '#shorts #Git #GitHub #DevOps #TechDev'),
        'tags': ['git init', 'git repository', '.git folder', 'what is a git repository', 'git tutorial',
                 'git for beginners', 'shorts', 'git', 'github', 'devops', 'jenkins', 'tech-dev'],
    },
}
