import boto3
import csv

def handler(event, context):
    region = 'us-east-1'
    recList = []
    try:
        s3 = boto3.client('s3')
        dynamodb = boto3.client('dynamodb', region_name=region)
        client = boto3.resource('dynamodb')
        table = client.Table('covid-data2')
        confile = s3.get_object(Bucket='testbucket01234567899999', Key='nytdata_s3.csv')
        recList = confile['Body'].read().decode('utf-8').split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
        lastrow = list(csv_reader)[-1]
        
        
        response = table.get_item(
            Key={
            'date': lastrow[0]
            }
        )
        if 'Item' in response:
            print('message 11111')
            return
        else:
            print('message 2222222')
            response2 = dynamodb.put_item(
            TableName='covid-data2',
            Item={
                'date' : {'S':lastrow[0]},
                'cases' : {'S':lastrow[1]},
                'deaths' : {'S':lastrow[2]},
            }
        )
    except Exception as e:
        print(str(e))