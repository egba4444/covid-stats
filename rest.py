import boto3
import json
def handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('covid-data2')
    response = table.get_item(
        Key={
            'date': event['queryStringParameters']['date']
        }
    )
    if 'Item' in response:
        return {
            'statusCode': '200',
            'body': json.dumps(response['Item'])
            }
    else:
        return {
            'statusCode': '404',
            'body': 'Not found'
        }