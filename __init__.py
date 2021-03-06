#! /usr/bin/python3.7

import sys

from flask import Flask, jsonify, render_template, request

from util import run

app = Flask(__name__)
app.secret_key = 'beans'


@app.route('/')
def home():
    return 'version : {}'.format(sys.version)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/run', methods=["POST"])
def run_file():
    print(request.form)
    code = str(request.form['code'])
    filename = str(request.form['filename'])

    stdout, stderr = run.go(code, filename)

    return jsonify(stdout=stdout,
                   stderr=stderr)
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='159.65.162.204')
