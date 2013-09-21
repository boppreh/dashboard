item_template = """<div id="item">{}</div>"""
column_template = """<div id="column">{}</div>"""
html_template = """
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
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
    return html_template.format('<br>'.join(applications))

app.run(port=80, debug=True)
