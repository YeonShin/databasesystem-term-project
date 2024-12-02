from config.db_connection import connect_db
from config.db_init import create_database_if_not_exists, use_database, init_database
import os

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