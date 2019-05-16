import json
import boto3
from dynamo.article import Article
from common import utils
import datetime
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_article_handler(event,context):
    article = Article()
    options = event['pathParameters']
    if 'title' in options:
        uri = options['title']
    else:
        msg = {
            "message": "pathParameters KeyError: '{}' is undefined!!".format('title')
        }
        return utils.response_wrapper(500,msg)
    
    response = article.get_item(uri)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return utils.response_wrapper(200,response['Item']) 
    elif response['ResponseMetadata']['HTTPStatusCode'] == 400:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(400,err) 
    elif response['ResponseMetadata']['HTTPStatusCode'] == 500:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(500,err) 

def put_article_handler(event,context):
    logger.info('body param is {}'.format(event['body']))
    logger.info('pathParameters param is {}'.format(event['pathParameters']))

    article = Article()
    options = event['pathParameters']
    article_info = json.loads(event['body'])
    #validate parameters
    if 'title' in options:
        uri = options['title']
    else:
        msg = "pathParameters KeyError: '{}' is undefined!!".format('title')
        logger.error(msg)
        return {
            "message": msg
        }
    author = article_info['author']
    contents = article_info['contents']
    title = article_info['title']
    created_at = utils.get_unixtime_now()

    logger.info('Start put article with {},{},{},{},{}'.format(uri,author,contents,created_at,title))
    response = article.put_item(uri,author,contents,created_at,title)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = {
            'message': 'Request is success.'
        }
        logger.info('Return msg with 200')
        return utils.response_wrapper(200,msg)
    elif response['ResponseMetadata']['HTTPStatusCode'] == 500:
        err = {
            "message": "Internal server error"
        }
        logger.error('Return msg with 500')
        return utils.response_wrapper(500,err)
    
def delete_article_handler(event,context):
    article = Article()
    options = event['pathParameters']
    if 'title' in options:
        uri = options['title']
    else:
        msg = {
            "message": "pathParameters KeyError: '{}' is undefined!!".format('title')
        }
        return utils.response_wrapper(500,msg)
        
    response = article.delete_item(uri)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        msg = {
            "message": "Delete article is succeed!!!"
        }
        return utils.response_wrapper(200,msg)
    elif response['ResponseMetadata']['HTTPStatusCode'] == 400:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(400,err) 
    elif response['ResponseMetadata']['HTTPStatusCode'] == 500:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(500,err) 

def get_latest_article_handler(event,context):
    article = Article()
    
    response = article.get_latest_items()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return utils.response_wrapper(200,{ "items": response.get('Items',[])})
    elif response['ResponseMetadata']['HTTPStatusCode'] == 400:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(400,err) 
    elif response['ResponseMetadata']['HTTPStatusCode'] == 500:
        err = {
            "message": response['ResponseMetadata']['Message']
        }
        return utils.response_wrapper(500,err) 