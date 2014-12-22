import sys
sys.path.append('../workspace')

from collections import defaultdict
from workspace import Workspace

def map_problems(project):
    icons = {
        'uncommited changes': 'pencil.png',
        'commits to push': 'plug.png',
        'commits to pull': 'plug.png',
        'using HTTPS to sync': 'globe.png',
        'no CHANGES.txt': 'report.png',
        'no README.txt': 'report.png',
        'commits to publish': 'box.png',
    }

    problems = defaultdict(list)
    for problem in project.problems:
        for description, icon in icons.items():
            if description in problem:
                problems[icon].append(problem)

    return {icon: '\n'.join(problem) for icon, problem in problems.items()}

def get_icon(project):
    icons = defaultdict(lambda: 'question.png', {
        'python': 'python.gif',
        'javascript': 'javascript.gif',
        'go': 'go.ico',
    })

    return icons[project.language.lower()]

def load_workspace():
    workspace = Workspace(r'..\\', r'..\go\src\github.com\boppreh')
    return workspace

