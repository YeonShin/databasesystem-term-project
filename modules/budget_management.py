import os

# (동아리장 기능) 신규 예산내역 등록
def create_budget(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  # 예산 입력받기
  try:
    amount = int(input("금액을 입력하세요: ").strip())
    year = int(input("연도를 입력하세요 (예: 2024): ").strip())
    month = int(input("월을 입력하세요 (1-12): ").strip())
    day = int(input("일을 입력하세요 (1-31): ").strip())
    usage = input("사용처를 입력하세요: ").strip()

    # 입력받은 날짜를 형식화
    date = f"{year}-{month:02d}-{day:02d} 00:00:00"

    # 예산 등록 쿼리
    query = """
    INSERT INTO Budget (Date, Amount, Budget_Usage, Club_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (date, amount, usage, club_id))
    mydb.commit()
    print(f"예산 {amount}원이 성공적으로 등록되었습니다. 사용처: {usage}")
  except ValueError:
    print("유효하지 않은 입력입니다. 다시 시도해주세요.")
  except Exception as e:
    print(f"오류 발생: {str(e)}")

    cursor.close()

# (동아리장 기능) 예산내역 조회
def select_budgets(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  # 해당 동아리의 예산 내역 조회
  query = """
  SELECT * FROM Budget WHERE Club_id = %s
  """
  cursor.execute(query, (club_id,))
  budgets = cursor.fetchall()
  cursor.close()

  if budgets:
    print(f"\n====== 동아리 (ID: {club_id})의 예산 내역 ======")
    for budget in budgets:
      print(f"예산 ID: {budget['Budget_id']}, 금액: {budget['Amount']}, 날짜: {budget['Date']}, 사용처: {budget['Budget_Usage']}")
  else:
    print(f"동아리 (ID: {club_id})에 등록된 예산 내역이 없습니다.")


# (동아리장 기능) 예산내역 수정
def update_budget(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  # 수정할 예산 ID 입력받기
  budget_id = input("수정할 예산의 ID를 입력하세요: ").strip()

  # 예산 존재 여부 확인
  query = """
  SELECT * FROM Budget WHERE Budget_id = %s AND Club_id = %s
  """
  cursor.execute(query, (budget_id, club_id))
  budget = cursor.fetchone()

  if not budget:
    print(f"예산 ID {budget_id}가 존재하지 않거나 이 동아리에 속하지 않습니다.")
    cursor.close()
    return

  # 새로운 정보 입력받기
  new_amount = input(f"새 금액 (현재: {budget['Amount']}) [변경하지 않으려면 엔터]: ").strip()
  new_amount = float(new_amount) if new_amount else budget['Amount']

  year = input(f"새 연도 (현재: {budget['Date'].year}) [변경하지 않으려면 엔터]: ").strip() or budget['Date'].year
  month = input(f"새 월 (현재: {budget['Date'].month}) [변경하지 않으려면 엔터]: ").strip() or budget['Date'].month
  day = input(f"새 일 (현재: {budget['Date'].day}) [변경하지 않으려면 엔터]: ").strip() or budget['Date'].day

  new_date = f"{year}-{int(month):02d}-{int(day):02d} 00:00:00"
  new_usage = input(f"새 사용처 (현재: {budget['Budget_Usage']}) [변경하지 않으려면 엔터]: ").strip() or budget['Budget_Usage']

  # 예산 정보 업데이트
  query_update = """
  UPDATE Budget
  SET Amount = %s, Date = %s, Budget_Usage = %s
  WHERE Budget_id = %s AND Club_id = %s
  """
  cursor.execute(query_update, (new_amount, new_date, new_usage, budget_id, club_id))
  mydb.commit()
  cursor.close()

  print(f"예산 ID {budget_id}가 성공적으로 수정되었습니다.")


# (동아리장 기능) 예산내역 삭제
def delete_budget(mydb, club_id):
  cursor = mydb.cursor(dictionary=True)

  # 삭제할 예산 ID 입력받기
  budget_id = input("삭제할 예산의 ID를 입력하세요: ").strip()

  # 예산 존재 여부 확인
  query = """
  SELECT * FROM Budget WHERE Budget_id = %s AND Club_id = %s
  """
  cursor.execute(query, (budget_id, club_id))
  budget = cursor.fetchone()

  if not budget:
    print(f"예산 ID {budget_id}가 존재하지 않거나 이 동아리에 속하지 않습니다.")
    cursor.close()
    return

  # 삭제 확인
  confirm = input(f"예산 ID {budget_id} (금액: {budget['Amount']}, 사용처: {budget['Budget_Usage']})를 삭제하시겠습니까? (y/n): ").strip().lower()
  if confirm == 'y':
    query_delete = """
    DELETE FROM Budget WHERE Budget_id = %s AND Club_id = %s
    """
    cursor.execute(query_delete, (budget_id, club_id))
    mydb.commit()
    print(f"예산 ID {budget_id}가 성공적으로 삭제되었습니다.")
  else:
    print("예산 삭제가 취소되었습니다.")

  cursor.close()
