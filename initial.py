import boto3
import csv

def handler(event, context):
    region = 'us-east-1'
    recList=[]
    try:
        s3 = boto3.client('s3')
        dynamodb = boto3.client('dynamodb', region_name=region)
        confile = s3.get_object(Bucket='testbucket01234567899999', Key='nytdata_s3.csv')
        recList = confile['Body'].read().decode('utf-8').split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
        firstrecord=True
        for row in csv_reader:
            print('message3.5')
            if(firstrecord):
                firstrecord=False
                continue
            date=row[0]
            cases=row[1] if row[1] else '-'
            deaths = row[2] if row[2] else '-'
            response = dynamodb.put_item(
                TableName='covid-data2',
                Item={
                    'date' : {'S':date},
                    'cases' : {'S':cases},
                    'deaths' : {'S':deaths},
                }
            )
            print('Put succeeded:')
        if dynamodb.get_item(TableName='covid-data2', Key={'date': {'S': '2020-01-21'},}) and not dynamodb.get_item(TableName='covid-data2', Key={'date': {'S': list(csv_reader)[-2][0]},}):
            lastrow = list(csv_reader)[-2]
            response = dynamodb.put_item(
                TableName='covid-data2',
                Item={
                    'date' : {'S':lastrow[0]},
                    'cases' : {'S':lastrow[1]},
                    'deaths' : {'S':lastrow[2]},
                }
            )
            
    except Exception as e:
        print(str(e))