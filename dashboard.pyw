import sys
sys.path.append('../workspace')


from collections import defaultdict
from workspace import Workspace
import flask

import win32clipboard, win32con
import os
import shutil
import random
import string
import zipfile

def random_name(n=8):
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for i in range(n))

def upload(path):
    print(path)
    scp_fmt = 'scp "{}" lucasboppre@marte.inf.ufsc.br:public_html'
    print(scp_fmt.format(path))
    os.system(scp_fmt.format(path))
    return 'https://inf.ufsc.br/~lucasboppre/' + os.path.basename(path)

def zip_folder(folder_path, zip_path):
    zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(folder_path) + 1
    for base, dirs, files in os.walk(folder_path):
       for f in files:
          fn = os.path.join(base, f)
          zip.write(fn, fn[rootlen:])

def upload_clipboard():
    win32clipboard.OpenClipboard()

    try:
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
            path = 'files/' + random_name() + '.txt'
            with open(path, 'wb') as f:
                f.write(win32clipboard.GetClipboardData(win32con.CF_TEXT))
            new_value = upload(path)
            os.remove(path)

        elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            values_list = []
            for path in win32clipboard.GetClipboardData(win32con.CF_HDROP):
                local_file = 'files/' + os.path.basename(path)

                if os.path.isdir(path):
                    local_file += '.zip'
                    zip_folder(path, local_file)
                else:
                    shutil.copy(path, local_file)

                values_list.append(upload(local_file))
                os.remove(local_file)
            new_value = '\n'.join(values_list)

    finally:
        win32clipboard.CloseClipboard()
    
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
        path = 'files/' + random_name() + '.png'
        from PIL import ImageGrab
        image = ImageGrab.grabclipboard()
        image.save(path,'PNG')
        new_value = upload(path)
        os.remove(path)

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, new_value)
    finally:
        win32clipboard.CloseClipboard()

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

@app.route("/upload_clipboard", methods=['POST'])
def upload_service():
    try:
        upload_clipboard()
        return ""
    except Exception as e:
        return e

app.run(port=80, debug=True, use_reloader=False)
