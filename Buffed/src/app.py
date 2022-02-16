from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Welcome to Buffed!</h1><br> Created by Blake Jackson, Tabs Chemelli, Cody Jackson'


if __name__ == '__main__':
    app.run()
