import os

# 신규 동아리 생성 함수
def create_club(mydb):
  cursor = mydb.cursor()
  name = input("동아리 이름을 입력하세요: ").strip()
  professor = input("지도교수 이름을 입력하세요: ").strip()
  location = input("동아리실 위치를 입력하세요: ").strip()
  introduction = input("동아리 소개를 입력하세요(20자 이내): ").strip()
  main_research = input("주요 연구 분야를 입력하세요: ").strip()

  query = """
  INSERT INTO Club (Club_Name, Professor, Location, Introduction, Main_Research)
  VALUES (%s, %s, %s, %s, %s)
  """
  cursor.execute(query, (name, professor, location, introduction, main_research))
  mydb.commit()
  os.system("clear")
  print(f"신규 동아리 '{name}'가 성공적으로 생성되었습니다.")
  cursor.close()

# 동아리 삭제 함수
def delete_club(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("삭제할 동아리의 고유번호를 입력하세요: ").strip()
  
  # 삭제 전에 해당 동아리 이름 조회
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()

  if not club:
    print(f"존재하지 않는 동아리 ID {club_id} 입니다.")
    cursor.close()
    return
  club_name = club['Club_Name']
  
  # 동아리 삭제
  query = "DELETE FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  mydb.commit()
  os.system("clear")
  print(f"동아리 '{club_name}'(ID {club_id})가 성공적으로 삭제되었습니다.")
  cursor.close()

# 동아리 정보 수정
def update_club_info(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("수정할 동아리의 고유번호를 입력하세요: ").strip()
    
    # 삭제 전에 해당 동아리 이름 조회
    query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    club = cursor.fetchone()
    
    if not club:
      print(f"존재하지 않는 동아리 ID {club_id} 입니다.")
      cursor.close()
      return
    
    club_name = club['Club_Name']

    print("\n수정할 항목을 선택하세요:")
    print("1. 이름")
    print("2. 지도교수")
    print("3. 동아리실 위치")
    print("4. 동아리 소개")
    print("5. 주요 연구 분야")
    choice = input("선택: ").strip()

    update_item = {
        "1": "Club_Name",
        "2": "Professor",
        "3": "Location",
        "4": "Introduction",
        "5": "Main_Research"
    }

    if choice in update_item:
        new_value = input(f"새로운 {update_item[choice]}을(를) 입력하세요: ").strip()
        query = f"UPDATE Club SET {update_item[choice]} = %s WHERE Club_id = %s"
        cursor.execute(query, (new_value, club_id))
        mydb.commit()
        os.system("clear")
        print(f"{club_name} 동아리 (ID {club_id})의 {update_item[choice]}가 성공적으로 수정되었습니다.")
    else:
        print("잘못된 선택입니다.")
    cursor.close()

# 전체 동아리 조회
def select_all_clubs(mydb):
  cursor = mydb.cursor(dictionary=True)
  query = "SELECT * FROM Club"
  cursor.execute(query)
  clubs = cursor.fetchall()
  cursor.close()

  if clubs:
    os.system("clear")
    print("\n========= 동아리 목록 =========")
    for club in clubs:
      print(f"ID: {club['Club_id']}, 이름: {club['Club_Name']}, 지도교수: {club['Professor']}, 위치: {club['Location']}")
    print("===============================")
  else:
    print("등록된 동아리가 없습니다.")
    
# 동아리 상세 조회
def select_club_detail(mydb):
  cursor = mydb.cursor(dictionary=True)
  query = "SELECT * FROM Club"
  cursor.execute(query)
  clubs = cursor.fetchall()
  cursor.close()

  if clubs:
    os.system("clear")
    print("\n========= 동아리 목록 =========")
    for club in clubs:
      print(f"ID: {club['Club_id']}, 이름: {club['Club_Name']}, 지도교수: {club['Professor']}, 위치: {club['Location']}")
    print("===============================")
  else:
    print("등록된 동아리가 없습니다.")
    
# 수상 실적 등록 함수(관리자 기능, 특정 동아리에 수상 실적 컬럼을 추가한다.)

# 수상 실적 조회 함수(관리자 기능, 특정 동아리의 수상 실적 리스트를 조회한다.)

# 수상 실적 수정 함수(관리자 기능, 특정 동아리의 수상 실적 중 하나를 수정한다.)

# 수상 실적 삭제 함수(관리자 기능, 특정 동아리의 수상 실적 중 하나를 삭제한다.)

# 활동 정보 조회(공통기능, 특정 동아리의 활동 정보 리스트를 조회한다.)

# 예산 내역 조회(공통기능, 특정 동아리의 예산 내역 리스트를 조회한다.)