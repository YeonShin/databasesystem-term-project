import mysql.connector
from mysql.connector import Error

# 데이터베이스가 없다면 생성
def create_database_if_not_exists(mydb):
  try:
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS software_club")
    mydb.commit()
    cursor.close()
  except Error as e:
    print(f"데이터베이스 생성 중 오류 발생: {e}")

# 데이터베이스 사용 함수
def use_database(mydb):
  try:
    cursor = mydb.cursor()
    cursor.execute("USE software_club")
    cursor.close()
  except Error as e:
    print(f"데이터베이스 사용 중 오류 발생: {e}")

# 초기 테이블 구성
def init_database(mydb, file_path):
  cursor = mydb.cursor()

  # 데이터베이스에 테이블 존재 여부 확인
  query = """
  SELECT COUNT(*) 
  FROM INFORMATION_SCHEMA.TABLES 
  WHERE TABLE_SCHEMA = DATABASE()
  """
  cursor.execute(query)
  result = cursor.fetchone()

  # 데이터베이스에 테이블이 하나라도 존재하면 SQL 파일 실행하지 않음
  if result[0] > 0:
      cursor.close()
      return

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
  except Error as e:
    print(f"SQL 파일 실행 중 오류 발생: {e}")