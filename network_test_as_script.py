import pymysql
from pymysql.cursors import DictCursor
import csv

def all_in_one_function():

    # fetch credentials from file
    file_path = 'C:/Users/user/Documents/yourCredentials/credentials.txt'

    with open(file_path, 'r') as file:
            lines = file.readlines()
            sql_username = lines[0].strip()
            sql_pass = lines[1].strip()
            hostname = lines[2].strip() 

    # Database configuration
    db_config = {
        'host': hostname,
        'port': 3306,
        'user': sql_username,
        'password': sql_pass,
        'db': 'IHIanonTelemetry',
        'cursorclass': DictCursor
    }

    # query
    sql_query = "SELECT * FROM tutorialStarted;"  

    try:
        # Establish connection to the remote database
        connection = pymysql.connect(**db_config)
        print("Connection established successfully!")

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()

                # Process and print the results
                print("Query executed successfully. Fetched data:")
                with open('output.csv', mode='w', newline= '', encoding='utf-8') as csvfile:
                    fieldnames = ['telemetryPingID', 'sessionID', 'userID', 'timestamp', 'gametime']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    headerwriter = csv.writer(csvfile)
                    headerwriter.writerow(fieldnames)
                    for row in results:
                        writer.writerow(row)
                        print(row)
                    
        except Exception as query_error:
            print("Error during query execution:", query_error)
        
    except Exception as conn_error:
        print("Error connecting to database:", conn_error)

    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Database connection closed.")


