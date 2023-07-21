import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir= r"C:\#Dev\ImagineCup\instantclient_21_7")
# connection string in the format
# <username>/<password>@<dbHostAddress>:<dbPort>/<dbServiceName>
connStr = 'lab/lab@localhost:1521/xe'

# initialize the connection object
def PSelectSql():
    conn = None
    record = None
    try:
        # create a connection object
        conn = cx_Oracle.connect(connStr)

        # get a cursor object from the connection
        cur = conn.cursor()

        sql = "select name , location ,grade, cost, weight, logi from vegie"

        cur.execute(sql)

        record = cur.fetchall()
        conn.commit()

        # do something with the database
    except Exception as err:
        print('Error while connecting to the db')
        print(err)
    finally:
        if(conn):
            # close the cursor object to avoid memory leaks
            cur.close()

            # close the connection object also
            conn.close()
    return record


# def TSelectSql():
#     conn = None
#     record = None
#     try:
#         # create a connection object
#         conn = cx_Oracle.connect(connStr)

#         # get a cursor object from the connection
#         cur = conn.cursor()

#         sql = "select name , location ,grade, cost, weight, logi from vegie"

#         cur.execute(sql)

#         record = cur.fetchall()
#         conn.commit()

#         # do something with the database
#     except Exception as err:
#         print('Error while connecting to the db')
#         print(err)
#     finally:
#         if(conn):
#             # close the cursor object to avoid memory leaks
#             cur.close()

#             # close the connection object also
#             conn.close()
#     return record
