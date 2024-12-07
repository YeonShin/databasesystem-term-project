from config.db_connection import connect_db
from config.db_init import create_database_if_not_exists, use_database, init_database
from modules.department_manager.department_manager import login_department_manager
from modules.club_manager.club_manager import login_club_manager, club_manager_menu
from modules.department_manager.department_manager import department_manager_menu
import os

def main_menu():
  mydb = connect_db()
  if mydb:
    create_database_if_not_exists(mydb)
    use_database(mydb)
    
    init_database(mydb, 'software_club_init.sql')
    
    while True:
      print("========================================")
      print("=== 소프트웨어학부 동아리 관리시스템 ===")
      print("========================================\n")
      print("1. 학부관리자 모드 로그인")
      print("2. 동아리장 모드 로그인")
      print("0. 시스템 종료\n")
      choice = input("로그인할 유형을 선택하세요: ")
      
      if choice == "1":
        department_manager = login_department_manager(mydb)
        if department_manager:  # 관리자 로그인
          department_manager_menu(mydb, department_manager['Employee_id'])
      elif choice == "2":
        club_manager = login_club_manager(mydb)
        if club_manager:  # 동아리장 로그인
          club_manager_menu(mydb, club_manager['Student_id'], club_manager['Club_id'])
      elif choice == "0":
        print("시스템을 종료합니다.")
        return
      else:
        os.system("clear")
        print("잘못된 입력입니다. 다시 선택하세요.")
    

        
if __name__ == "__main__":
  main_menu()