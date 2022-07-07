import flask
#import pyodbc
from flask import request, jsonify


server = 'campdovetestsqlserver.database.windows.net'
database = 'CampDoveTest'
username = 'campdove_read'
password = 'c@mpD0v3r3@d'   
driver= '{ODBC Driver 17 for SQL Server}'

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Testing DB Read</h1>
<p>A test for reading a DB</p>'''


#@app.route('/api/v1/dbread', methods=['GET'])
#def db_read():
#    test_string = ''
#    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#        with conn.cursor() as cursor:
#            cursor.execute("SELECT fname, lname, phone, email from people")
#            row = cursor.fetchone()
#            while row:
#                test_string = test_string + '<p>' + (str(row[0]) + " " + str(row[1])) + " " + str(row[2]) + " " + str(row[3]) + '</p>';
#                row = cursor.fetchone()
#    return test_string;

# driver function
#if __name__ == '__main__':
    #app.run(debug = True)