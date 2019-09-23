# Flask boilerplate

Marshmallow, Flask-migrate, Postgres, Flasgger, Click, Flask-sqlalchemy, Gunicorn, Dotenv

## Prerequisites
* Python 3.7 with pip3 (install using Homebrew)
* Postgres (install using Homebrew)
* Virtualenv (```pip 3 install virutalenv```)
* Optional: Heroku CLI (install using Homebrew)

## Project setup
1) Create a virtual environment in project folder (```virtualenv venv```)
2) Activate virtual environment (```source venv/bin/activate```)
3) Install requirered modules (```pip install -r requirements.txt```)
4) Cop and rename example.env -> .env and set upp the variables in it
5) Start local Postgres server and create a database ("jlm")
6) Run database migrations (```flask db upgrade```)
7) Run flask app:
   
     Flask server: ```flask run```
   
     Production server: ```gunicorn wsgi:app```

## Project updates
Create database migrations script: ```flask db migrate  -m [message]"```

Create a requirements file: ```pip freeze requirements.txt```

## Heroku setup
1) Login to Heroku account (```heroku login```)
2) Add Heroku staging and production remote: (```heroku git:remote -a [dyno name]```)
3) Referencing dyno names as "staging" and "production"?
4) Making staging default remote (```git config heroku.remote staging```)
5) Deploy: (```git push heroku master```)
6) Run local Heroku: ```heroku local web```
