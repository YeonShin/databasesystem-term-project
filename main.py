import mysql.connector
from mysql.connector import Error
import os

def connect_db():
  try:
    mydb = mysql.connector.connect(
      host="192.168.56.101",  
      port=4567,
      user="yeonshinkim",
      passwd="1234",
    )
    if mydb.is_connected():
      print("MySQL 데이터베이스에 성공적으로 연결되었습니다!")
    return mydb
  except Error as e:
    print(f"데이터베이스 연결에 실패했습니다: {e}")
    return None
  
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
    
def main_menu():
  print("==============================================\n")
  print("====== 소프트웨어학부 학부 동아리 관리시스템 ======\n")
  print("==============================================\n")
  
  mydb = connect_db()
  if mydb:
    create_database_if_not_exists(mydb)
    use_database(mydb)
    
    init_database(mydb, 'software_club_init.sql')
    
    while True:
      print("1. 관리자 모드 로그인")
      print("2. 동아리장 모드 로그인")
      print("0. 종료")
      choice = input("로그인할 유형을 선택하세요: ")
      
      if choice == "1":
        # 관리자 모드 로그인 처리
        print("관리자 모드 선택")
        # 로그인 및 관리자 기능 호출
      elif choice == "2":
        # 동아리장 모드 로그인 처리
        print("동아리장 모드 선택")
        # 로그인 및 동아리장 기능 호출
      elif choice == "0":
        print("프로그램을 종료합니다.")
        break
      else:
        print("잘못된 입력입니다. 다시 선택하세요.")
        
if __name__ == "__main__":
  main_menu()