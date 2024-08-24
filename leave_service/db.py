import mysql.connector
def connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tuan0843055059#",
        database="leave_service"
    )