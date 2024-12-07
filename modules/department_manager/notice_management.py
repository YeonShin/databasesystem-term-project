import os

# 공지사항 등록 기능 (관리자 기능, 공지사항을 게시할 수 있음)
def post_notice(mydb, author_id):
  cursor = mydb.cursor(dictionary=True)
  try:
    title = input("공지사항 제목을 입력하세요: ").strip()
    content = input("공지사항 내용을 입력하세요: ").strip()

    # 공지사항 등록
    query = """
    INSERT INTO Notice (Title, Content, Author_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (title, content, author_id))
    mydb.commit()

    os.system("clear")
    print("공지사항이 성공적으로 게시되었습니다.")
    cursor.close()
  except ValueError:
    os.system('clear')
    print("유효하지 않은 입력입니다. 다시 시도해주세요.")
  except Exception as e:
    os.system('clear')
    print(f"오류 발생: {str(e)}")

# 공지사항 조회 기능 (관리자 기능, 모든 관리자들이 작성한 공지사항 목록을 볼 수 있음, 목록에서는 공지번호, 제목, 작성일자, 작성자 이름(ID))
def select_notices(mydb):
  cursor = mydb.cursor(dictionary=True)

  # 모든 공지사항 조회
  query = """
  SELECT Notice_id, Title, Posted_Date, Ename, Author_id
  FROM Notice
  INNER JOIN Department_Manager ON Notice.Author_id = Department_Manager.Employee_id
  """
  cursor.execute(query)
  notices = cursor.fetchall()
  cursor.close()

  os.system("clear")
  if notices:
    print("\n============= 공지사항 목록 =============")
    for notice in notices:
      print(f"공지번호: {notice['Notice_id']}, 제목: {notice['Title']}, 작성일자: {notice['Posted_Date']}, 작성자: {notice['Ename']} ({notice['Author_id']})")
  else:
    print("등록된 공지사항이 없습니다.")

# 공지사항 상세 조회 기능 (관리자 기능, 특정 공지사항의 id를 받아 상세 내용을 볼 수 있음. 제목, 작성일자, 작성자 이름, 내용(따로 줄 파서 출력))
def select_notice_detail(mydb):
  cursor = mydb.cursor(dictionary=True)
  notice_id = input("조회할 공지사항 ID를 입력하세요: ").strip()

  # 특정 공지사항 상세 조회
  query = """
  SELECT Title, Posted_Date, Ename, Content
  FROM Notice
  INNER JOIN Department_Manager ON Notice.Author_id = Department_Manager.Employee_id
  WHERE Notice_id = %s
  """
  cursor.execute(query, (notice_id,))
  notice = cursor.fetchone()
  cursor.close()

  os.system("clear")
  if notice:
    print(f"\n============= 공지사항 상세 정보 =============")
    print(f"제목: {notice['Title']}")
    print(f"작성일자: {notice['Posted_Date']}")
    print(f"작성자: {notice['Ename']}")
    print(f"\n내용:\n{notice['Content']}")
    print(f"=========================================\n")
  else:
    os.system("clear")
    print(f"공지사항 ID {notice_id}가 존재하지 않습니다.")

# 공지사항 수정 기능 (관리자 기능, 특정 공지사항의 제목, 내용을 수정할 수 있음, 작성한 작성자만이 수정 가능!)
def update_notice(mydb, author_id):
  cursor = mydb.cursor(dictionary=True)
  notice_id = input("수정할 공지사항 ID를 입력하세요: ").strip()

  # 공지사항 작성자 확인
  query = "SELECT * FROM Notice WHERE Notice_id = %s"
  cursor.execute(query, (notice_id,))
  notice = cursor.fetchone()

  if notice is None:
    os.system("clear")
    print(f"공지사항 ID {notice_id}가 존재하지 않습니다.")
    cursor.close()
    return

  if notice['Author_id'] != author_id:
    os.system("clear")
    print("수정 권한이 없습니다. 작성자만 공지사항을 수정할 수 있습니다.")
    cursor.close()
    return

  try:
    # 공지사항 수정
    new_title = input("새로운 제목을 입력하세요 [변경하지 않으려면 엔터]: ").strip() or notice['Title']
    new_content = input("새로운 내용을 입력하세요 [변경하지 않으려면 엔터]: ").strip() or notice['Content']

    query = """
    UPDATE Notice SET Title = %s, Content = %s WHERE Notice_id = %s
    """
    cursor.execute(query, (new_title, new_content, notice_id))
    mydb.commit()

    os.system("clear")
    print(f"공지사항 ID {notice_id}가 성공적으로 수정되었습니다.")
    cursor.close()
  except ValueError:
    os.system('clear')
    print("유효하지 않은 입력입니다. 다시 시도해주세요.")
  except Exception as e:
    os.system('clear')
    print(f"오류 발생: {str(e)}")

# 공지사항 삭제 기능 (관리자 기능, 특정 공지사항을 삭제하는 기능, 작성한 작성자만 삭제 가능)
def delete_notice(mydb, author_id):
  cursor = mydb.cursor(dictionary=True)
  notice_id = input("삭제할 공지사항 ID를 입력하세요: ").strip()

  # 공지사항 작성자 확인
  query = "SELECT * FROM Notice WHERE Notice_id = %s"
  cursor.execute(query, (notice_id,))
  notice = cursor.fetchone()

  if notice is None:
    os.system("clear")
    print(f"공지사항 ID {notice_id}가 존재하지 않습니다.")
    cursor.close()
    return

  if notice['Author_id'] != author_id:
    os.system("clear")
    print("삭제 권한이 없습니다. 작성자만 공지사항을 삭제할 수 있습니다.")
    cursor.close()
    return

  # 삭제 확인
  confirm = input(f"공지사항 '{notice['Title']}'를 삭제하시겠습니까? (y/n): ").strip().lower()
  if confirm == 'y':
    query = """
    DELETE FROM Notice WHERE Notice_id = %s
    """
    cursor.execute(query, (notice_id,))
    mydb.commit()
    os.system('clear')
    print(f"공지사항 ID {notice_id}가 성공적으로 삭제되었습니다.")
  else:
    os.system('clear')
    print("공지사항 삭제가 취소되었습니다.")
  cursor.close()
