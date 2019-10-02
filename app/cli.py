'''
    File name: cli.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Command line interface functionality
'''

import click
from flask.cli import AppGroup
import csv
import json
import os
import boto3
from flask import current_app as app
from .models import ContentSchema
from marshmallow import ValidationError
import shutil
from distutils.dir_util import copy_tree


content_schema = ContentSchema(many=True)
content_master_folder = app.config['APP_CONTENT_FOLDER']
content_build_folder = app.config['APP_CONTENT_BUILD_FOLDER']
json_file = content_master_folder + app.config['APP_CONTENT_FILE']
csv_file = content_master_folder + app.config['APP_CSV_FILE']
content_cli = AppGroup('content')


# S3 conf and upload
def upload_files(path, destination_folder='', env='stage', many=False):
    # STAGE or PROD bucket
    if(env == 'prod'):
        aws_access_key_id = app.config['PROD_BUCKET_ACCESS_KEY_ID']
        aws_secret_access_key = app.config['PROD_BUCKET_SECRET_ACCESS_KEY']
    else:
        aws_access_key_id = app.config['STAGE_BUCKET_ACCESS_KEY_ID']
        aws_secret_access_key = app.config['STAGE_BUCKET_SECRET_ACCESS_KEY']

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=app.config['BUCKET_REGION_NAME']
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(app.config['BUCKET_NAME'] + '-' + env)
    folder_prefix = app.config['BUCKET_FOLDER_PREFIX']

    if(many):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if (not file.startswith('.')):
                    full_path = os.path.join(subdir, file)
                    with open(full_path, 'rb') as data:
                        click.echo(
                            'Processing: ' +
                            destination_folder +
                            full_path[len(path)+0:])
                        bucket.put_object(
                            Key=folder_prefix + destination_folder +
                            full_path[len(path)+0:], Body=data)
    else:
        head, tail = os.path.split(path)
        data = open(path, 'rb')
        bucket.put_object(
            Key=folder_prefix + destination_folder + tail, Body=data)


# Read CSV File
def read_CSV(csv_file, json_file, build=False):
    if (not os.path.isfile(csv_file)):
        click.echo(
            'Can\'t find source.csv needed in local folder resources/master/'
            )
        click.echo('')
        return False

    csv_rows = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend(
                [{field[i]:row[field[i]] for i in range(len(field))}])
        try:
            result = content_schema.load(csv_rows)
        except ValidationError as err:
            for item in err.messages.items():
                data_row = str(item[0])
                spreadsheet_row = str(item[0] + 2)
                click.echo(
                    'Spreadsheet row: ' + spreadsheet_row +
                    ' (Item: ' + data_row + ')'
                    )
                for subitem in item[1].items():
                    click.echo(str(subitem[1]))
                click.echo('')
            return False
        if(build):
            return convert_write_json(result, json_file)
        else:
            return True


# Convert csv data into json
def convert_write_json(data, json_file):
    with open(json_file, "w", encoding='utf-8') as f:
        data = json.dumps(
            data, sort_keys=False,
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False)
        f.write(data)
    return True


# Validate resources/master/source.csv (or specified csv file)
# command: flask validate_content (resources/master/filename.csv)
@content_cli.command("validate")
@click.option(
    '--source', '-s',
    required=False,
    type=click.Path(exists=True),
    help='Path to csv file'
    )
def validate_content(source=False):
    """Validate resources/master/source.csv (or passed csv file)"""
    click.echo('')
    click.echo('-----------------------------')

    if(source):
        csv_validation_file = source
    else:
        csv_validation_file = csv_file

    if(read_CSV(csv_validation_file, json_file)):
        click.echo(u'\u2713' + ' CSV process done')
    else:
        click.echo(u'\u2717' + ' CSV process failed')

    click.echo('-----------------------------')
    click.echo('')


# Validate resources/master/source.csv
# Create content json file
# Copy images to resources/contentbuild/
# Make zip with current content (json and images)
# command: flask content build
@content_cli.command("build")
def build_content():
    """Validate and process content"""
    click.echo('')
    click.echo('-----------------------------')

    # Validate csv file
    if(read_CSV(csv_file, json_file, True)):
        click.echo(u'\u2713' + ' CSV build process done')
    else:
        click.echo(u'\u2717' + ' CSV build process failed')
        click.echo('-----------------------------')
        click.echo('')
        return

    # Process app content
    try:
        tmp_folder = 'resources/_tmp'

        # Remove temp folder
        if(os.path.isdir(tmp_folder)):
            shutil.rmtree(tmp_folder)

        # Copy master image folder to temp folder
        shutil.copytree(
            os.path.join(content_master_folder, 'images/'),
            os.path.join(tmp_folder, 'images/')
            )

        # Zip current app content
        shutil.copy2(json_file, tmp_folder)
        shutil.make_archive(
            os.path.join(content_build_folder, 'appcontent'),
            'zip',
            tmp_folder
            )

        # Copy images to contentbuild
        copy_tree(
            os.path.join(tmp_folder, 'images/'),
            os.path.join(content_build_folder, 'images/')
            )

        # Remove temp folder
        shutil.rmtree(tmp_folder)

        click.echo(u'\u2713' + ' App content process done')
    except IOError as e:
        print(e)
        click.echo(u'\u2717' + ' Error when copying app content file')
        click.echo('-----------------------------')
        click.echo('')
        return

    click.echo('-----------------------------')
    click.echo('')

# Upload resoures/contentbuild/ to S3
# Choose stage or prod bucket
# command: flask upload_content --env prod
@content_cli.command("upload")
@click.option(
    '--env', '-e',
    type=click.Choice(['stage', 'prod']),
    default='stage',
    help='Choose S3 bucket'
    )
def upload_content(env):
    """Upload processed content to S3"""
    click.echo('')
    click.echo('-----------------------------')
    if(os.path.isdir(content_build_folder)):
        upload_files(content_build_folder, '', env, True)
        click.echo(
            u'\u2713' + ' App content uploaded to S3 (bucket: ' + env + ')'
            )
    else:
        click.echo(u'\u2717' + ' Folder resources/contentbuild/ is missing')
        click.echo(u'\u2717' + ' Run flask content build')
    click.echo('-----------------------------')
    click.echo('')


# Upload file or folder to S3
# command: flask s3uploadfile --env dev
# --destination destination_foler/ filename.txt
# command: flask s3uploadfile --folder --env prod
# --destination destination/foler/on/s3/  path/to/folder
@click.command("s3upload")
@click.option(
    '--env', '-e', type=click.Choice(['stage', 'prod']), default='stage'
    )
@click.option('--destination', '-d', default='')
@click.option('--folder', '-f', is_flag=True)
@click.argument("source", required=True, type=click.Path(exists=True))
def s3upload(env, destination, folder, source):
    destination = os.path.join(destination, '')
    upload_files(source, destination, env, folder)
    uploaded_to = ' uploaded'
    if(destination):
        uploaded_to += ' to ' + destination
    click.echo(source + uploaded_to)
