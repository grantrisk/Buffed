from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():

    return '<h1> Welcome to Buffed!</h1>' \
           '<h3> Created by: Cody Jackson</h3>'


if __name__ == '__main__':
    app.run()
