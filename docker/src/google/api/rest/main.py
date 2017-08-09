import logging
logging.getLogger().setLevel(logging.INFO)
import sys
from flask import Flask, abort, make_response, jsonify, url_for, request, json
from google.model import GoogleModel
from flask_jsontools import jsonapi

from rest_utils import register_encoder

app = Flask(__name__)
register_encoder(app)

@app.route('/google/api/v1.0/sincronizar_clave', methods=['GET'])
@jsonapi
def sincronizar():
    return GoogleModel.sincronizar_clave()

@app.route('/google/api/v1.0/sincronizar_usuario', methods=['GET'])
@jsonapi
def sincronizar():
    return GoogleModel.sincronizar_usuario()


@app.route('/google/api/v1.0/sincronizar_usuarios', methods=['GET'])
@jsonapi
def sincronizarUsuarios():
    return GoogleModel.sincronizarUsuarios()

@app.route('/google/api/v1.0/sincronizar_usuarios/<uid>', methods=['PUT','POST'])
@jsonapi
def sincronizarUsuario(uid):
    ''' toma de la base de usuarios los datos y lo sincroniza internamente con la base del sistema de google '''
    assert uid is not None
    return GoogleModel.sincronizarUsuario(uid)



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
