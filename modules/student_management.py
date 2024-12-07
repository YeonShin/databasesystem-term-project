import os

# (학부 관리자 기능) 전체 학생 목록 조회 함수
def select_all_students(mydb):
  cursor = mydb.cursor(dictionary=True)
  
  query = """
  SELECT s.Student_id, s.Sname, s.Year, s.Phone, s.Role, s.Enrollment_Status, 
          s.Club_id, d.Ename AS Dmanager_Name
  FROM Student s
  INNER JOIN Department_Manager d ON s.Dmanager_id = d.Employee_id
  """
  cursor.execute(query)
  students = cursor.fetchall()
  cursor.close()
  
  if students:
    os.system('clear')
    print(f"\n====== 소프트웨어학부 학생 목록 ======")
    for student in students:
      enrollment_status = "재학중" if student["Enrollment_Status"] else "휴학중"
      print(f"학번: {student['Student_id']}, 이름: {student['Sname']}, 학년: {student['Year']}, "
            f"연락처: {student['Phone']}, 소속 동아리 번호: {student['Club_id']}, 직책: {student['Role']}, "
            f"재학여부: {enrollment_status}, 최근 수정자: {student['Dmanager_Name']}")
  else:
    os.system('clear')
    print("등록된 학생 정보가 없습니다.")

# (학부 관리자 기능) 특정 이름의 학생 정보 조회 함수
def select_student_by_name(mydb):
  cursor = mydb.cursor(dictionary=True)
  name = input("검색할 학생의 이름을 입력하세요: ").strip()

  # club_id에 필터링해서 이름이 같은 학생 검색 즉, 특정 동아리에 대해서 검색
  query = """
  SELECT s.Student_id, s.Sname, s.Year, s.Phone, s.Role, s.Enrollment_Status, 
          s.Club_id, d.Ename AS Dmanager_Name
  FROM Student s
  INNER JOIN Department_Manager d ON s.Dmanager_id = d.Employee_id
  WHERE s.Sname LIKE %s
  """
  cursor.execute(query, (f"%{name}%", ))
    
  students = cursor.fetchall()
  cursor.close()

  if students:
    os.system('clear')
    print(f"\n====== 이름 '{name}' 검색 결과 ======")
    for student in students:
      enrollment_status = "재학중" if student['Enrollment_Status'] else "휴학중"
      print(
          f"학번: {student['Student_id']}, 이름: {student['Sname']}, 학년: {student['Year']}, "
          f"연락처: {student['Phone']}, 소속 동아리 번호: {student['Club_id']}, 직책: {student['Role']}, "
          f"재학여부: {enrollment_status}, 최근 수정자: {student['Dmanager_Name']}"
        )
  else:
    os.system('clear')
    print("해당 이름의 학생을 찾을 수 없습니다.")
    
