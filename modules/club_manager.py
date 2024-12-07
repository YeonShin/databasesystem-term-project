import os
from modules.member_management import *
from modules.activity_management import *
from modules.budget_management import *
from modules.notice_management import *

def login_club_manager(mydb):
  student_id = input("학번 10자리를 입력하세요: ").strip()
  cursor = mydb.cursor(dictionary=True)
  query = """
  SELECT S.*, C.Club_Name
  FROM Student S
  JOIN Club C ON S.Club_id = C.Club_id
  WHERE S.Student_id = %s AND S.Role = '동아리장'
  """
  cursor.execute(query, (student_id,))
  club_manager = cursor.fetchone()
  cursor.close()

  if club_manager:
    os.system('clear')
    print(f"환영합니다, {club_manager['Sname']}님! ({club_manager['Club_Name']} 동아리장)")
    return club_manager
  else:
    os.system('clear')
    print("올바르지 않은 학번이거나 동아리장이 아닙니다.")
    return None

def club_manager_menu(mydb, manager_id, club_id):
  # 동아리장 메뉴  
  while True:
    print("\n======= 동아리장 모드 =======")
    print("1. 부원 관리")
    print("2. 동아리 활동 관리")
    print("3. 예산 내역 관리")
    print("4. 학부 공지 사항 확인")
    print("0. 종료")
    print("===============================\n")
    
    task = input("원하는 업무를 선택하세요: ").strip()
    
    if task == "1":
      os.system('clear')
      print("============== 부원 관리 =================")
      print("1. 신규 부원 등록\t\t2. 전체 부원 조회")
      print("3. 개별 부원 조회\t\t4. 부원 정보 수정")
      print("5. 부원 탈퇴 처리")
      print("0. 뒤로가기")
      print("===============================\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 신규 부원 등록 (동아리장이 관리하는 특정 동아리의 부원에 한해)
        add_member_to_club(mydb, club_id)
      elif choice == "2":
        # 전체 부원 조회 (동아리장이 관리하는 특정 동아리의 부원에 한해)
        select_all_members(mydb, club_id)
      elif choice == "3":
        # 개별 부원 조회 (동아리장이 관리하는 특정 동아리의 부원에 한해)
        search_member_by_name(mydb, club_id)
      elif choice == "4":
        # 부원 정보 수정 (동아리장이 관리하는 특정 동아리의 부원에 한해, 직책은 수정 불가)
        update_member(mydb, club_id)
      elif choice == "5":
        # 부원 정보 삭제 (동아리장이 관리하는 특정 동아리의 부원에 한해, 삭제하면 부원이 속한 동아리가 NULL)
        remove_member_from_club(mydb, club_id)
      elif choice == "0":
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        os.system("clear")
        print("잘못된 접근")
    elif task == "2":
      os.system('clear')
      print("============== 동아리 활동 관리 =================")
      print("1. 신규 활동 등록\t\t2. 활동 목록 조회")
      print("3. 활동 상세 조회\t\t4. 활동 정보 수정")
      print("5. 활동 정보 삭제\t\t0. 뒤로가기")
      print("===============================\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 신규 활동 등록
        create_activity(mydb, club_id)
      elif choice == "2":
        # 전체 활동 조회
        select_activities(mydb, club_id)
      elif choice == "3":
        # 전체 활동 조회
        select_activity_detail(mydb, club_id)
      elif choice == "4":
        # 개별 활동 조회
        update_activity(mydb, club_id)
      elif choice == "5":
        # 활동 내용 
        delete_activity(mydb, club_id)
      elif choice == "0":
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        os.system("clear")
        print("잘못된 접근")
    elif task == "3":
      os.system('clear')
      print("============== 예산 내역 관리 =================")
      print("1. 예산내역 등록\t\t2. 예산내역 조회")
      print("3. 예산내역 수정\t\t4. 예산내역 삭제")
      print("0. 뒤로가기")
      print("===============================\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        create_budget(mydb, club_id)
      elif choice == "2":
        select_budgets(mydb, club_id)
      elif choice == "3":
        update_budget(mydb, club_id)
      elif choice == "4":
        delete_budget(mydb, club_id)
      elif choice == "0":
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        os.system("clear")
        print("잘못된 접근")
    elif task == "4":
      os.system('clear')
      print("============== 학부 공지사항 확인 =================")
      print("1. 공지사항 목록 조회\t\t2. 공지사항 상세 조회")
      print("0. 뒤로가기")
      print("===============================\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        select_notices(mydb)
      elif choice == "2":
        select_notice_detail(mydb)
      elif choice == "0":
        os.system("clear")
        print("이전으로 돌아갑니다.")
        continue
      else:
        os.system("clear")
        print("잘못된 접근")
    elif task == "0":
      os.system("clear")
      print("동아리장 모드에서 로그아웃합니다.\n")
      break
    else:
      os.system("clear")
      print("잘못된 입력입니다. 다시 선택하세요.\n")
        
