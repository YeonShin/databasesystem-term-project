import os

# (동아리장 기능) 신규 활동 등록
def create_activity(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)

    # 활동 이름 및 설명 입력받기
    activity_name = input("활동 이름을 입력하세요: ").strip()
    activity_description = input("활동 설명을 입력하세요: ").strip()

    # 활동 등록 쿼리
    query = """
    INSERT INTO Activity (Aname, Activity_Description, Club_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (activity_name, activity_description, club_id))
    mydb.commit()
    cursor.close()

    print(f"활동 '{activity_name}'이 성공적으로 등록되었습니다.")

# (동아리장 기능) 활동 정보 조회
def select_activities(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)

    # 해당 동아리의 모든 활동 조회
    query = """
    SELECT * FROM Activity WHERE Club_id = %s
    """
    cursor.execute(query, (club_id,))
    activities = cursor.fetchall()
    cursor.close()

    if activities:
        print(f"\n====== 동아리 (ID: {club_id})의 활동 목록 ======")
        for activity in activities:
            print(f"활동 ID: {activity['Activity_id']}, 이름: {activity['Aname']}, 날짜: {activity['Activity_Date']}, \n설명: {activity['Activity_Description']}")
    else:
        print(f"동아리 (ID: {club_id})에 등록된 활동이 없습니다.")

# (동아리장 기능) 활동 정보 수정
def update_activity(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)

    # 수정할 활동 ID 입력받기
    activity_id = input("수정할 활동의 ID를 입력하세요: ").strip()

    # 활동 존재 여부 확인
    query = """
    SELECT * FROM Activity WHERE Activity_id = %s AND Club_id = %s
    """
    cursor.execute(query, (activity_id, club_id))
    activity = cursor.fetchone()

    if not activity:
        print(f"활동 ID {activity_id}가 존재하지 않거나 이 동아리에 속하지 않습니다.")
        cursor.close()
        return

    # 새로운 활동 이름 및 설명 입력받기
    new_name = input(f"새 활동 이름 (현재: {activity['Aname']}) [변경하지 않으려면 엔터]: ").strip() or activity['Aname']
    new_description = input(f"새 활동 설명 (현재: {activity['Activity_Description']}) [변경하지 않으려면 엔터]: ").strip() or activity['Activity_Description']

    # 활동 정보 업데이트
    query_update = """
    UPDATE Activity
    SET Aname = %s, Activity_Description = %s
    WHERE Activity_id = %s AND Club_id = %s
    """
    cursor.execute(query_update, (new_name, new_description, activity_id, club_id))
    mydb.commit()
    cursor.close()

    print(f"활동 ID {activity_id}가 성공적으로 수정되었습니다.")

# (동아리장 기능) 활동 삭제
def delete_activity(mydb, club_id):
    cursor = mydb.cursor(dictionary=True)

    # 삭제할 활동 ID 입력받기
    activity_id = input("삭제할 활동의 ID를 입력하세요: ").strip()

    # 활동 존재 여부 확인
    query = """
    SELECT * FROM Activity WHERE Activity_id = %s AND Club_id = %s
    """
    cursor.execute(query, (activity_id, club_id))
    activity = cursor.fetchone()

    if not activity:
        print(f"활동 ID {activity_id}가 존재하지 않거나 이 동아리에 속하지 않습니다.")
        cursor.close()
        return

    # 삭제 확인
    confirm = input(f"활동 '{activity['Aname']}'를 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm == 'y':
        query_delete = """
        DELETE FROM Activity WHERE Activity_id = %s AND Club_id = %s
        """
        cursor.execute(query_delete, (activity_id, club_id))
        mydb.commit()
        print(f"활동 ID {activity_id}가 성공적으로 삭제되었습니다.")
    else:
        print("활동 삭제가 취소되었습니다.")

    cursor.close()

# ()