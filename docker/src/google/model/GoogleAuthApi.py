'''
    https://developers.google.com/admin-sdk/directory/
    https://developers.google.com/admin-sdk/directory/v1/reference/users/

    aca estan los scopes
    https://developers.google.com/identity/protocols/googlescopes

    sudo pip3 install --upgrade google-api-python-client
    sudo pip3 install httplib2
'''

import os

from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

class GAuthApis:

    adminGoogle = os.environ['ADMIN_USER_GOOGLE']

    SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    """

    @classmethod
    def getCredentials(cls, username):
        ''' genera las credenciales delegadas al usuario username '''
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'credentials.json')

        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, cls.SCOPES)

        ''' uso una cuenta de admin del dominio para acceder a todas las apis '''
        admin_credentials = credentials.create_delegated(username)

        return admin_credentials

    @classmethod
    def getService(cls, username=adminGoogle, api='admin', version='directory_v1'):
        ''' crea un servicio de acceso a las apis y lo retora '''
        credentials = cls.getCredentials(username)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build(api, version, http=http)
        return service
