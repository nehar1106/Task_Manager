import boto3
from datetime import datetime
import json



dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
task_table = dynamodb.Table('task_list')

def put_task(table, user_nm, task_desc, upd_ts):
    print(f"table is {table}")
    print(f"user_nm is {user_nm}")
    print(f"task_desc is {task_desc}")
    print(f"upd_ts is {upd_ts}")
    item = {
        'user_nm': user_nm,         
        'task_desc': task_desc,
        'upd_ts': upd_ts
    }

    
    table.put_item(Item=item)
    response = task_table.put_item(Item=item)
    return response

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        print("GET request")
        user_nm = event['queryStringParameters']['user_nm']
       

        response = task_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_nm').eq(user_nm)
        )
       
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps(response['Items'])
        }

    elif event['httpMethod'] == 'POST':
        print("POST request")

        try:
            body = json.loads(event['body'])

            user_name = body['user_name']
            task_desc = body['task_desc']
            upd_ts = body.get('upd_ts', datetime.utcnow().isoformat())

            response = put_task(task_table, user_name, task_desc, upd_ts)

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': json.dumps({'message': 'Task saved successfully', 'response': response})
            }

        except Exception as e:
            print(f"Error: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
