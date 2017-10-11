

if __name__ == '__main__':
    import os
    import sys

    dominio = os.environ['GOOGLE_URL'].replace('http://','').replace('https://','')
    nombre = sys.argv[1]
    path = sys.argv[2]
    server = sys.argv[3]

    import auth_utils
    r = auth_utils.RegistrarServicio()
    r.register_once(name=nombre, domain=dominio, path=path, server=server)
