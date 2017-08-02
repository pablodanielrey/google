from flask import Flask, request, send_from_directory
from login.api.http import HttpAuthClient

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/users/web/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
httpAuthClient = HttpAuthClient(
                        os.environ['LOGIN_URL'],
                        os.environ['LOGIN_REST_API_URL'])


@app.route('/favicon.ico', methods=['GET','POST'])
def favicon():
    return send_from_directory(app.static_url_path, 'favicon.ico')

@app.route('/<path:path>')
@httpAuthClient.require_login
def send(path):
    return send_from_directory(app.static_url_path, path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
