import json
import boto3
from botocore.exceptions import ClientError
from common import utils
import decimal
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def dynamo_client(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table

class Article():
    
    table = dynamo_client('postObject')
    post_category = 'article'
    def __init__(self):
        pass

    def get_item(self,uri):
        
        key = {
            'postCategory': self.post_category,
            'uri': uri
        }
        response = {
            'ResponseMetadata': {}
        }
        try:
            response = self.table.get_item(
                    Key=key
                )
        except ClientError as e:
            response['ResponseMetadata']['HTTPStatusCode'] = 400
            response['ResponseMetadata']['Message'] = e.response['Error']['Message']
            return response

        if 'Item' in response:
            return response 
        else:
            logger.error('Item not found, {}'.format(response))
            response['ResponseMetadata']['HTTPStatusCode'] = 500
            response['ResponseMetadata']['Message'] = 'Item not found. Item does not exists.'
            return response    
    
    def put_item(self,uri,author,contents,created_at,title):
        response = self.table.put_item(
            Item={
                'postCategory': self.post_category,
                'uri': uri,
                'author': author,
                'contents': contents,
                'createdAt': created_at,
                'title': title
            }
        )
        return response
    
    def delete_item(self,uri):

        key = {
            'postCategory': self.post_category,
            'uri': uri
        }
        response = {
            'ResponseMetadata': {}
        }
        try:
            response = self.table.delete_item(
                    Key=key,
                    ReturnValues='ALL_OLD'
                )
        except ClientError as e:
            response['ResponseMetadata']['HTTPStatusCode'] = 400
            response['ResponseMetadata']['Message'] = e.response['Error']['Message']
            return response
        if 'Attributes' not in response:
            err = 'Given key {} does not exist so there is no change after detele item.'.format(uri)
            logger.error(err)
            response['ResponseMetadata']['HTTPStatusCode'] = 500
            response['ResponseMetadata']['Message'] = err
            return response
        return response
    
    def get_latest_items(self,time_from=None,time_till=None,number=5):
        if time_from is None:
            time_from = utils.get_unixtime_one_month_ago()
        if time_till is None:
            time_till = utils.get_unixtime_now()

        try:
            response = self.table.query(
                IndexName="postCategory-createdAt-index",
                KeyConditionExpression= "postCategory = :v_category and createdAt between :v_start and :v_end",
                ExpressionAttributeValues={
                    ":v_start": time_from,
                    ":v_end": time_till,
                    ":v_category": self.post_category
                },
                Limit=number
            )
        except ClientError as e:
            response['ResponseMetadata']['HTTPStatusCode'] = 400
            response['ResponseMetadata']['Message'] = e.response['Error']['Message']
            return response
        return response