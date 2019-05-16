import json
import datetime
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def response_wrapper(status_code,data):
    return {
            "isBase64Encoded": True,
            "statusCode": status_code,
            "headers": { 
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            "body": json.dumps(data,indent=4, cls=DecimalEncoder)
        }

def get_unixtime_now():
    now = datetime.datetime.now()
    return int(now.timestamp())

def get_unixtime_one_month_ago():
    return get_unixtime_now() - (60 * 60 * 24 * 31)