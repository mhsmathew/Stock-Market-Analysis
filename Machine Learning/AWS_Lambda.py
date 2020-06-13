import os
import io
import boto3
import json
import csv
ENDPOINT_NAME = os.environ['ENDPOINT_NAME2']
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    output = {}
    data = json.loads(json.dumps(event))['body']
    #payload = data['data']
    data = json.loads(data)
    data = data['data']
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=data)
    response = response['Body'].read().decode("utf-8")
    pred = round(float(response),2)
    output["data"] = pred
    return output

