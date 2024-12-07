from modules.department_manager.club_management import *
from modules.department_manager.student_management import *
from modules.department_manager.notice_management import *
from modules.club_manager.activity_management import select_activities, select_activity_detail
from modules.club_manager.budget_management import select_budgets
import os

# 관리자 로그인
def login_department_manager(mydb):
  employee_id = input("직원번호 8자리를 입력해주세요: ").strip()
  cursor = mydb.cursor(dictionary=True)
  query = "SELECT * FROM Department_Manager WHERE Employee_id = %s"
  cursor.execute(query, (employee_id, ))
  department_manager = cursor.fetchone()
  cursor.close()
  
  if department_manager:
    os.system("clear")
    print(f"환영합니다, {department_manager['Ename']}님!")
    return department_manager
  else:
    os.system("clear")
    print("올바르지 않은 직원번호입니다.")
    return None
    
def department_manager_menu(mydb, manager_id):
  """
  학부 관리자 메뉴
  """
  while True:
    print("\n======= 학부 관리자 모드 =======")
    print("1. 동아리 관리")
    print("2. 학생 관리")
    print("3. 공지사항 관리")
    print("0. 종료")
    print("===============================\n")
    
    task = input("원하는 업무를 선택하세요: ").strip()
    
    if task == "1":
      os.system("clear")
      print("============== 동아리 관리 =================")
      print("1. 동아리 생성\t\t\t2. 동아리 목록 조회")
      print("3. 상세 정보 조회\t\t4. 동아리 정보 수정")
      print("5. 동아리 삭제\t\t\t6. 수상 실적 등록")
      print("7. 수상 실적 조회\t\t8. 수상 실적 수정")
      print("9. 수상 실적 삭제\t\t10. 활동 정보 조회")
      print("11. 예산 내역 조회\t\t0. 뒤로가기")
      print("==========================================\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        create_club(mydb)
      elif choice == "2":
        select_all_clubs(mydb)
      elif choice == "3":
        select_club_detail(mydb)
      elif choice == "4":
        update_club_info(mydb)
      elif choice == "5":
        delete_club(mydb)
      elif choice == "6":
        add_award(mydb)
      elif choice == "7":
        select_awards(mydb)
      elif choice == "8":
        update_award(mydb)
      elif choice == "9":
        delete_award(mydb)
      elif choice == "10":
        select_activities(mydb)
      elif choice == "11":
        select_budgets(mydb)
      elif choice == "0":
        # 뒤로가기
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        # 잘못된 접근
        os.system("clear")
        print("잘못된 접근")
    elif task == "2":
      os.system("clear")
      print("============== 학생 관리 =================")
      print("1. 전체 학생 조회\t\t2. 개별 학생 조회")
      print("3. 학생 직책 변경\t\t 4. 학생 정보 등록")
      print("5. 학생 정보 수정\t\t 6. 학생 정보 삭제")
      print("0. 뒤로가기")
      print("==========================================\n")
      
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        select_all_students(mydb)
      elif choice == "2":
        select_student_by_name(mydb)
      elif choice == "3":
        assign_club_manager(mydb, manager_id)
      elif choice == "4":
        create_student(mydb, manager_id)
      elif choice == "5":
        update_student(mydb, manager_id)
      elif choice == "6":
        delete_student(mydb)
      elif choice == "0":
        # 뒤로가기
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        # 잘못된 접근
        os.system("clear")
        print("잘못된 접근")
    elif task == "3":
      os.system("clear")
      print("============== 공지사항 관리 =================")
      print("1. 공지사항 게시\t\t2. 공지사항 조회")
      print("3. 공지사항 상세 조회\t\t4. 공지사항 수정")
      print("5. 공지사항 삭제\t\t0. 뒤로가기")
      print("==========================================\n")
      
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        post_notice(mydb, manager_id)
      elif choice == "2":
        select_notices(mydb)
      elif choice == "3":
        select_notice_detail(mydb)
      elif choice == "4":
        update_notice(mydb, manager_id)
      elif choice == "5":
        delete_notice(mydb, manager_id)
      elif choice == "0":
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        os.system("clear")
        print("잘못된 접근")
    elif task == "0":
      os.system("clear")
      print("관리자 모드에서 로그아웃합니다.\n")
      break
    else:
      os.system("clear")
      print("잘못된 입력입니다. 다시 선택하세요.")
        
