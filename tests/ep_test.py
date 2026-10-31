EP = {'num': 99, 'title': 'Test', 'short': 'Scene test', 'scenes': [
 {'type': 'terminal', 'beats': [
   {'cmd': 'git status', 'out': ['fatal: not a git repository (or any of the parent directories): .git'], 'err': True, 'cap': 'Run *git status* in a normal folder and Git complains.'},
   {'cmd': 'git init', 'out': ['Initialized empty Git repository in /home/shivam/my-project/.git/'], 'ok': True, 'cap': 'Now *git init* creates the repo.'},
   {'cmd': 'git commit -am "fix login bug"', 'out': ['[main a1b2c3d] fix login bug', ' 1 file changed, 2 insertions(+)'], 'hl': ['-am'], 'note': '-a stages tracked files', 'cap': 'The *-am* flag adds and commits in one go.'}]},
 {'type': 'lanes', 'files': ['index.html'], 'beats': [
   {'cmd': 'touch style.css', 'new': ['style.css'], 'cap': 'New files start as *untracked*.'},
   {'cmd': 'git add .', 'add': '.', 'cap': '*git add* puts them in the box.'},
   {'cmd': 'git commit -m "home page"', 'commit': 'home page', 'cap': '*Commit* ships the box.'},
   {'cmd': 'edit index.html', 'modify': ['index.html'], 'cap': 'Edit again and it shows *modified*.'}]},
 {'type': 'code', 'file': 'config.yaml', 'lines': ['replicas: 2', '<<<<<<< HEAD', 'image: app:v1.4', '=======', 'image: app:v1.5', '>>>>>>> feature', 'port: 8080'],
  'beats': [{'cap': 'A *merge conflict* looks like this.', 'hl': [[2, 6]], 'note': 'pick one, delete markers'},
            {'cap': 'Keep what you want.', 'lines': ['replicas: 2', 'image: app:v1.5', 'port: 8080'], 'hl': [[2, 2, [52, 211, 153]]]}]},
 {'type': 'graph', 'title': 'Rebase', 'emoji': '🚂', 'beats': [
   {'ops': [['commit', 'main', 'C1'], ['commit', 'main', 'C2'], ['branch', 'feature', 'main'], ['commit', 'feature', 'F1'], ['commit', 'feature', 'F2'], ['commit', 'main', 'C3']], 'cap': 'Main moved on.'},
   {'ops': [['rebase', 'feature', 'main']], 'cap': 'Rebase replays *F1 F2* on top.'},
   {'ops': [['squash', 'feature', 2, 'S'], ['tag', 'C3', 'v1.0']], 'cap': 'Squash into one.'}]},
]}
