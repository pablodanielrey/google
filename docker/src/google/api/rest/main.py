import logging
logging.getLogger().setLevel(logging.INFO)
import sys
from flask import Flask, abort, make_response, jsonify, url_for, request, json
from users.model import UsersModel
from flask_jsontools import jsonapi

from rest_utils import register_encoder

app = Flask(__name__)
register_encoder(app)

@app.route('/users/api/v1.0/usuarios/', methods=['GET', 'POST'], defaults={'usuario':None})
@app.route('/users/api/v1.0/usuarios/<usuario>', methods=['GET', 'POST'])
@jsonapi
def usuarios(usuario):
    dni = request.args.get('d',None)
    mostrarClave = request.args.get('c',False,bool)

    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    return UsersModel.usuarios(usuario=usuario, dni=dni, c=mostrarClave, offset=offset, limit=limit)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

def main():
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == '__main__':
    main()
