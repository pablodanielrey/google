from google.model.GoogleAuthApi import GAuthApis
import base64
import email
from email.mime.text import MIMEText
from email.parser import Parser

def crearMensaje(api, version, username, file):
    scopes = ['https://www.googleapis.com/auth/gmail.insert','https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']
    service = GAuthApis.getService(version, api, scopes, username)

    headers = Parser().parse(file)
    urlsafe = base64.urlsafe_b64encode(headers.as_string().encode()).decode()
    result = service.users().messages().insert(userId=username,body={'raw': urlsafe}).execute()

def obtenerCorreos(api, version, username):
    scopes = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']
    service = GAuthApis.getService(version, api, scopes, username)

    respuesta = service.users().messages().list(userId=username).execute()
    ids = []
    if 'messages' in respuesta:
        ids.extend([m["id"] for m in respuesta["messages"]])

    while 'nextPageToken' in respuesta:
        page_token = respuesta['nextPageToken']
        respuesta = service.users().messages().list(userId=username, pageToken=page_token).execute()
        if 'messages' in respuesta:
            ids.extend([m["id"] for m in respuesta["messages"]])

    return ids

def obtenerCorreo(api, version, username, mid):
    scopes = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']
    service = GAuthApis.getService(version, api, scopes, username)

    correo  = service.users().messages().get(userId=username, id= mid).execute()

    return correo

if __name__ == '__main__':
    version ='v1'
    api = 'gmail'
    username = '31381082@econo.unlp.edu.ar'

    file = open("google/test/model/mensaje", 'r')
    headers = Parser().parse(file)
    urlsafe = base64.urlsafe_b64encode(headers.as_string().encode()).decode()
    print(urlsafe)
    exit()

    # crearMensaje(api, version, username, file)
    correos = obtenerCorreos(api, version, username)
    id = '15e3d90f09f1d0d4'

    correo = obtenerCorreo(api, version, username, id)

    print(correo)
