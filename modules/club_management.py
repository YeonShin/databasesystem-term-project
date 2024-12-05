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
    
# 수상 실적 등록 함수
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

  query = """
  INSERT INTO Club_Awards (Club_id, Award)
  VALUES (%s, %s)
  """
  cursor.execute(query, (club_id, award))
  mydb.commit()

  if club:
    os.system("clear")
    print(f"{club['Club_Name']} 동아리에 수상 실적 '{award}'가 등록되었습니다.")
  else:
    os.system("clear")
    print(f"동아리 ID {club_id}가 존재하지 않습니다.")
  cursor.close()

# 수상 실적 조회 함수
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

    query = "SELECT Award_id, Award FROM Club_Awards WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    awards = cursor.fetchall()
    
    cursor.close()
    

    if awards:
      os.system("clear")
      print(f"\n============= {club['Club_Name']} 동아리의 수상 실적 목록 =============")
      for idx, award in enumerate(awards, 1):
        print(f"{idx}. ID: {award['Award_id']}, 실적내용: {award['Award']}")
    else:
      os.system("clear")
      print(f"{club['Club_Name']} 동아리에 등록된 수상 실적이 없습니다.")

# 수상 실적 수정 함수
def update_award(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("수상 실적을 수정할 동아리 ID를 입력하세요: ").strip()
    award_id = input("수정할 기존 실적의 ID를 입력하세요: ").strip()
    new_award = input("새로운 수상 실적을 입력하세요: ").strip()

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

    query = """
    UPDATE Club_Awards SET Award = %s
    WHERE Club_id = %s AND Award_id = %s
    """
    cursor.execute(query, (new_award, club_id, award_id))
    mydb.commit()
  
    os.system("clear")
    print(f" {club['Club_Name']} 동아리의 수상 실적 (ID: {award_id})가 '{new_award}'로 수정되었습니다.")
    cursor.close()

# 수상 실적 삭제 함수
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

    query = "DELETE FROM Club_Awards WHERE Club_id = %s AND Award_id = %s"
    cursor.execute(query, (club_id, award_id))
    mydb.commit()
    
    os.system("clear")
    print(f"{club['Club_Name']} 동아리의 수상 실적 (ID: {award_id}) 이(가) 삭제되었습니다.")
    cursor.close()

# 활동 정보 조회 함수
def select_activities(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("활동 정보를 조회할 동아리 ID를 입력하세요: ").strip()

    query = "SELECT * FROM Activity WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    activities = cursor.fetchall()
    cursor.close()

    if activities:
        print(f"\n동아리 ID {club_id}의 활동 정보 목록:")
        for activity in activities:
            print(f"활동 이름: {activity['Aname']}, 세부 내용: {activity['Details']}")
    else:
        print(f"동아리 ID {club_id}에 등록된 활동 정보가 없습니다.")

# 예산 내역 조회 함수
def view_budget(mydb):
    cursor = mydb.cursor(dictionary=True)
    club_id = input("예산 내역을 조회할 동아리 ID를 입력하세요: ").strip()

    query = "SELECT * FROM Budget WHERE Club_id = %s"
    cursor.execute(query, (club_id,))
    budgets = cursor.fetchall()
    cursor.close()

    if budgets:
        print(f"\n동아리 ID {club_id}의 예산 내역 목록:")
        for budget in budgets:
            print(f"날짜: {budget['Date']}, 금액: {budget['Amount']}, 사용처: {budget['Usage']}")
    else:
        print(f"동아리 ID {club_id}에 등록된 예산 내역이 없습니다.")

# 활동 정보 조회 기능 (공통기능, 특정 동아리의 활동 정보 리스트를 조회, 동아리가 없을 시 처리 해주고)
def select_activities(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("활동 정보를 조회할 동아리 ID를 입력하세요: ").strip()
  
  # 동아리 존재 여부 확인
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()
  
  if club is None:
    os.system("clear")
    print(f"동아리 ID {club_id}가 존재하지 않습니다.")
    cursor.close()
    return

  # 활동 정보 조회
  query = """
  SELECT Activity_id, Aname, Activity_Date, Activity_Description
  FROM Activity WHERE Club_id = %s
  """
  cursor.execute(query, (club_id,))
  activities = cursor.fetchall()
  
  cursor.close()

  # 결과 출력
  os.system("clear")
  if activities:
    print(f"\n============= {club['Club_Name']} 동아리의 활동 정보 목록 =============")
    for activity in activities:
      print(f"ID: {activity['Activity_id']}, 이름: {activity['Aname']}, 날짜: {activity['Activity_Date']}, 내용: {activity['Activity_Description']}")
  else:
    print(f"{club['Club_Name']} 동아리에 등록된 활동 정보가 없습니다.")

# 예산 내역 조회 기능 (공통기능, 특정 동아리의 예산 내역 리스트를 조회,동아리가 없을 시 처리 해주고)
def select_budget(mydb):
  cursor = mydb.cursor(dictionary=True)
  club_id = input("예산 내역을 조회할 동아리 ID를 입력하세요: ").strip()
  
  # 동아리 존재 여부 확인
  query = "SELECT Club_Name FROM Club WHERE Club_id = %s"
  cursor.execute(query, (club_id,))
  club = cursor.fetchone()
  
  if club is None:
    os.system("clear")
    print(f"동아리 ID {club_id}가 존재하지 않습니다.")
    cursor.close()
    return

  # 예산 내역 조회
  query = """
  SELECT Budget_id, Date, Amount, Budget_Usage
  FROM Budget WHERE Club_id = %s
  """
  cursor.execute(query, (club_id,))
  budgets = cursor.fetchall()
  
  cursor.close()

  # 결과 출력
  os.system("clear")
  if budgets:
    print(f"\n============= {club['Club_Name']} 동아리의 예산 내역 =============")
    for budget in budgets:
      print(f"ID: {budget['Budget_id']}, 날짜: {budget['Date']}, 금액: {budget['Amount']}원, 사용처: {budget['Budget_Usage']}")
  else:
    print(f"{club['Club_Name']} 동아리에 등록된 예산 내역이 없습니다.")

