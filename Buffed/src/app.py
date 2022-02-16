from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to Buffed! Blake Jackson'


if __name__ == '__main__':
    app.run()
