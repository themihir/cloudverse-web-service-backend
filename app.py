import json
import simplejson
import logging
import CONSTANT
import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, make_response, request, Response

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/')
def hello_world():
    logger.info('Hello World!')
    return 'Hello World!'


@app.route('/createWorkstation', methods=['POST'])
def create_workstation():
    response_dict = {'successCode': 200, 'successMessage': 'Success'}
    received_dict = request.json
    logger.info("received input:\n", received_dict)

    try:
        sqs_client = boto3.client('sqs')
        response = sqs_client.send_message(
            QueueUrl=CONSTANT.SQS_QUERY_URL,
            MessageBody=json.dumps(received_dict))
        logger.info(response)

    except Exception as ex:
        logger.info("exception:\n", ex)
        response_dict = {'successCode': 400, 'successMessage': 'Failed'}
    response_data = jsonify(response_dict)
    response_data.headers['Access-Control-Allow-Origin'] = '*'
    return response_data


@app.route('/resumeWorkstation', methods=['POST'])
def resume_workstation():
    response_dict = {'successCode': 200, 'successMessage': 'Success'}
    received_dict = request.json
    logger.info("received input:\n", received_dict)

    try:
        sqs_client = boto3.client('sqs')
        response = sqs_client.send_message(
            QueueUrl=CONSTANT.SQS_QUERY_URL,
            MessageBody=json.dumps(received_dict))
        logger.info(response)
    except Exception as ex:
        logger.info("exception:\n", ex)
        response_dict = {'successCode': 400, 'successMessage': 'Failed'}
    response = jsonify(response_dict)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/listWorkstation', methods=['POST'])
def list_workstation():
    received_dict = request.json
    user_id = received_dict.get('userId')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cloudverse_prod_users')
    user_data = {}
    # response_dict = {'successCode': 200, 'successMessage': 'Success'}
    try:
        # data validation
        if user_id is None or user_id == "":
            raise Exception("User is not valid")

        # executing query for dynamoDB table
        response = table.query(
            KeyConditionExpression=Key('userId').eq(user_id))
        logger.info("data fetched from db")
        user_data = response.get('Items')
        if not user_data:
            raise Exception("User data is not available")
        # workstation_list = [data.get('workstations') for data in user_data]
        success_code = 200
    except Exception as ex:
        logger.info("exception:\n", ex)
        success_code = 400
    resp = Response(simplejson.dumps(user_data),
                    headers={'Access-Control-Allow-Origin': '*'},
                    status=success_code,
                    mimetype='application/json')
    return resp


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


if __name__ == '__main__':
    app.run(debug=True)
