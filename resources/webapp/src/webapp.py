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
    bucket_name = 'cdkdemobucket'
    s3obj = s3.Object(bucket_name, 'top/index.html').get()
    page = s3obj['Body'].read().decode(encoding='utf-8')
    template = jinja2.Template(page)

    data = {}

    bucket = s3.Bucket(bucket_name)
    objs = bucket.meta.client.list_objects_v2(Bucket = bucket.name, Prefix = '')
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    
    for obj in objs.get('Contents'):
        url = "https://{0}.s3-{1}.amazonaws.com/{2}".format(
            bucket_name,
            bucket_location['LocationConstraint'],
            obj.get('Key')
        )
        content = "cdkdemobucket/{0}".format(
            obj.get('Key')
        )

        data[content] = url
    
    res =  {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {"Content-Type": "*/*"},
        'body': template.render(bucketdata=data)
    }
    return res

