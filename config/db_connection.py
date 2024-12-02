import mysql.connector
from mysql.connector import Error

# 데이터베이스 Network 연결 함수
def connect_db():
  try:
    mydb = mysql.connector.connect(
      host="192.168.56.101",  
      port=4567,
      user="yeonshinkim",
      passwd="1234",
    )
    return mydb
  except Error as e:
    print(f"데이터베이스 연결에 실패했습니다: {e}")
    return None