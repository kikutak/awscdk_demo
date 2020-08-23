import json
import boto3
import logging
import io
import base64
import jinja2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.resource('s3')

def main(event, context):
    if(not event):
        return {
            'isBase64Encoded': False,
            'headers': {"Content-Type": "*/*"},
            'statusCode': 500,
            'body': "event is null"
        }

    method = event['requestContext']['httpMethod']

    if(method == 'GET'):
        return get_template()

def get_template():
    s3obj = s3.Object('cdkdemobucket', 'top/index.html').get()
    page = s3obj['Body'].read().decode(encoding='utf-8')
    template = jinja2.Template(page)

    data = {}

    bucket = s3.Bucket('cdkdemobucket')
    objs = bucket.meta.client.list_objects_v2(Bucket = bucket.name, Prefix = '')

    for obj in objs.get('Contents'):
        data[obj.get('Key')] = 'http://aaa'
    
    res =  {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {"Content-Type": "*/*"},
        'body': template.render(data=data)
    }
    return res

def get_page():
    s3obj = s3.Object('cdkdemobucket', 'top/index.html').get()
    page = s3obj['Body'].read()

    res =  {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {"Content-Type": "*/*"},
        'body': page.decode(encoding='utf-8')
    }
    return res

""" 
    if(event["action"] == "Create"):
        return {
            'statusCode':200
            'body':"Create"
        }

    if(event["action"] == "Destroy"):
        return {
            'statusCode':200
            'body':"Destroy"
        } """


"""     bucket = "cdkdemobucket/top"
    key = "testdata.txt"
    file_contents = "testdata"

    obj = s3.Object(bucket, key)
    obj.put(Body = file_contents)
    return """
