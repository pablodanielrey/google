from google.model.GoogleAuthApi import GAuthApis
import base64
import email
from email.mime.text import MIMEText
from email.parser import Parser
from apiclient import errors
import os
import re

def crearMensaje(api, version, username, file, labelIds):
    scopes = ['https://www.googleapis.com/auth/gmail.insert','https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']
    service = GAuthApis.getService(version, api, scopes, username)

    headers = Parser().parse(file)
    urlsafe = base64.urlsafe_b64encode(headers.as_string().encode()).decode()
    print(headers)
    print(urlsafe)
    return service.users().messages().insert(userId=username,internalDateSource='dateHeader',body={'raw': urlsafe, 'labelIds': labelIds}).execute()

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

def obtenerLabels(userId):
    scopes = ['https://mail.google.com/',
              'https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.labels',
              'https://www.googleapis.com/auth/gmail.metadata']

    service = GAuthApis.getService('v1', 'gmail', scopes, userId)
    try:
        response = service.users().labels().list(userId=userId).execute()
        labels = response['labels']
        return labels
    except errors.HttpError as err:
        print('An error occurred: %s' % error)

def crearEtiqueta(userId, nombre):
    scopes = ['https://mail.google.com/',
              'https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/gmail.labels']

    service = GAuthApis.getService('v1', 'gmail', scopes, userId)
    try:
        label = service.users().labels().create(userId=userId, body={'name':nombre}).execute()
        return label["id"]
    except errors.HttpError as err:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    version ='v1'
    api = 'gmail'
    username = '31381082@econo.unlp.edu.ar'

    patron = re.compile('\..+')

    maildir = '/home/emanuel/econo/Maildir'

    (base, dirs, files) = next(os.walk(maildir))

    omitir = ['.Sent', '.Enviados', '.Borradores', '.Draft','.Trash']
    '''
    labelsGoogle = obtenerLabels(username)
    etiquetasGoogle = [l["name"] for l in labelsGoogle]
    etiquetasNuevas = []

    for d in dirs:
        if patron.match(d) and d not in omitir:
            l = d.replace(".","/")[1:]
            if l not in etiquetasGoogle:
                id = crearEtiqueta(username, l)
                etiquetasNuevas.append({'id':id, 'dir':d})
                print(d)

    print(etiquetasNuevas)
    '''

    for (base, dirs, files) in os.walk(maildir):
        if base[-4:] in ['/cur','/new']:
            print(base)


    exit()



    with open("google/test/model/mensaje", 'r') as file:

        labelIds = ['INBOX']
        print(crearMensaje(api, version, username, file, labelIds))

        '''
        id = '15e3d90f09f1d0d4'
        correos = obtenerCorreos(api, version, username,labelIds)
        correo = obtenerCorreo(api, version, username, id)

        print(correo)
        '''
