import boto3
import json
import requests
import os
import boto3
from botocore.exceptions import ClientError
import yaml
import sys
from cfn_flip import flip, to_yaml, to_json

# Parametros

tenant = "PONER TU TENANT"
consoleaddr = "us-east1.cloud.twistlock.com"
# Region = os.environ['Region']
# bucketName = os.environ['BucketName']
# secret_name = os.environ['secretname']
accesskey = "ACCESS"
secret = "SECRET"
task = 'fargate-task-definition'

unprotected_fn = 'unprotected.json'
protected_fn = 'protected.json'
client = boto3.client('ecs')

def getToken(accesskey,secret):

	print('Autenticando...')
	loginurl = "{}/api/v1/authenticate".format(tenant)

	credentials = {"username": accesskey,"password": secret}
	
	payload = json.dumps(credentials)
	
	headers = {
	    "Accept": "application/json; charset=UTF-8",
    	"Content-Type": "application/json; charset=UTF-8"
	}

	loginresp = requests.request("POST", loginurl, data=payload, headers=headers)
	if loginresp.status_code == 200:
		loginresp = json.loads(loginresp.text)
		token = loginresp['token']
		print('Autenticado exitoso!')
	else:
		print('\nValidar credenciales y/o tenant...\n')
	return token

def getTask():
	
	print('Obteniendo el task de AWS con nombre: ' + task)
	response = client.describe_task_definition(
	    taskDefinition=task,
	)
	print('Se obtuvo el task satisfactoriamente.')
	mytask = response['taskDefinition']
	delete_list = ['taskDefinitionArn', 'registeredAt', 'registeredBy', 'revision']
	for d in delete_list:
		mytask.pop(d)
	
	json_o = json.dumps(mytask, indent=3)
	json_file = open('%s' % unprotected_fn, 'w')
	json_file.write(json_o)
	json_file.close()
	print('Se escribió exitosamente el archivo json localmente')

def getTaskProtected(token):

	print('Enviando la solicitud de App-Embbeded a Prisma Cloud...')
	url = "{}/api/v1/defenders/fargate.json".format(tenant)
	token = 'Bearer ' + token
	headers = {
    'Authorization': token,
	}
	data = open(unprotected_fn, 'rb').read()
	querystring = {"consoleaddr": consoleaddr,"defenderType":"appEmbedded"}
	req = json.loads(requests.post(url, headers=headers, params=querystring, data=data).text)
	req1 = json.dumps(req, indent=3, sort_keys=True)
	json_file = open('%s' % protected_fn, 'w')
	json_file.write(req1)
	json_file.close()

def convertToJson():

	yaml_file = open('task-definition.yaml')
	json_file = 'task-definition.json'
	json = to_json(yaml_file)
	print(json)
	# json_f = open('%s' % json_file, 'w')
	# json_f.write(json)
	# json_f.close()

def reports_lambda_handler(event, context):
	
#	task_definition = getTask()
#	token = getToken(accesskey,secret)
#	getDefender = getTaskProtected(token)
	convertToJson()

event = ""
context = ""
resultados = reports_lambda_handler(event, context)
