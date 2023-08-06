# __init__.py

# Version 
__version__ = "1.0.0"


import simplejson as json
import boto3
import os

AWS_KEY = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET = os.environ['AWS_SECRET_ACCESS_KEY']

if 'AWS_SESSION_TOKEN' in os.environ:
	AWS_SESSION = os.environ['AWS_SESSION_TOKEN']

yachtDefaultObject = {
		"sheets":{
			"template":[],
			"data":[],
			"labels":[],
			"key":[],
			"lines":[],
			"periods":[],
			"labels":[],
			"chartId":"linechart",
			"options":[],
			"dropdown":[]
			}
	}

def syncData(jsonObject,id,yacht=False,version=20):

	finalJson = json.dumps(jsonObject, indent=4)

	print("Connecting to S3")
	bucket = 'gdn-cdn'

	if 'AWS_SESSION_TOKEN' in os.environ:
		session = boto3.Session(
		aws_access_key_id=AWS_KEY,
		aws_secret_access_key=AWS_SECRET,
		aws_session_token = AWS_SESSION
		)
	else:
		session = boto3.Session(
		aws_access_key_id=AWS_KEY,
		aws_secret_access_key=AWS_SECRET,
		)

	s3 = session.resource('s3')

	if yacht:
		key = "yacht-charter-data/{id}.json".format(id=id)
	else:
		key = "{id}.json".format(id=id)

	object = s3.Object(bucket, key)
	object.put(Body=finalJson, CacheControl="max-age=30", ACL='public-read', ContentType="application/json")

	print("JSON is updated")

	if yacht:
		print("data", "https://interactive.guim.co.uk/yacht-charter-data/{id}.json".format(id=id))
		print("chart", "https://interactive.guim.co.uk/embed/aus/2020/yacht-charter-v{version}/index.html?key={id}&location=yacht-charter-data".format(id=id, version=version))
	else:
		print("data", "https://interactive.guim.co.uk/{id}.json".format(id=id))

def yachtCharter(template, data, chartName, dropdown = [], lines=[], chartId=[{"type":"linechart"}], options=[{"colorScheme":"guardian"}],key=[], periods=[], labels=[], version=24):

	jsonDictObject = {
		"sheets":{
			"template":template,
			"data":data,
			"labels":labels,
			"key":key,
			"lines":lines,
			"periods":periods,
			"labels":labels,
			"chartId":chartId,
			"options":options,
			"dropdown":dropdown
			}
	}

	#%% Sync

	syncData(jsonDictObject, chartName, yacht=True, version=version)