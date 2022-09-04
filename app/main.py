import awsgi
from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)


@app.route('/hello')
def index():
    return jsonify(status=200, message='OK')

@app.route('/test')
def index_test():
    return jsonify(status=200, message='TEST OK')


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')