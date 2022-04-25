from flask import Flask, render_template
from flask_sock import Sock
import json
import time
from backend.scrape import Scraper as sc

app = Flask(
    __name__,
    static_folder='backend/dist/static',
    template_folder='backend/dist'
)
sock = Sock(app)
@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/connection')
def chat(ws):
    while True:
        time.sleep(1)
        message = ws.receive()
        if message is None:
            break

        message = json.loads(message)
        sc.fromWebMaker(message['number'],message['format'],message['all'],ws)

    return 'ok'

if __name__ == '__main__':
    app.run()