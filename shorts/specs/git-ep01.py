SHORT = {
    'series': 'git',
    'tag': 'EP 1',
    'hook': {'text': 'What is *Git*? Explained by an elephant', 'sub': 'Git & GitHub, Ep 1 in 30 seconds',
             'who': ['gajju', 'mitthu']},
    'beats': [
        {'who': 'kaalu', 'big': 'final_v2_REAL.docx', 'sub': 'Sound familiar?', 'mood': 'happy', 'arms': 'point',
         'say': 'Saving files as *final_v2_REAL*? Total chaos!'},
        {'who': 'gajju', 'big': 'GIT', 'sub': 'remembers every version',
         'say': 'Git is a *time machine* for your code. Like an elephant, it never forgets.'},
        {'who': 'gajju', 'cmd': 'git log --oneline', 'arms': 'point',
         'out': ['a1b2c3d Fix login bug', '9f8e7d6 Add login page', '4c5d6e7 First commit'], 'hl': 'a1b2c3d',
         'say': 'Every save is a *commit*. You can jump back any time.'},
        {'who': 'ollie', 'big': 'GIT vs GITHUB', 'sub': 'camera vs Instagram',
         'say': '*Git* is the camera. *GitHub* is Instagram, where you share.'},
        {'who': 'bablu', 'cmd': 'git push origin main', 'out': ['To github.com:shivam/app.git', '   9f8e7d6..a1b2c3d  main -> main'],
         'hl': 'main -> main', 'say': 'In DevOps, one *git push* can start Jenkins and deploy your app.',
         'badge': 'CI/CD!'},
    ],
    'cta': {'who': ['gajju', 'ollie', 'kaalu'],
            'lines': ['Git & GitHub, Ep 1', 'New episode every day, 4 PM IST']},
    'upload': {
        'title': 'What is Git? Explained by an Elephant #shorts #git',
        'description': (
            'Git is a time machine for your code: every commit is a save point you can jump back to. '
            'Git is the camera, GitHub is where you share, and one git push can trigger Jenkins CI/CD.\n\n'
            'Full episode: "What is Git? Why every developer needs it | Git & GitHub Ep 1" on the Tech-dev channel.\n'
            'New Git episode every day at 4 PM IST.\n\n'
            '#shorts #Git #GitHub #DevOps #TechDev'),
        'tags': ['git', 'github', 'what is git', 'git vs github', 'git tutorial', 'git for beginners', 'shorts',
                 'git commit', 'git push', 'devops', 'ci cd', 'jenkins', 'tech-dev'],
    },
}
