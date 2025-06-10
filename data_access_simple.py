import pymysql
from pymysql.cursors import DictCursor
import csv

def connect(db_config, sql_query, connected_behavior):
    try:
        # Establish connection to the remote database
        connection = pymysql.connect(**db_config)
        print("Connection established successfully!")

        try:
            result = connected_behavior(connection, sql_query)
                    
        except Exception as query_error:
            print("Error during query execution:", query_error)
        
    except Exception as conn_error:
        print("Error connecting to database:", conn_error)

    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("Database connection closed.")
        
        return result

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

def retrieve_all_rows_and_write_to_csv(connection, sql_query, output_name="output"):
    with connection.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()
                print("Query executed successfully.")

                

                with open( output_name+'.csv', mode='w', newline= '', encoding='utf-8') as csvfile:
                    fieldnames = {a[0] for a in cursor.description}
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    headerwriter = csv.writer(csvfile)
                    headerwriter.writerow(fieldnames)
                    for row in results:
                        writer.writerow(row)
                        print(row)
                return 1


def fetch_table_names(connection, sql_query):
       with connection.cursor() as cursor:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                results = [ list(row.values())[0] for row in rows ]
                print("Query executed successfully.")
                return results


def dump_all_tables():
    db_request = create_db_request_from_credentials("C:/Users/user/Documents/yourCredentials/credentials.txt")

    table_names = connect(db_request, "SHOW TABLES", fetch_table_names)
    print(table_names)
    for table_name in table_names:
        connect(db_request, "SELECT * FROM " + table_name +";", lambda a, b : retrieve_all_rows_and_write_to_csv(a, b, table_name))


dump_all_tables()