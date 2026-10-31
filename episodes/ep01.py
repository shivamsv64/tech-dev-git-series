EP = {
    'num': 1,
    'title': 'What is Git? Why Every Developer Needs It',
    'short': 'What is Git?',
    'scenes': [
        {'type': 'title', 'chapter': 'Intro', 'title': 'What is Git?', 'sub': 'and why *every developer* needs it', 'emoji': '🧠',
         'beats': [{'cap': 'Welcome to Episode 1 of *Git & GitHub: Beginner to Advanced* on Tech-dev.'}]},

        {'type': 'bubble', 'chapter': 'The problem Git solves',
         'beats': [
             {'say': 'Ever seen a folder like this? 😅', 'mood': 'think',
              'items': ['📄 resume.docx', '📄 resume_final.docx', '📄 resume_final_v2.docx', '📄 resume_FINAL_REAL.docx'],
              'cap': 'Ever saved your work as *resume_final*, then *final_v2*, then *FINAL_REAL*?'},
             {'say': 'Now imagine 5 people doing this…', 'mood': 'shock', 'arms': 'shock',
              'items': ['!r 😱 Who changed the address?', '!r 😱 Which file is the latest?'],
              'cap': 'Now imagine five teammates editing the same project. Someone *overwrites* your work, and nobody knows which copy is latest.'},
             {'say': 'Git fixes exactly this. 🎯', 'mood': 'happy',
              'cap': 'That chaos is exactly the problem *Git* was built to solve.'},
         ]},

        {'type': 'cards', 'chapter': 'What is Git', 'title': 'What is Git?', 'emoji': '🤔',
         'beats': [
             {'card': {'emoji': '🕰️', 'title': 'Time machine', 'text': 'Every change saved with *who*, *what* and *when*'},
              'cap': '*Git* is a *version control system*. It records every change to your files, like a time machine for your project.'},
             {'card': {'emoji': '🎮', 'title': 'Checkpoints', 'text': 'Messed up? Jump back to the *last good save*'},
              'cap': 'Think of *checkpoints in a video game*. Lost a fight? You restart from the last save, not from level one.'},
             {'card': {'emoji': '📝', 'title': 'Google Docs history', 'text': 'Like *version history*, but for whole projects'},
              'cap': 'Or Google Docs *version history*, but for entire projects with thousands of files.'},
         ]},

        {'type': 'graph', 'chapter': 'Commits & branches', 'title': 'How Git sees your project', 'emoji': '🌳',
         'beats': [
             {'ops': [['commit', 'main', 'C1']], 'cap': 'Every save point is called a *commit*, a snapshot of your whole project.'},
             {'ops': [['commit', 'main', 'C2'], ['commit', 'main', 'C3']], 'cap': 'Commits link together into a *history* you can travel back through anytime.'},
             {'ops': [['branch', 'feature', 'main'], ['checkout', 'feature'], ['commit', 'feature', 'F1'], ['commit', 'feature', 'F2']],
              'cap': 'Want to try a risky idea? Create a *branch*, your own parallel timeline. The main project stays safe.'},
             {'ops': [['checkout', 'main'], ['merge', 'feature', 'main', 'M']], 'mood': 'happy',
              'cap': 'When it works, *merge* it back. We will master every one of these steps in this series.'},
         ]},

        {'type': 'vs', 'chapter': 'Git vs GitHub', 'title': 'Git vs GitHub', 'emoji': '⚔️',
         'left': {'emoji': '🧰', 'title': 'Git', 'sub': 'The tool'},
         'right': {'emoji': '☁️', 'title': 'GitHub', 'sub': 'The website'},
         'rows': [['Where it lives', '💻 Your computer', '🌐 The cloud'],
                  ['Job', 'Tracks versions', 'Stores & shares repos'],
                  ['Internet?', '✅ Works offline', '📶 Needs internet'],
                  ['Real-life', '📸 Your camera', '🖼️ Instagram']],
         'beats': [
             {'cap': 'People mix these two up all the time. *Git* and *GitHub* are not the same thing.'},
             {'row': 0, 'cap': 'Git is a *tool* installed on your computer. GitHub is a *website* in the cloud.'},
             {'row': 1, 'cap': 'Git tracks the versions. GitHub *stores and shares* those Git projects with your team.'},
             {'row': 2, 'cap': 'That is why Git works *completely offline*, on a flight or in the metro.'},
             {'row': 3, 'cap': 'Simple way to remember: Git is your *camera*, GitHub is *Instagram* where you share the photos.'},
         ]},

        {'type': 'cards', 'chapter': 'Git in real DevOps', 'title': 'Where I use Git every day', 'emoji': '🛠️',
         'beats': [
             {'card': {'emoji': '🚀', 'title': 'CI/CD', 'text': 'Every push triggers a *Jenkins* pipeline'},
              'cap': 'In my DevOps job, every code push to Git *triggers a CI/CD pipeline* that tests and deploys automatically.'},
             {'card': {'emoji': '🏗️', 'title': 'Infra as code', 'text': 'Servers & cloud configs live in *Git*'},
              'cap': 'Even our servers and cloud infrastructure are stored in Git *as code*.'},
             {'card': {'emoji': '🔙', 'title': 'Fast rollbacks', 'text': 'Bad release? Back to the *last good commit*'},
              'cap': 'And when a release breaks production, Git lets us *roll back* to the last good version in minutes.'},
         ]},

        {'type': 'quiz', 'chapter': 'Quick quiz', 'q': 'Which one *needs the internet* to work?', 'opts': ['Git', 'GitHub', 'Both', 'Neither'], 'ans': 1,
         'beats': [{'cap': 'Quick quiz! Pause and think. Which one *needs the internet*?'},
                   {'reveal': True, 'cap': '*GitHub!* Git runs fully on your own machine.'}]},

        {'type': 'recap', 'chapter': 'Recap', 'title': 'Today in 30 seconds', 'emoji': '📝',
         'items': [['Git', 'Version control: tracks every change'], ['Commit', 'A snapshot / save point'],
                   ['Branch', 'A safe parallel timeline'], ['Merge', 'Bring a branch back into main'], ['GitHub', 'Cloud home to share Git repos']],
         'beats': [{'cap': 'Let us recap. These five words are the foundation of *everything* in Git.'}]},

        {'type': 'outro', 'next': 'EP 02 · *Install & Configure Git* on Windows, Mac & Linux',
         'beats': [{'cap': 'If this helped, *subscribe* and hit the bell. Tomorrow we install and configure Git. See you there!'}]},
    ],
    'thumb': {'words': ['WHAT IS', 'GIT?'], 'colors': [[241, 245, 249], [56, 189, 248]], 'emoji': '🧠', 'badge': 'EXPLAINED!', 'mood': 'happy', 'arms': 'point'},
    'upload': {
        'title': 'What is Git? Explained Simply with Real-Life Examples | Git & GitHub Ep 1',
        'hook': 'Still saving files as final_v2_REAL? 😅 Git fixes that. Learn what Git is, how commits & branches work, and the real difference between Git and GitHub, explained with cartoons and real-life examples.',
        'learn': ['What version control is (and why "final_v2" fails)', 'Commits, history, branches & merges in plain English',
                  'Git vs GitHub: camera vs Instagram', 'How Git powers CI/CD and rollbacks in real DevOps teams'],
        'question': 'Be honest: what is the worst "final_final" file name you have ever saved? 😂',
        'hashtags': ['#Git', '#GitHub', '#LearnGit', '#DevOps', '#TechDev'],
        'tags': ['what is git', 'git tutorial for beginners', 'git and github', 'git vs github', 'version control', 'git explained',
                 'learn git', 'git commit', 'git branch', 'devops', 'git basics', 'git course', 'tech-dev'],
    },
}
