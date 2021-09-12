import csv, urllib.request
from urllib.request import urlretrieve as retrieve
import boto3

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'


def handler(event, context):
    retrieve(url, '/tmp/trialwhat.csv')
    print('did this succeed?')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('testbucket01234567899999')
    s3.meta.client.upload_file('/tmp/trialwhat.csv', 'testbucket01234567899999', 'nytdata_s3.csv')
    