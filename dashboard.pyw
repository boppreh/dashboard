import flask
from modules.upload_clipboard import upload_clipboard
from modules.transfer_clipboard import transfer_clipboard
from modules.workspace import load_workspace, map_problems, get_icon

app = flask.Flask(__name__, static_folder='static', static_url_path='')

workspace = load_workspace()

@app.route('/')
def index():
    projects = sorted(({'name': project.name,
                       'package': project.package,
                       'problems': map_problems(project),
                       #'problems': {},
                       'icon': get_icon(project),
                       'language': project.language,
                       'active': project.active,
                       } for project in workspace),
                      key=lambda p: p['name'])

    return flask.render_template('template.html',
                                 projects=projects)

@app.route('/<project_name>/activate', methods=['POST'])
def activate_project(project_name):
    project = workspace[project_name]
    if project.active:
        project.deactivate()
    else:
        project.activate()
    return ''

@app.route('/upload_clipboard', methods=['POST'])
def upload_service():
    upload_clipboard()
    return ''

@app.route('/transfer_clipboard', methods=['POST'])
def transfer_service():
    transfer_clipboard()
    return ''

app.run(port=80, debug=True, use_reloader=False)
