application_template = """<div>{} [{}]</div>"""
html_template = """
<html>
    <body>{}</body>
</html>
"""

from requests import get, exceptions

class Application(object):
    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __str__(self):
        try:
            get('http://localhost:' + str(self.port), timeout=0.001)
            status = 'Online'
        except (exceptions.ConnectionError, exceptions.Timeout):
            status = 'Offline'

        return application_template.format(self.name, status)

applications = [Application('Scheduler Notifier', 2340),
                Application('Typist', 2341),
                Application('Watcher Daemon', 2342),
                Application('Network Status', 2343),
                Application('J', 2344),
                Application('Doorman', 2345),
               ]

if __name__ == '__main__':
    print 'a'
    from background import tray
    tray('Dashboard', 'status.png')

    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def index():
        return html_template.format(''.join(map(str, applications)))

    app.run(port=80)
