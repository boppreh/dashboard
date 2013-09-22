application_template = """<div>{}</div>"""
html_template = """
<html>
    <body>{}</body>
</html>
"""

class Application(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return application_template.format(self.name)

applications = map(Application, ["Scheduler Notifier", "Typist",
                                 "Watcher Daemon", "Network Status", "J",
                                 "Doorman"])

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return html_template.format(''.join(map(str, applications)))

app.run(port=80, debug=True)
