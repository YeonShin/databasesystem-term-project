import mysql.connector
from mysql.connector import Error

def create_database_if_not_exists(mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS software_club")
        mydb.commit()
        cursor.close()
    except Error as e:
        print(f"데이터베이스 생성 중 오류 발생: {e}")
        
def use_database(mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute("USE software_club")
        cursor.close()
        print("software_club 데이터베이스를 사용합니다.")
    except Error as e:
        print(f"데이터베이스 사용 중 오류 발생: {e}")

def init_database(mydb, file_path):
  try:
    cursor = mydb.cursor()
    with open(file_path, 'r') as sql_file:
      sql_script = sql_file.read()
      commands = sql_script.split(';')  # SQL 명령어를 ';'로 분리
      for command in commands:
        if command.strip():  # 빈 명령어 무시
          cursor.execute(command.strip())
      mydb.commit()
    cursor.close()
    print(f"{file_path} 파일이 성공적으로 실행되었습니다.")
  except Error as e:
    print(f"SQL 파일 실행 중 오류 발생: {e}")