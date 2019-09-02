import click
from flask.cli import with_appcontext	
import csv
import json
import sys
import os
import boto3
from flask import current_app as app


def upload_files(path, destination_folder='', many=False):
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
				full_path =  os.path.join(subdir, file)
			
				with open(full_path, 'rb') as data:
					print(folder_prefix + full_path[len(path)+1:])
					bucket.put_object(Key=folder_prefix + full_path[len(path)+1:], Body=data)
	else:
		head, tail = os.path.split(path)
		data = open(path, 'rb')
		bucket.put_object(Key=folder_prefix + destination_folder + tail, Body=data)



#Read CSV File
def read_CSV(csv_file, json_file):
	csv_rows = []
	with open(csv_file) as csvfile:
		reader = csv.DictReader(csvfile)
		field = reader.fieldnames
		for row in reader:
			csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
		convert_write_json(csv_rows, json_file)

#Convert csv data into json
def convert_write_json(data, json_file):
	# Check if folder "resources" excists
	with open('resources/' + json_file, "w") as f:
		f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))


@click.command("csvexport")
@with_appcontext
@click.option('--destination', '-d', type=click.Choice(['dev', 'prod', 'none']), default='none')
@click.argument("csv_file", required=False, type=click.Path(exists=True))
def csvexport(destination, csv_file=False):
	
	json_file = 'appcontent.json'
	
	if(csv_file):
		if(os.path.splitext(csv_file)[1] != '.csv'):
			exit('Not a CSV file')
	else:
		csv_file = 'resources/csv/source.csv'
		
	if(os.path.isfile(csv_file)):
		read_CSV(csv_file,json_file)
		if(destination != 'none'):
			upload_files('resources/' + json_file, destination + '/', False)
			click.echo('CSV uploaded to: ' + destination)
			
		click.echo('CSV process done')
		#validate JSON
		#upload to S3 - DEV or PROD
	else:
		exit('Can´t locate CSV file')
		
@click.command("s3upload")
@with_appcontext
@click.option('--destination', '-d', type=click.Choice(['dev', 'prod']), default='dev')
@click.argument("source_file", required=True, type=click.Path(exists=True))
def s3upload(destination, source_file=False):
	upload_files(source_file, destination + '/', False)
	click.echo(source_file + ' uploaded to ' + destination)
	
	# Folder upload
	
	"""
	json_file = 'parsed.json'
	
	if(csv_file):
		if(os.path.splitext(csv_file)[1] != '.csv'):
			exit('Not a CSV file')
	else:
		csv_file = 'source.csv'
		
	if(os.path.isfile(csv_file)):
		read_CSV(csv_file,json_file)
	else:
		exit('Can´t locate CSV file')
"""