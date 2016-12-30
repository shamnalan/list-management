from bottle import *
#from flask import request
import logging
import psycopg2
import json

_api_version = 1.0

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


# GET http://server_ip:port/api/version
@get('/api/version')
def get_data():
    logging.info("HTTP get call made to /api/version")
    return {'success': True, 'version': _api_version}

#@get('/api/lists')
@app.route('/api/lists', method=['OPTIONS', 'GET'])
def get_data():
    logging.info("HTTP get call made to /api/lists")

    query = 'SELECT list_name, list_id, list_type, list_owner FROM listmanagement.lists'
    lists = _execute_query(query, ('user_name',))

    #callback = request.args.get('callback')
    #logging.info('Callback '+request)
    #return '{0}({1})'.format(callback, {'a':1, 'b':2})

    #return { "name":"John", "age":31, "city":"New York" }
    #one = request.GET.get('one', '').strip()
    #callback = request.query.callback
    #logging.info('Lists -->' + lists)
    data = json.dumps(lists)
    #logging.info('Data -->' + data)

    #jsonresp = [{ "name":"John", "age":31, "city":"New York" }, { "name":"Sham", "age":31, "city":"New Jersey" }]

    return data
    #return '{0}({1})'.format(callback, data)
    #return json.dumps(jsonresp)

@app.route('/api/new-list', method=['OPTIONS', 'POST'])
def create_list():

    # Get the JSON from the API request
    request_json = request.json

    if request_json is not None:
        logging.info("You asked me to create a new list called %s", request_json)

        # Get first name and last name from JSON, default to None
        list_name = request_json.get('list_name', None)
        query = 'INSERT INTO listmanagement.lists (list_name, list_id, list_type, list_owner) VALUES (%s, %s, %s, %s)'

        _execute_sql(query, (list_name, '001', 'CompanyType', 'Sham Nalan'))

    return {'success': True }


# Create a new user
@post('/api/new-user')
def create_user():
    logging.info("HTTP post call made to /api/new-user")

    # Get the JSON from the API request
    request_json = request.json

    # Get first name and last name from JSON, default to None
    first_name = request_json.get('first_name', None)
    last_name = request_json.get('last_name', None)
    username = request_json.get('username', None)

    logging.info("You asked me to create a new user called %s %s", first_name, last_name)
    return {'success': True}


# Return all users in the table
@get('/api/all-users')
def get_all_users():
    logging.info("HTTP post call made to /api/all-users")

    # We need to implement this

    return {'success': True}


# Delete a user from the table
@delete('/api/delete-user')
def delete_user():
    logging.info("HTTP delete call made to /api/delete-user")

    # Get the JSON from the API request
    request_json = request.json

    # Get first name and last name from JSON, default to None
    first_name = request_json.get('first_name', None)
    last_name = request_json.get('last_name', None)
    username = request_json.get('username', None)

    logging.info("You asked me to delete a user called %s %s", first_name, last_name)


def _execute_sql(sql, values):
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(sql, values)

    rows_affected=cursor.rowcount
    logging.info("Rows effected ---> %s", rows_affected)


    cursor.close()
    conn.close()

def _execute_query(sql, values):
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(sql, values)
    #rows_affected=cursor.rowcount
    #data = cursor.fetchall()

    #logging.info("Queried values are %s", data)
    #cur.execute(query, args)
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.connection.close()
    return r
    #return (r[0] if r else None) if one else r

    #cursor.close()
    #conn.close()
    #return data

def _get_connection():
    conn = psycopg2.connect("dbname='listmanagement' user='postgres' host='postgres' password='password'")
    conn.autocommit = True
    return conn

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    logging.info('Starting HTTP server')
    #run(host='0.0.0.0', port=8080, reloader=True, debug=True)
    run(app, host='0.0.0.0', port=8080)


main()
