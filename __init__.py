#! /usr/bin/python3

from flask import Flask

app = Flask(__name__)
app.secret_key = 'beans'


@app.route('/')
def home():
    return 'Hello!'


if __name__ == '__main__':
    app.debug = True
    app.run()
