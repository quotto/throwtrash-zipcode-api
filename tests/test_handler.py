import unittest
import json
import os
os.environ['STAGE'] = 'dev'
from function import handler

class Test(unittest.TestCase):
    def test_search(self):
        response = handler.handler({
            'path': '/search',
            'queryStringParameters': {
                'zipcode': '1001701'
            },
            'headers': {'origin': 'http://localhost'}
        },{})

        self.assertEquals(response['statusCode'], '200')
        self.assertEquals(response['body'],json.dumps({
            'address': ['東京都青ヶ島村青ヶ島村一円']
        }))

    def test_load(self):
        response = handler.handler({
            'path': '/load',
            'queryStringParameters': {
                'address': '東京都青ヶ島村青ヶ島村一円'
            },
            'headers': {
                'origin': 'https://accountlink.mythrowaway.net'
            }
        },{})

        body = json.loads(response['body'])
        self.assertEqual(response['statusCode'], '200')
        self.assertEqual(body['data'][0],[{"type":"unburn","schedules":[{"type":"weekday","value":"0"},{"type":"biweek","value":"2-3"}]},{"type":"other","trash_val": "粗大ごみ","schedules":[{"type":"month","value":"15"},{"type":"evweek","value":{"weekday":"3","interval": 3,"start":"2021-05-16"}}]}])
        self.assertEqual(body['data'][1],[{"type":"burn","schedules":[{"type":"weekday","value":"0"}]},{"type":"other","trash_val":"生ごみ","schedules":[{"type":"month","value":"30"}]}])
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], 'https://accountlink.mythrowaway.net')

    def test_load_no_data(self):
        response = handler.handler({
            'path': '/load',
            'queryStringParameters': {
                'address': '東京都昭島市朝日町'
            },
            'headers': {
                'origin': 'http://localhost'
            }
        },{})
        body = json.loads(response['body'])
        self.assertEqual(len(body['data']), 0)
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], 'http://localhost')

    def test_load_parameter_error(self):
        response = handler.handler({
            'path': '/load',
            'queryStringParameters': {
            },
            'headers': {
                'origin': 'https://localhost'
            }
        },{})

        self.assertEqual(response['statusCode'], '400')
        body = json.loads(response['body'])
        self.assertEqual(body['message'],'パラメータエラー')