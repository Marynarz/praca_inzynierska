from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    # Thread(target=app.run()).start()
    app.run()