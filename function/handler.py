import logging
import json
import os
import re
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.client('dynamodb')


TABLE_SUFFIX = '' if 'STAGE' not in os.environ else '-' + os.environ['STAGE']
address_collection_table = 'throwtrash-address-collection{}'.format(TABLE_SUFFIX)
trash_schedule_table = 'TrashSchedule{}'.format(TABLE_SUFFIX)

LAST_EVALUATED_KEY = 'LastEvaluatedKey'
LOG_LEVEL = logging.DEBUG if 'STAGE' in os.environ else logging.INFO

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(logging.StreamHandler())

prog = re.compile(r'(http|https):\/\/(localhost|accountlink\.mythrowaway\.net)$')

def handler(event, context):
    logger.debug(json.dumps(event))

    origin = event['headers']['origin']
    headers = {}
    if(prog.match(origin)):
        headers = {
            'Access-Control-Allow-Origin': origin,
        }
    logger.debug(json.dumps(headers))

    if(event['path'] == '/search'):
        zipcode = event['queryStringParameters']['zipcode']
        if(zipcode != None):
            response = dynamodb.query(
                TableName=address_collection_table,
                KeyConditionExpression='zipcode=:zipcode',
                ExpressionAttributeValues={
                    ':zipcode': {
                        'S': zipcode
                    }
                },
                ScanIndexForward=True,
                Limit=10
            )

            logger.info(json.dumps(response))

            address_list = []
            for item in response['Items']:
                address_list.append(item['address']['S'])

            return {
                'statusCode': '200',
                'body': json.dumps({
                    'address':  address_list
                }),
                'headers': headers,
            }
        return {
            'statusCode': '400',
            'body': json.dumps({
                'message': 'パラメータエラー'
            }),
        }
    elif(event['path'] == '/load'):
        query = event['queryStringParameters']
        if('address' in query):
            response = dynamodb.query(
                TableName=trash_schedule_table,
                IndexName='address-schedule',
                KeyConditionExpression='address=:address',
                ExpressionAttributeValues={
                    ':address': {
                        'S': query['address']
                    }
                },
                ScanIndexForward=False,
                Limit=50
            )

            logger.info(json.dumps(response))

            result_list = []
            if(response['Count'] > 0):
                for item in response['Items']:
                    result_list.append(json.loads(item['description']['S']))
            return {
                'statusCode': '200',
                'body':  json.dumps({
                    'data': result_list
                }),
                'headers': headers
            }
        return {
            'statusCode': '400',
            'body': json.dumps({
                'message': 'パラメータエラー'
            }),
        }

