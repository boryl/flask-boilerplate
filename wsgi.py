'''
    File name: wsgi.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
'''

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
