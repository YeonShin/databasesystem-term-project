from modules.club_management import *
from modules.member_management import *
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
    return True
  else:
    os.system("clear")
    print("올바르지 않은 직원번호입니다.")
    return False
    
def department_manager_menu(mydb):
  """
  학부 관리자 메뉴
  """
  while True:
    print("\n======= 학부 관리자 모드 =======")
    print("1. 동아리 관리")
    print("2. 부원 관리")
    print("3. 공지사항 관리")
    print("0. 종료\n")
    
    task = input("원하는 업무를 선택하세요: ").strip()
    
    if task == "1":
      os.system("clear")
      print("============== 동아리 관리 =================")
      print("1. 동아리 개설\t\t\t2. 전체 동아리 조회")
      print("3. 기본 정보 수정\t\t4. 동아리 삭제")
      print("5. 수상 실적 등록\t\t6. 수상 실적 조회")
      print("7. 수상 실적 수정\t\t8. 수상 실적 삭제")
      print("9. 활동 정보 조회\t\t10. 예산 내역 조회")
      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 동아리 개설
        create_club(mydb)
      elif choice == "2":
        select_all_clubs(mydb)
      elif choice == "3":
        update_club_info(mydb)
      elif choice == "4":
        delete_club(mydb)
      elif choice == "5":
        add_award(mydb)
      elif choice == "6":
        select_awards(mydb)
      elif choice == "7":
        update_award(mydb)
      elif choice == "8":
        delete_award(mydb)
      # elif choice == "9":
      #   # 활동 정보 조회
      # elif choice == "10":
      #   # 예산 내역 조회
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
      print("============== 부원 관리 =================")
      print("1. 전체 부원 조회\t\t2. 개별 부원 조회\n")
      print("3. 부원 직책 변경\n")
      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        view_all_members(mydb)
      elif choice == "2":
        search_member_by_name(mydb)
      elif choice == "3":
        assign_club_manager(mydb)
      elif choice == "0":
        # 뒤로가기
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        # 잘못된 접근
        os.system("clear")
        print("잘못된 접근")
    # elif task == "3":
    #   print("\n==================================")
    #   print("1. 공지사항 게시\t\t2. 공지사항 조회\n")
    #   print("3. 공지사항 수정\t\t4. 공지사항 삭제\n")
    #   print("0. 뒤로가기\n")
    #   choice = input("수행하고자하는 작업을 선택하세요: ").strip()
    #   if choice == "1":
    #     # 공지사항 게시
    #   elif choice == "2":
    #     # 공지사항 조회
    #   elif choice == "3":
    #     # 공지사항 수정
    #   elif choice == "4":
    #     # 공지사항 삭제
    #   elif choice == "0":
    #     # 뒤로가기
    #     continue
    #   else:
    #     # 잘못된 접근
    elif task == "0":
      os.system("clear")
      print("관리자 모드에서 로그아웃합니다.")
      break
    else:
      print("잘못된 입력입니다. 다시 선택하세요.")
        
