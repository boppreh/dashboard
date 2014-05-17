import sys
sys.path.append('../workspace')

from collections import defaultdict
from workspace import Workspace
import flask

app = flask.Flask(__name__, static_folder='static', static_url_path='')

workspace = Workspace(r'..\\', r'..\go\src\github.com\boppreh')
workspace.problems

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


@app.route("/")
def index():
    projects = sorted(({'name': project.name,
                       'package': project.package,
                       'problems': map_problems(project),
                       'icon': get_icon(project),
                       'language': project.language,
                       } for project in workspace), key=lambda p: p['name'])

    return flask.render_template('template.html',
                                 projects=projects)

app.run(port=80, debug=True, use_reloader=False)
