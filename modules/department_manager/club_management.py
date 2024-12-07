import os

# (학부 관리자 기능) 신규 동아리 생성 함수
def create_club(mydb):
  try:
    cursor = mydb.cursor(dictionary=True)
    name = input("동아리 이름을 입력하세요: ").strip()
    professor = input("지도교수 이름을 입력하세요: ").strip()
    location = input("동아리실 위치를 입력하세요: ").strip()
    introduction = input("동아리 소개를 입력하세요(20자 이내): ").strip()
    main_research = input("주요 연구 분야를 입력하세요: ").strip()
    
    # 초기 동아리장 설정
    student_id = input("초기 동아리장의 학번을 입력하세요: ").strip()
    
    # 학생 존재 여부 및 소속 확인
    query_student = """
    SELECT Student_id, Club_id FROM Student WHERE Student_id = %s
    """
    cursor.execute(query_student, (student_id,))
    student = cursor.fetchone()
    
    if not student:
      print(f"학번 {student_id}에 해당하는 학생을 찾을 수 없습니다.")
      cursor.close()
      return

    if student["Club_id"] is not None:
      print(f"학생 (학번: {student_id})은 이미 다른 동아리에 소속되어 있습니다.")
      cursor.close()
      return

    query = """
    INSERT INTO Club (Club_Name, Professor, Location, Introduction, Main_Research)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, professor, location, introduction, main_research))
    club_id = cursor.lastrowid 
    
    # 초기 동아리장 설정
    query_update_student = """
    UPDATE Student
    SET Club_id = %s, Role = '동아리장'
    WHERE Student_id = %s
    """
    cursor.execute(query_update_student, (club_id, student_id))
    mydb.commit()
    
    
    mydb.commit()
    os.system("clear")
    print(f"신규 동아리 '{name}'가 성공적으로 생성되었습니다.")
    cursor.close()
  except Exception as e:
    os.system('clear')
    print(f"오류 발생: {str(e)}")

# (학부 관리자 기능) 동아리 삭제 함수
def delete_club(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("삭제할 동아리의 고유번호를 입력하세요: ").strip()
  
  # 삭제 전에 해당 동아리 이름 조회
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()

  if not club:
    os.system("clear")
    print(f"존재하지 않는 동아리 ID {club_id} 입니다.")
    cursor.close()
    return
  club_name = club['Club_Name']
  
  # 삭제 확인
  confirm = input(f"{club_name} 동아리 (ID {club_id})를 삭제하시겠습니까? (y/n): ").strip().lower()
  if confirm == 'y':
    query_delete = """
    DELETE FROM Club WHERE Club_id = %s
    """
    cursor.execute(query_delete, (club_id, ))
    mydb.commit()
    os.system("clear")
    print(f"{club_name}동아리 (ID: {club_id})가 성공적으로 삭제되었습니다.")
    
  else:
    os.system("clear")
    print("동아리 삭제가 취소되었습니다.")
    
  cursor.close()


# (학부 관리자 기능) 동아리 정보 수정
def update_club_info(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("정보를 수정할 동아리 ID를 입력하세요: ").strip()
    
    # 삭제 전에 해당 동아리 이름 조회
    query = "SELECT * FROM Club WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    club = cursor.fetchone()
    
    if not club:
      os.system("clear")
      print(f"존재하지 않는 동아리 ID {club_id} 입니다.")
      cursor.close()
      return
    
    club_name = club['Club_Name']

    try:
      new_name = input(f"새 이름 (현재: {club['Club_Name']}) [변경하지 않으려면 엔터]: ").strip() or club['Club_Name']
      new_professor = input(f"새 지도교수 (현재: {club['Professor']}) [변경하지 않으려면 엔터]: ").strip() or club['Professor']
      new_location = input(f"새 동아리실 (현재: {club['Location']}) [변경하지 않으려면 엔터]: ").strip() or club['Location']
      new_introduction = input(f"새 소개 (현재: {club['Introduction']}) [변경하지 않으려면 엔터]: ").strip() or club['Introduction']
      new_main_research = input(f"새 연구분야 (현재: {club['Main_Research']}) [변경하지 않으려면 엔터]: ").strip() or club['Main_Research']

      query = """
      UPDATE Club
      SET Club_Name = %s, Professor = %s, Location = %s, Introduction = %s, Main_Research = %s
      WHERE Club_id = %s
      """
      cursor.execute(query, (new_name, new_professor, new_location, new_introduction, new_main_research, club_id))
      mydb.commit()
      cursor.close()
      os.system("clear")
      print(f"{club_name} 동아리 (ID {club_id})의 정보가 성공적으로 수정되었습니다.")
    except Exception as e:
      os.system('clear')
      print(f"오류 발생: {str(e)}")

# (학부 관리자 기능) 전체 동아리 조회
def select_all_clubs(mydb):
  cursor = mydb.cursor(dictionary=True)
  query = """
  SELECT 
      Club.Club_id, Club.Club_Name, Club.Professor, Club.Location, 
      Student.Sname AS Manager_Name, Student.Student_id AS Manager_Id
  FROM Club
  LEFT JOIN Student 
  ON Club.Club_id = Student.Club_id AND Student.Role = '동아리장'
  """
  cursor.execute(query)
  clubs = cursor.fetchall()
  cursor.close()

  if clubs:
    os.system("clear")
    print("\n=================== 동아리 목록 =====================")
    for club in clubs:
      manager_info = f"동아리장: {club['Manager_Name']} (학번: {club['Manager_Id']})" if club['Manager_Name'] else "미정"
      print(
        f"ID: {club['Club_id']}, 이름: {club['Club_Name']}, "
        f"지도교수: {club['Professor']}, 위치: {club['Location']}, "
        f"동아리장: {manager_info}"
      )
    print("=====================================================")
  else:
    os.system('clear')
    print("등록된 동아리가 없습니다.")
    
# (학부 관리자 기능) 동아리 상세 조회
def select_club_detail(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("상세 조회할 동아리 ID를 입력하세요: ").strip()
  
  query = "SELECT * FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id, ))
  club = cursor.fetchone()
  
  if not club:
    os.system("clear")
    print("등록된 동아리가 없습니다.")
    cursor.close()
    return
      
  query_member_count = """
  SELECT COUNT(*) AS Member_Count 
  FROM Student 
  WHERE Club_id = %s
  """
  cursor.execute(query_member_count, (club_id,))
  member_count = cursor.fetchone()["Member_Count"]
  
  cursor.close()

  os.system("clear")
  print("\n=================== 동아리 상세 정보 =====================")
  print(f"ID: {club['Club_id']}, 이름: {club['Club_Name']}, 지도교수: {club['Professor']}, 위치: {club['Location']}")
  print(f"동아리 소개: {club['Introduction']}")
  print(f"연구주제: {club['Main_Research']}")
  print(f"부원의 수: {member_count}명")
  print("=====================================================")
    
# (학부 관리자 기능) 수상 실적 등록 함수
def add_award(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("수상 실적을 등록할 동아리 ID를 입력하세요: ").strip()
  
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()
  
  if club is None:
    os.system("clear")
    print(f"동아리 ID {club_id}가 존재하지 않습니다.")
    return
  
  award = input("추가할 수상 실적(30자 이내)를 입력하세요: ").strip()

  try:
    query = """
    INSERT INTO Club_Awards (Club_id, Award_Detail)
    VALUES (%s, %s)
    """
    cursor.execute(query, (club_id, award))
    mydb.commit()

    if club:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리에 수상 실적 '{award}'가 등록되었습니다.")
    else:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리 (ID {club_id})가 존재하지 않습니다.")
    cursor.close()
  except Exception as e:
      os.system('clear')
      print(f"오류 발생: {str(e)}")

# (학부 관리자 기능) 수상 실적 조회 함수
def select_awards(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("수상 실적을 조회할 동아리 ID를 입력하세요: ").strip()
    
    query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    club = cursor.fetchone()
    
    if club is None:
      os.system("clear")
      print(f"동아리 ID {club_id}가 존재하지 않습니다.")
      return

    query = "SELECT Award_id, Award_Detail FROM Club_Awards WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    awards = cursor.fetchall()
    
    cursor.close()
    

    if awards:
      os.system("clear")
      print(f"\n============= {club['Club_Name']} 동아리의 수상 실적 목록 =============")
      for idx, award in enumerate(awards, 1):
        print(f"{idx}. ID: {award['Award_id']}, 실적내용: {award['Award_Detail']}")
    else:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리에 등록된 수상 실적이 없습니다.")

# (학부 관리자 기능) 수상 실적 수정 함수
def update_award(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("수상 실적을 수정할 동아리 ID를 입력하세요: ").strip()
    
    query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    club = cursor.fetchone()
    
    if club is None:
      os.system("clear")
      print(f"동아리 ID {club_id}가 존재하지 않습니다.")
      cursor.close()
      return
    
    award_id = input("수정할 기존 실적의 ID를 입력하세요: ").strip()
    
    # 수상 실적 존재 여부 확인
    query = "SELECT * FROM Club_Awards WHERE Club_id = %s AND Award_id = %s"
    cursor.execute(query, (club_id, award_id))
    award = cursor.fetchone()
    
    if award is None:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리에 수상 실적 ID {award_id}가 존재하지 않습니다.")
      cursor.close()
      return
    
    new_award = input("새로운 수상 실적을 입력하세요 [변경하지 않으려면 엔터]: ").strip() or award['Award_Detail']

    query = """
    UPDATE Club_Awards SET Award_Detail = %s
    WHERE Club_id = %s AND Award_id = %s
    """
    cursor.execute(query, (new_award, club_id, award_id))
    mydb.commit()
  
    os.system("clear")
    print(f" {club['Club_Name']} 동아리의 수상 실적 (ID: {award_id})가 '{new_award}'로 수정되었습니다.")
    cursor.close()

# (학부 관리자 기능) 수상 실적 삭제 함수
def delete_award(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("수상 실적을 삭제할 동아리 ID를 입력하세요: ").strip()
    award_id = input("삭제할 수상 실적의 ID를 입력하세요: ").strip()
    
    query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    club = cursor.fetchone()
    
    if club is None:
      os.system("clear")
      print(f"동아리 ID {club_id}가 존재하지 않습니다.")
      cursor.close()
      return
    
    # 수상 실적 존재 여부 확인
    query = "SELECT * FROM Club_Awards WHERE Club_id = %s AND Award_id = %s"
    cursor.execute(query, (club_id, award_id))
    award = cursor.fetchone()
    
    if award is None:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리에 수상 실적 ID {award_id}가 존재하지 않습니다.")
      cursor.close()
      return
    
    confirm = input(f"실적 정보 (실적 번호: {award_id})를 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm == 'y':
        query = "DELETE FROM Club_Awards WHERE Club_id = %s AND Award_id = %s"
        cursor.execute(query, (club_id, award_id))
        mydb.commit()
        os.system("clear")
        print(f"{club['Club_Name']} 동아리의 수상 실적 (ID: {award_id}) 이(가) 삭제되었습니다.")
    else:
        print("실적 삭제가 취소되었습니다.")
    cursor.close()
