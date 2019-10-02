# Flask boilerplate

API/APP Boilerplate code. Gunicorn, SQLalchemy, Marshmallow, Flasgger, Boto3, Click

## Prerequisites
* Python 3.7 with pip3 (install using Homebrew)
* Postgres (install using Homebrew)
* Pipenv: ```pip3 install pipenv```
* Optional: Heroku CLI (install using Homebrew)

## Project setup
1) Create and activate a virtual environment in project folder: ```pipenv shell```
2) Install requirered modules: ```pipenv install```
3) Cop and rename example.env -> .env and set upp the variables in it
4) Start local Postgres server and create a database ("jlm")
5) Run database migrations: ```flask db upgrade```
6) Run flask app:
   
     Flask server: ```flask run```
   
     Production server: ```gunicorn wsgi:app```

## Processing app content updates
1) Download content csv file from Google Sheets
2) Rename file to source.csv and put it in resources/master/
3) Validate content file: ```flask content validate```
4) Build app content: ```flask content build```
5) Upload content to S3: 
   1) Stage: ```flask content upload --env stage```
   2) Production: ```flask content upload --env prod```

All images in resources/contentbuild/images are kept for legacy reasons. Never delete files in that folder!

## Project updates
Create database migrations script: ```flask db migrate  -m [message]"```

Update modules: ```pipenv update```

Create a pipfile.lock : ```pipenv lock```

## Heroku setup
1) Login to Heroku account: ```heroku login```
2) Add Heroku staging and production remote: ```heroku git:remote -a [dyno name]```
3) Referencing dyno names as "staging" and "production"?
4) Making staging default remote: ```git config heroku.remote staging```
5) Deploy: ```git push heroku master```
6) Run local Heroku: ```heroku local web```
