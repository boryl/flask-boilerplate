import click
from flask.cli import with_appcontext
import csv
import json
import os
import boto3
from flask import current_app as app


# S3 conf and upload
def upload_files(path, destination_folder='', many=False):
    # DEV or PROD bucket
    session = boto3.Session(
        aws_access_key_id=app.config['CLOUDCUBE_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['CLOUDCUBE_SECRET_ACCESS_KEY'],
        region_name=app.config['CLOUDCUBE_REGION_NAME']
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(app.config['CLOUDCUBE_BUCKET_NAME'])
    folder_prefix = app.config['CLOUDCUBE_FOLDER_PREFIX']

    if(many):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if (not file.startswith('.')):
                    full_path = os.path.join(subdir, file)
                    with open(full_path, 'rb') as data:
                        click.echo(
                            destination_folder + full_path[len(path)+0:])
                        bucket.put_object(
                            Key=folder_prefix + destination_folder +
                            full_path[len(path)+0:], Body=data)
    else:
        head, tail = os.path.split(path)
        data = open(path, 'rb')
        click.echo(destination_folder + tail)
        bucket.put_object(
            Key=folder_prefix + destination_folder + tail, Body=data)


# Read CSV File
def read_CSV(csv_file, json_file):
    csv_rows = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend(
                [{field[i]:row[field[i]] for i in range(len(field))}])
        convert_write_json(csv_rows, json_file)


# Convert csv data into json
def convert_write_json(data, json_file):
    # Check if folder "resources" exists
    with open('resources/' + json_file, "w") as f:
        f.write(json.dumps(
            data, sort_keys=False, indent=4, separators=(',', ': ')))


# Convert CSV file to JSON with optional S3 upload
# flask csvexport --env dev filename.csv
# flask csvexport --env dev --destination destination/foler/on/s3/ filename.csv
@click.command("csvexport")
@with_appcontext
@click.option(
    '--env', '-e', type=click.Choice(['dev', 'prod', 'none']), default='none')
@click.option('--destination', '-d')
@click.argument("csv_file", required=False, type=click.Path(exists=True))
def csvexport(destination, env, csv_file=False):

    json_file = 'appcontent.json'

    if(csv_file):
        if(os.path.splitext(csv_file)[1] != '.csv'):
            exit('Not a CSV file')
    else:
        csv_file = 'resources/csv/source.csv'

    read_CSV(csv_file, json_file)
    # Validate CSV content
    # check images exists in folder
    if(env != 'none'):
        destination = os.path.join(env + '/' + destination, '')
        upload_files('resources/' + json_file, destination, False)
        click.echo('CSV uploaded to: ' + destination)
    else:
        click.echo('CSV process done')


# Upload file or folder to S3
# flask s3uploadfile --env dev --destination destination_foler/ filename.txt
# flask s3uploadfile --folder --env prod
# --destination destination/foler/on/s3/  path/to/folder
@click.command("s3upload")
@with_appcontext
@click.option('--env', '-e', type=click.Choice(['dev', 'prod']), default='dev')
@click.option('--destination', '-d')
@click.option('--folder', '-f', is_flag=True)
@click.argument("source", required=True, type=click.Path(exists=True))
def s3upload(env, destination, folder, source):
    destination = os.path.join(env + '/' + destination, '')
    upload_files(source, destination, folder)
    click.echo(source + ' uploaded to ' + destination)
