
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
      print(f"환영합니다, {club_manager['Sname']}님! ({club_manager['Club_Name']} 동아리장)")
      # 해당 동아리 관리 기능 호출
  else:
      print("올바르지 않은 학번이거나 동아리장이 아닙니다.")

def club_manager_menu(mydb):
  # 동아리장 메뉴  
  while True:
    print("\n========== 동아리장 모드 ==========")
    print("1. 부원 관리\n")
    print("2. 동아리 활동 관리\n")
    print("3. 예산 내역 관리\n")
    print("4. 공지 사항 확인\n")
    print("0. 종료")
    
    task = input("원하는 업무를 선택하세요: ").strip()
    
    if task == "1":
      print("\n==================================")
      print("1. 신규 부원 등록\t\t2. 전체 부원 조회\n")
      print("3. 개별 부원 조회\t\t4. 부원 정보 수정\n")
      print("5. 부원 정보 삭제\n")
      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 신규 부원 등록 (동아리장이 관리하는 특정 동아리의 부원에 한해)
      elif choice == "2":
        # 전체 부원 조회 (동아리장이 관리하는 특정 동아리의 부원에 한해)
      elif choice == "3":
        # 개별 부원 조회 (동아리장이 관리하는 특정 동아리의 부원에 한해)
      elif choice == "4":
        # 부원 정보 수정 (동아리장이 관리하는 특정 동아리의 부원에 한해, 직책은 수정 불가)
      elif choice == "5":
        # 부원 정보 삭제 (동아리장이 관리하는 특정 동아리의 부원에 한해, 삭제하면 부원이 속한 동아리가 NULL)
      elif choice == "0":
        # 뒤로가기
        continue
      else:
        # 잘못된 접근
    elif task == "2":
      print("\n==================================")
      print("1. 신규 활동 등록\t\t2. 활동 정보 조회\n")
      print("3. 활동 정보 수정\t\t4. 활동 정보 삭제\n")

      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 신규 활동 등록
      elif choice == "2":
        # 전체 활동 조회
      elif choice == "3":
        # 개별 활동 조회
      elif choice == "4":
        # 활동 내용 수정
      elif choice == "0":
        # 뒤로가기
        continue
      else:
        # 잘못된 접근
    elif task == "3":
      print("\n==================================")
      print("1. 예산내역 등록\t\t2. 예산내역 조회\n")
      print("3. 예산내역 수정\t\t4. 예산내역 삭제\n")
      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 신규 예산내역 등록
      elif choice == "2":
        # 예산내역 조회
      elif choice == "3":
        # 예산내역 수정
      elif choice == "4":
        # 예산내역 삭제
      elif choice == "0":
        # 뒤로가기
        continue
      else:
        # 잘못된 접근
    elif task == "4":
      print("\n==================================")
      print("1. 공지사항 목록 조회\t\t2. 공지사항 상세 조회\n")
      print("0. 뒤로가기\n")
      choice = input("수행하고자하는 작업을 선택하세요: ").strip()
      if choice == "1":
        # 공지사항 목록 조회
      elif choice == "2":
        # 공지사항 상세 조회
      elif choice == "0":
        # 뒤로가기
        continue
      else:
        # 잘못된 접근
    elif task == "0":
      print("관리자 모드에서 로그아웃합니다.")
      break
    else:
      print("잘못된 입력입니다. 다시 선택하세요.")
        
