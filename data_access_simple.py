import pymysql
from pymysql.cursors import DictCursor
import csv

def connect(db_config, sql_query):
    try:
        # Establish connection to the remote database
        connection = pymysql.connect(**db_config)
        print("Connection established successfully!")

        try:
            retrieve_data(connection, sql_query, print_rows_and_write_to_csv)
                    
        except Exception as query_error:
            print("Error during query execution:", query_error)
        
    except Exception as conn_error:
        print("Error connecting to database:", conn_error)

    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Database connection closed.")

def create_db_request_from_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sql_username = lines[0].strip()
        sql_pass = lines[1].strip()
        hostname = lines[2].strip()
    
    db_config = {
        'host': hostname,
        'port': 3306,
        'user': sql_username,
        'password': sql_pass,
        'db': 'IHIanonTelemetry',
        'cursorclass': DictCursor
    }
    return db_config

def retrieve_data(connection, sql_query, data_processing_function):
    with connection.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()
                print("Query executed successfully.")
                data_processing_function(results)
                

def print_rows_and_write_to_csv(results):
     with open('output.csv', mode='w', newline= '', encoding='utf-8') as csvfile:
                    fieldnames = ['telemetryPingID', 'sessionID', 'userID', 'timestamp', 'gametime']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    headerwriter = csv.writer(csvfile)
                    headerwriter.writerow(fieldnames)
                    for row in results:
                        writer.writerow(row)
                        print(row)

def fetch_table_names(connection, sql_query):
       with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                results = [ list(row.values())[0] for row in rows ]
                print("Query executed successfully.")
                return results
       

connect(create_db_request_from_credentials("C:/Users/user/Documents/yourCredentials/credentials.txt"), "SELECT * FROM tutorialStarted")