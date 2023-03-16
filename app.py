import json

from flask import Flask, render_template, request
from flask_cors import CORS
from kibana_analyse import get_failed_requests

app = Flask(__name__)
CORS(app,  resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/failed-requests', methods=['GET', 'POST'])
def failed_requests_2():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        form = request.form
        size_, res = get_failed_requests(request=form['request'], size=form['size'])
        return render_template('index.html', res=res, size=size_)


@app.route('/failed-requests-2', methods=['POST'])
def failed_requests():
    form = request.form
    print(form['request'])
    return json.dumps({
        'data': get_failed_requests(request=form['request'], size=form['size'])
    })


if __name__ == '__main__':
    app.run()
