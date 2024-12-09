from flask import Flask, request, render_template
import createTable
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import deleteTable
from context import Context
from logger import book_logger

application = Flask(__name__)
newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
table_name = createTable.create_dax_table('employeeTable')
dynamodb = Context.dynamodb_local
logger = book_logger()


@application.route('/employee', methods=['PUT'])
def create_employee():
    try:
        request_data = request.get_json()
        employee_names = []
        if request.method == 'PUT':
            employee_table = dynamodb.Table(table_name)
            # Loop through the list of all employees
            for all_employees in request_data:
                employee_name = all_employees['name']
                if employee_name == '':
                    logger.info(f'Employee name is: {employee_name}')
                    return f'Employee name is: {employee_name}', 400
                employee_names.append(employee_name)
                employee_id = all_employees['id']
                if employee_id == 0 or None:
                    logger.info(f'Employee ID is: {employee_id}')
                    return f'Employee ID is: {employee_id}', 400
                employee_list = employee_table.query(
                    KeyConditionExpression=Key('id').eq(employee_id))
                items = employee_list['Items']
                if len(items) != 0:
                    emp_id = items[0]['id']
                    if employee_id == emp_id:
                        logger.info('Employee already exist')
                        logger.info(f'Employee with ID: {employee_id} already exist')
                        return f'Employee with ID: {employee_id} already exist', 409
                response = employee_table.put_item(Item=all_employees)
                logger.info('Employee successfully added')
                logger.info(f'Employee with ID: {employee_id} Employee successfully added')
        logger.info(f'Successfully created Employees: {employee_names}')
        return f'Successfully created Employees: {employee_names}', 201
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee', methods=['POST'])
def update_employee():
    try:
        request_data = request.get_json()
        employee_names = []
        if request.method == 'POST':
            employee_table = dynamodb.Table(table_name)

            for all_employees in request_data:
                employee_name = all_employees['name']
                get_employee_name()
                employee_names.append(employee_name)
                employee_id = all_employees['id']
                get_employee_id()
                employee_age = all_employees['age']
                get_employee_age()
                employee_address = all_employees['address']
                employee_gender = all_employees['gender']
                employee_list = employee_table.query(
                    KeyConditionExpression=Key('id').eq(employee_id))
                items = employee_list['Items']
                if len(items) == 0:
                    logger.info('Employee does not exist exist')
                    logger.info(f'Employee with ID: {employee_id} does not exist')
                    return f'Employee with ID: {employee_id} does not exist', 200
                response = employee_table.update_item(
                    Key={
                        'id': employee_id,
                        'name': employee_name
                    },
                    UpdateExpression="set age=:a,address=:d,gender=:g",
                    ExpressionAttributeValues={
                        ':a': employee_age,
                        ':d': employee_address,
                        ':g': employee_gender

                    },

                    ReturnValues="UPDATED_NEW"

                )
                logger.info('Successfully updated employee')
                logger.info('Successfully updated employee')
        logger.info(f'Successfully updated Employee: {employee_names}')
        return f'Successfully updated Employee: {employee_names}', 200
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee/allEmployees', methods=['GET'])
def get_employees():
    try:
        if request.method == 'GET':
            employee_table = dynamodb.Table(table_name)

            # Loop through all the items and load each
            employee_list = employee_table.scan(
                Select="ALL_ATTRIBUTES"
            )
            if employee_list['Count'] == 0:
                logger.info(f"There are no Employees in the Data Base")
                return f"There are no Employees in the Data Base", 200
            else:
                logger.info(f"The following employees exist in the Data base: {employee_list}")
                return f"The following employees exist in the Data base: {employee_list}", 200
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee', methods=['GET'])
def get_employee():
    try:
        request_data_id = get_employee_id()
        request_data_name = get_employee_name()
        if request.method == 'GET':
            employee_table = dynamodb.Table(table_name)

            # Loop through all the items and load each
            employee_list = employee_table.query(
                KeyConditionExpression=Key('id').eq(int(request_data_id))
            )
            if employee_list['Count'] == 0:
                logger.info(f"There is no Employee in the Data Base with name: {request_data_name}")
                return f"There is no Employee in the Data Base with name: {request_data_name}", 200
            else:
                for employee in employee_list['Items']:
                    if employee['id'] == int(request_data_id):
                        logger.info('Successfully retrieved employee')
                        logger.info(f'Successfully retrieved Employee: {employee}')
                        return f'Successfully retrieved Employee: {employee}', 200
                    else:
                        logger.info(f'Successfully retrieved Employee: {employee}')
                        return f"No employee exist with name: {employee['name']}", 204
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee/index', methods=['GET'])
def get_html():
    try:
        if request.method == 'GET':
            logger.info(f'Successfully returned index page')
            return render_template('index.html')
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee', methods=['DELETE'])
def delete_employee():
    try:
        request_data_name = get_employee_name()
        request_data_id = int(request.args.get('id'))
        if request_data_id == 0 or None:
            logger.info(f'Employee ID is: {request_data_id}')
            return f'Employee ID is: {request_data_id}', 400
        if request.method == 'DELETE':
            employee_table = dynamodb.Table(table_name)

            employee_list = employee_table.query(
                KeyConditionExpression=Key('id').eq(request_data_id))
            items = employee_list['Items']
            if len(items) == 0:
                logger.info(f'No employees exist with id: {request_data_id}')
                logger.info(f'No employees exist with id: {request_data_id}')
                return f'No employees exist with id: {request_data_id}', 200

            response = employee_table.delete_item(
                Key={
                    'name': request_data_name,
                    'id': request_data_id
                }
            )
            logger.info('Successfully deleted employee')
            logger.info(f'Successfully deleted Employee {request_data_name}')
            return f'Successfully deleted Employee {request_data_name}', 202
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


@application.route('/employee/Employee_DB', methods=['DELETE'])
def delete_employee_db():
    try:
        deleteTable.delete_dax_table()
        logger.info(f'Successfully deleted {table_name} database')
        return f'Successfully deleted {table_name} database'
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


def get_employee_name():
    try:
        request_data_name = request.args.get('name')
        if request_data_name == '':
            logger.info(f'Employee name is: {request_data_name}')
            return f'Employee name is: {request_data_name}', 400
        else:
            return request_data_name
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


def get_employee_id():
    try:
        request_data_id = request.args.get('id')
        if request_data_id == 0 or None:
            logger.info(f'Employee ID is: {request_data_id}')
            return f'Employee ID is: {request_data_id}', 400
        else:
            return request_data_id
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


def get_employee_age():
    try:
        _request = request.args.get('age')
        if _request == '':
            logger.info(f'Employee age is: {_request}')
            return f'Employee age is: {_request}', 400
        else:
            return _request
    except ClientError as ex:
        logger.critical(ex.response)
        logger.error(f'An error occurred: {ex}')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080)
    # application.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
