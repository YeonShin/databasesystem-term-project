import os

# 동아리 부원 전체 조회 함수
def view_all_members(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("부원을 조회할 동아리의 ID를 입력하세요: ").strip()

  query = """
  SELECT * FROM Student
  WHERE Club_id = %s
  """
  cursor.execute(query, (club_id,))
  members = cursor.fetchall()
  cursor.close()

  if members:
    os.system('clear')
    print(f"\n====== 동아리 ID {club_id}의 부원 목록 ======")
    for member in members:
      print(f"학번: {member['Student_id']}, 이름: {member['Sname']}, 학년: {member['Year']}, 직책: {member['Role']}")
  else:
    os.system('clear')
    print("해당 동아리에 부원이 없습니다.")

# 특정 부원 정보 조회
def search_member_by_name(mydb):
  cursor = mydb.cursor(dictionary=True)
  name = input("검색할 부원의 이름을 입력하세요: ").strip()

  query = """
  SELECT * FROM Student
  WHERE Sname LIKE %s
  """
  cursor.execute(query, (f"%{name}%",))
  members = cursor.fetchall()
  cursor.close()

  if members:
    os.system('clear')
    print(f"\n====== 이름 '{name}' 검색 결과 ======")
    for member in members:
      print(f"학번: {member['Student_id']}, 이름: {member['Sname']}, 동아리 ID: {member['Club_id']}, 직책: {member['Role']}")
  else:
    os.system('clear')
    print("해당 이름의 부원을 찾을 수 없습니다.")

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
    UPDATE Student SET Role = '일반부원'
    WHERE Student_id = %s AND Club_id = %s
    """
    cursor.execute(query, (current_manager['Student_id'], club_id))

  # 새로운 동아리장을 지정
  query = """
  UPDATE Student SET Role = '동아리장'
  WHERE Student_id = %s AND Club_id = %s
  """
  cursor.execute(query, (new_student_id, club_id))
  mydb.commit()
  
  os.system('clear')
  print(f"학번 {new_student_id}가 동아리 ID {club_id}의 새로운 동아리장으로 지정되었습니다.")
  cursor.close()