# (학부 관리자 기능) 학생 정보 등록 함수
def create_student(mydb, dmanager_id):
  cursor = mydb.cursor(dictionary=True)
  
  # 올해의 연도를 가져옴
  from datetime import datetime
  current_year = datetime.now().year

  # 가장 최근 학번 조회 (해당 연도 기준)
  query_get_last_student = f"""
  SELECT MAX(Student_id) AS Last_Student_Id 
  FROM Student 
  WHERE Student_id LIKE '{current_year}03%'
  """
  cursor.execute(query_get_last_student)
  result = cursor.fetchone()
  
  # 학번 생성 (현재 연도 + 039 + 번호)
  if result['Last_Student_Id']:
    last_id = int(result['Last_Student_Id'][-3:])  # 마지막 세 자리 번호 추출
    new_id = f"{current_year}039{last_id + 1:03}"   # 새 학번 생성
  else:
    new_id = f"{current_year}039001"  # 첫 학번 생성
  
  # 학생 정보 입력 받기
  sname = input("학생 이름을 입력하세요: ").strip()
  
  # 학년 입력받기 (유효한 정수만 허용)
  while True:
    try:
      year = int(input("학생 학년을 입력하세요 (1~4): ").strip())
      if year < 1 or year > 4:
        print("학년은 1부터 4 사이의 값을 입력해야 합니다.")
      else:
        break
    except ValueError:
      print("유효한 숫자를 입력해주세요.")
  
  # 전화번호 입력받기 및 검증
  phone = input("학생 전화번호를 입력하세요 (형식: 010-0000-0000): ").strip()
  import re
  phone_pattern = re.compile(r"^010-\d{4}-\d{4}$")
  if not phone_pattern.match(phone):
    print("전화번호 형식이 잘못되었습니다. 다시 시도해주세요.")
    cursor.close()
    return
  
  # 소속 동아리 입력받기
  club_id = input("소속 동아리 ID를 입력하세요 (없으면 엔터): ").strip()
  if club_id:
    # 입력된 Club_id가 유효한지 확인
    query_check_club = "SELECT Club_id FROM Club WHERE Club_id = %s"
    cursor.execute(query_check_club, (club_id,))
    club_result = cursor.fetchone()
    if not club_result:
      print("입력한 동아리가 존재하지 않아 'NULL'로 설정됩니다.")
      club_id = None
  else:
    club_id = None

  # 기본값 설정
  department = "소프트웨어학부"
  role = "일반학생"
  enrollment_status = True

  # INSERT 쿼리 실행
  query_insert_student = """
  INSERT INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id, Dmanager_id)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
  """
  cursor.execute(query_insert_student, (new_id, sname, department, year, phone, role, enrollment_status, club_id, dmanager_id))
  mydb.commit()
  cursor.close()

  print(f"학생 등록이 완료되었습니다. 학번: {new_id}, 이름: {sname}, 학부: {department}, 학년: {year}, 전화번호: {phone}, 소속 동아리: {club_id if club_id else '없음'}")

# (학부 관리자 기능) 학생 정보 수정
def update_student(mydb, dmanager_id):
  cursor = mydb.cursor(dictionary=True)
  
  # 수정할 학생의 학번 입력받기
  student_id = input("수정할 학생의 학번을 입력하세요: ").strip()
  
  # 해당 학생 조회
  query = "SELECT * FROM Student WHERE Student_id = %s"
  cursor.execute(query, (student_id,))
  student = cursor.fetchone()
  
  if not student:
    print("해당 학번의 학생을 찾을 수 없습니다.")
    cursor.close()
    return
  
  # 새로운 정보 입력받기
  new_name = input(f"새 이름 (현재: {student['Sname']}) [변경하지 않으려면 엔터]: ").strip() or student['Sname']
  new_year = input(f"새 학년 (현재: {student['Year']}) [1-4, 변경하지 않으려면 엔터]: ").strip()
  new_year = int(new_year) if new_year.isdigit() and 1 <= int(new_year) <= 4 else student['Year']
  new_phone = input(f"새 연락처 (현재: {student['Phone']}) [변경하지 않으려면 엔터]: ").strip() or student['Phone']
  new_status = input(f"재학 여부 (현재: {'재학중' if student['Enrollment_Status'] else '휴학중'}) [1: 재학중, 0: 휴학중, 변경하지 않으려면 엔터]: ").strip()
  new_status = bool(int(new_status)) if new_status in ['0', '1'] else student['Enrollment_Status']
  new_club_id = input(f"새 소속 동아리 번호 (현재: {student['Club_id']}) [변경하지 않으려면 엔터]: ").strip()
  if new_club_id:
    # 동아리 유효성 확인
    query_check_club = "SELECT Club_id FROM Club WHERE Club_id = %s"
    cursor.execute(query_check_club, (new_club_id,))
    if not cursor.fetchone():
      print("입력한 동아리가 존재하지 않아 'NULL'로 설정됩니다.")
      new_club_id = None
    # 학생 정보 업데이트
    query_update = """
    UPDATE Student
    SET Sname = %s, Year = %s, Phone = %s, Enrollment_Status = %s, Club_id = %s, Dmanager_id = %s, Role = '일반학생'
    WHERE Student_id = %s
    """
  else:
    new_club_id = student['Club_id']
    # 학생 정보 업데이트
    query_update = """
    UPDATE Student
    SET Sname = %s, Year = %s, Phone = %s, Enrollment_Status = %s, Club_id = %s, Dmanager_id = %s
    WHERE Student_id = %s
    """

  cursor.execute(query_update, (new_name, new_year, new_phone, new_status, new_club_id, dmanager_id, student_id))
  mydb.commit()
  cursor.close()
  
  print(f"학생 정보가 성공적으로 수정되었습니다. 학번: {student_id}")


