import os

# (동아리장 기능) 신규 부원 등록
def add_member_to_club(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  # 추가할 부원의 학번 입력받기
  student_id = input("추가할 부원의 학번을 입력하세요: ").strip()
  
  # 학생 정보 조회
  query = "SELECT * FROM Student WHERE Student_id = %s"
  cursor.execute(query, (student_id,))
  student = cursor.fetchone()
  
  if not student:
    print("해당 학번의 학생을 찾을 수 없습니다.")
    cursor.close()
    return
  
  # 이미 소속된 동아리인지 확인
  if student['Club_id'] == club_id:
    print(f"해당 학생 (학번: {student['Student_id']}, 이름: {student['Sname']})은 이미 이 동아리에 소속되어 있습니다.")
  elif student['Club_id'] is not None:
    print(f"해당 학생은 이미 다른 동아리 (ID: {student['Club_id']})에 소속되어 있습니다.")
    print("이미 다른 동아리에 소속된 학생은 등록할 수 없습니다.")
  else:
    # 학생의 동아리 소속 변경 및 직책 초기화
    query_update = """
    UPDATE Student
    SET Club_id = %s, Role = '일반학생'
    WHERE Student_id = %s
    """
    cursor.execute(query_update, (club_id, student_id))
    mydb.commit()
    print(f"학생 (학번: {student['Student_id']}, 이름: {student['Sname']})이 성공적으로 동아리 (ID: {club_id})에 등록되었습니다.")
  
  cursor.close()


# (동아리장 기능) 내 동아리 부원 전체 조회 함수 함수
def view_all_members(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  query = """
  SELECT * FROM Student
  WHERE Club_id = %s
  """
  cursor.execute(query, (club_id,))
  members = cursor.fetchall()
  
  # 해당 동아리 이름 조회
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()
  cursor.close()

  if not club:
    print(f"동아리 ID {club_id}는 존재하지 않습니다.")
    return
      
  if members:
    os.system('clear')
    print(f"\n====== {club['Club_Name']} 동아리의 부원 목록 ======")
    for member in members:
      enrollment_status = "재학중" if member["Enrollment_Status"] else "휴학중"
      print(f"학번: {member['Student_id']}, 이름: {member['Sname']}, 학년: {member['Year']}, 연락처: {member['Phone']}, 직책: {member['Role']}, 재학여부: {enrollment_status}")
  else:
    os.system('clear')
    print("해당 동아리에 부원이 없습니다.")

# (동아리장 기능) 특정 부원 정보 조회 함수
def search_member_by_name(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)
  name = input("검색할 부원의 이름을 입력하세요: ").strip()

  # club_id에 필터링해서 이름이 같은 학생 검색 즉, 특정 동아리에 대해서 검색
  query = """
  SELECT * FROM Student
  WHERE Sname LIKE %s AND Club_id = %s
  """
  cursor.execute(query, (f"%{name}%", club_id))
    
  members = cursor.fetchall()
  cursor.close()

  if members:
    os.system('clear')
    print(f"\n====== 이름 '{name}' 검색 결과 ======")
    for member in members:
      enrollment_status = "재학중" if member["Enrollment_Status"] else "휴학중"
      print(f"학번: {member['Student_id']}, 이름: {member['Sname']}, 학년: {member['Year']}, 연락처: {member['Phone']}, 소속 동아리 번호: {member['Club_id']}, 직책: {member['Role']}, 재학여부: {enrollment_status}")
  else:
    os.system('clear')
    print("해당 이름의 부원을 찾을 수 없습니다.")
    
# (동아리장 기능) 특정 부원 정보 수정
def update_member(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)
    
    # 수정할 부원의 학번 입력받기
    student_id = input("수정할 부원의 학번을 입력하세요: ").strip()
    
    # 해당 부원 조회
    query = "SELECT * FROM Student WHERE Student_id = %s AND Club_id = %s"
    cursor.execute(query, (student_id, club_id))
    member = cursor.fetchone()
    
    if not member:
        print("해당 학번의 부원을 찾을 수 없습니다.")
        cursor.close()
        return
    
    # 새로운 정보 입력받기
    new_name = input(f"새 이름 (현재: {member['Sname']}) [변경하지 않으려면 엔터]: ").strip() or member['Sname']
    new_year = input(f"새 학년 (현재: {member['Year']}) [1-4, 변경하지 않으려면 엔터]: ").strip()
    new_year = int(new_year) if new_year.isdigit() and 1 <= int(new_year) <= 4 else member['Year']
    new_phone = input(f"새 연락처 (현재: {member['Phone']}) [변경하지 않으려면 엔터]: ").strip() or member['Phone']
    new_status = input(f"재학 여부 (현재: {'재학중' if member['Enrollment_Status'] else '휴학중'}) [1: 재학중, 0: 휴학중, 변경하지 않으려면 엔터]: ").strip()
    new_status = bool(int(new_status)) if new_status in ['0', '1'] else member['Enrollment_Status']
    
    # 부원 정보 업데이트
    query_update = """
    UPDATE Student
    SET Sname = %s, Year = %s, Phone = %s, Enrollment_Status = %s
    WHERE Student_id = %s AND Club_id = %s
    """
    cursor.execute(query_update, (new_name, new_year, new_phone, new_status, student_id, club_id))
    mydb.commit()
    cursor.close()
    
    print(f"부원 정보가 성공적으로 수정되었습니다. 학번: {student_id}")

# (동아리장 기능) 부원 소속 해제
def remove_member_from_club(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)
    
    # 내보낼 부원의 학번 입력받기
    student_id = input("탈퇴 처리할 부원의 학번을 입력하세요: ").strip()
    
    # 해당 부원 조회
    query = "SELECT * FROM Student WHERE Student_id = %s AND Club_id = %s"
    cursor.execute(query, (student_id, club_id))
    member = cursor.fetchone()
    
    if not member:
        print("해당 학번의 부원을 찾을 수 없습니다.")
        cursor.close()
        return
    
    # 소속 해제 확인
    confirm = input(f"부원 정보 (학번: {member['Student_id']}, 이름: {member['Sname']})를 탈퇴 처리하시겠습니까? (y/n): ").strip().lower()
    if confirm == 'y':
        query_update = "UPDATE Student SET Club_id = NULL WHERE Student_id = %s AND Club_id = %s"
        cursor.execute(query_update, (student_id, club_id))
        mydb.commit()
        print(f"탈퇴 처리되었습니다. 학번: {student_id}")
    else:
        print("부원 탈퇴 처리가 취소되었습니다.")
    
    cursor.close()
