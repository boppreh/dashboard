from requests import get, exceptions

application_template = """<div><b>{}</b>: {}</div>"""
html_template = """
<html>
    <body>{}</body>
</html>
"""

class Application(object):
    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __str__(self):
        try:
            url = 'http://localhost:' + str(self.port)
            value = get(url, timeout=0.001).content
        except (exceptions.ConnectionError, exceptions.Timeout):
            value = '[Offline]'

        return application_template.format(self.name, value)

applications = [Application('Scheduler Notifier', 2340),
                Application('Typist', 2341),
                Application('Watcher Daemon', 2342),
                Application('Network Status', 2343),
                Application('J', 2344),
                Application('Doorman', 2345),
                Application('Calculator', 2346),
               ]

if __name__ == '__main__':
    from background import tray
    import webbrowser
    tray('Dashboard', 'status.png',
         on_click=lambda: webbrowser.open('http://localhost:80'))

    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def index():
        return html_template.format('<br>'.join(map(str, applications)))

    app.run(port=80)
