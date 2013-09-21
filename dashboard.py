application_template = """<div>{}</div>"""
html_template = """
<html>
    <body>{}</body>
</html>
"""

class Application(object):
    def __init__(self, name):
        self.name = name

applications = ["Scheduler Notifier", "Typist", "Watcher Daemon",
                "Network Status", "J", "Doorman"]

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    str_apps = (application_template.format(a) for a in applications)
    return html_template.format(''.join(str_apps))

app.run(port=80, debug=True)