# (학부 관리자 기능) 학생 정보 삭제
def delete_student(mydb):
  cursor = mydb.cursor(dictionary=True)
  
  # 삭제할 학생의 학번 입력받기
  student_id = input("삭제할 학생의 학번을 입력하세요: ").strip()
  
  # 해당 학생 조회
  query = "SELECT * FROM Student WHERE Student_id = %s"
  cursor.execute(query, (student_id,))
  student = cursor.fetchone()
  
  if not student:
      print("해당 학번의 학생을 찾을 수 없습니다.")
      cursor.close()
      return
  
  # 삭제 확인
  confirm = input(f"학생 정보 (학번: {student['Student_id']}, 이름: {student['Sname']})를 삭제하시겠습니까? (y/n): ").strip().lower()
  if confirm == 'y':
      query_delete = "DELETE FROM Student WHERE Student_id = %s"
      cursor.execute(query_delete, (student_id,))
      mydb.commit()
      print(f"학생 정보가 성공적으로 삭제되었습니다. 학번: {student_id}")
  else:
      print("삭제 작업이 취소되었습니다.")
  
  cursor.close()

# 동아리장 지정 기능 (학부관리자 기능)
def assign_club_manager(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("동아리 고유번호를 입력하세요: ").strip()
  
  # 현재 동아리장 확인
  query = """
  SELECT Student_id, Sname FROM Student 
  WHERE Club_id = %s AND Role = '동아리장'
  """
  cursor.execute(query, (club_id,))
  current_manager = cursor.fetchone()

  os.system('clear')
  if current_manager:
    print(f"현재 동아리장: {current_manager['Sname']} (학번: {current_manager['Student_id']})")
    print("동아리장을 변경합니다.")
  else:
    print("현재 동아리장이 없습니다. 새로운 동아리장을 바로 지정합니다.")
  
  new_student_id = input("새로운 동아리장으로 지정할 학생의 학번을 입력하세요: ").strip()

  # 입력한 학번이 해당 동아리에 소속된 학생인지 확인
  query = """
  SELECT Student_id, Sname FROM Student
  WHERE Student_id = %s AND Club_id = %s
  """
  cursor.execute(query, (new_student_id, club_id))
  student = cursor.fetchone()

  if not student:
    print(f"학번 {new_student_id}는 동아리 ID {club_id}에 소속되지 않은 학생입니다.")
    cursor.close()
    return

  # 기존 동아리장의 직책을 일반 부원으로 변경 (있는 경우)
  if current_manager:
    query = """
    UPDATE Student SET Role = '일반학생'
    WHERE Student_id = %s AND Club_id = %s
    """
    cursor.execute(query, (current_manager['Student_id'], club_id))

  # 새로운 동아리장을 지정
  query = """
  UPDATE Student SET Role = '동아리장'
  WHERE Student_id = %s AND Club_id = %s
  """
  cursor.execute(query, (new_student_id, club_id))
  
  query = """
  SELECT Sname FROM Student WHERE Student_id = %s
  """
  cursor.execute(query, (new_student_id, ))
  new_student = cursor.fetchone()
  
  mydb.commit()
  
  os.system('clear')
  print(f"학번 {new_student_id}({new_student['Sname']})가 동아리 ID {club_id}의 새로운 동아리장으로 지정되었습니다.")
  cursor.close()
