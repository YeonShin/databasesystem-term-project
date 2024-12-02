-- 동아리 테이블 생성
CREATE TABLE IF NOT EXISTS Club (
  Club_id INT AUTO_INCREMENT PRIMARY KEY,
  Club_Name VARCHAR(20) NOT NULL,
  Professor VARCHAR(20),
  Location VARCHAR(10),
  Introduction VARCHAR(20),
  Main_Research VARCHAR(20)
);
-- 학부관리자 테이블 생성
CREATE TABLE IF NOT EXISTS Department_Manager (
  Employee_id VARCHAR(8) PRIMARY KEY NOT NULL,
  Ename VARCHAR(20) NOT NULL,
  Department VARCHAR(20) NOT NULL
);
-- 학생 테이블 생성
CREATE TABLE IF NOT EXISTS Student (
    Student_id VARCHAR(10) PRIMARY KEY NOT NULL,
    Sname VARCHAR(20) NOT NULL,
    Department VARCHAR(20) NOT NULL,
    Year INT NOT NULL,
    Phone VARCHAR(20),
    Role ENUM('동아리장', '일반부원') NOT NULL,
    Enrollment_Status BOOLEAN DEFAULT TRUE,
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 공지사항 테이블 생성
CREATE TABLE IF NOT EXISTS Notice (
    Notice_id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(20) NOT NULL,
    Content TEXT NOT NULL,
    Posted_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Author_id VARCHAR(8),
    FOREIGN KEY (Author_id) REFERENCES Department_Manager(Employee_id)
);
-- 동아리실적 테이블 생성
CREATE TABLE IF NOT EXISTS Club_Awards (
    Club_id INT,
    Award VARCHAR(30),
    PRIMARY KEY (Club_id, Award),
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 동아리활동 테이블 생성
CREATE TABLE IF NOT EXISTS Activity (
    Activity_id INT AUTO_INCREMENT PRIMARY KEY,
    Aname VARCHAR(20) NOT NULL,
    Activity_Description TEXT,
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 동아리예산 테이블 생성
CREATE TABLE IF NOT EXISTS Budget (
    Budget_id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATETIME NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Budget_Usage VARCHAR(40),
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 학부관리자-동아리 관리 관계 테이블 생성
CREATE TABLE IF NOT EXISTS Manages (
    Manager_id VARCHAR(8),
    Club_id INT,
    PRIMARY KEY (Manager_id, Club_id),
    FOREIGN KEY (Manager_id) REFERENCES Department_Manager(Employee_id),
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);


-- 학부 관리자(조교) 초기 데이터 삽입
INSERT IGNORE INTO Department_Manager (Employee_id, Ename, Department) VALUES ('18010001', '김조교', '소프트웨어학부');
INSERT IGNORE INTO Department_Manager (Employee_id, Ename, Department) VALUES ('18010002', '이조교', '소프트웨어학부');
INSERT IGNORE INTO Department_Manager (Employee_id, Ename, Department) VALUES ('18010003', '박조교', '소프트웨어학부');

-- 동아리 초기 데이터 삽입
INSERT IGNORE INTO Club (Club_id, Club_Name, Professor, Location, Introduction, Main_Research) VALUES
(1, 'CUVIC', '이재성', 'S4-1 114', 'Chungbuk National University Visual C++ Club', 'C++');
INSERT IGNORE INTO Club (Club_id, Club_Name, Professor, Location, Introduction, Main_Research) VALUES
(2, 'SAMMARU', 'Aziz Nasridinov', 'S4-1 113', 'Security & Algorithm Management', 'Security');
INSERT IGNORE INTO Club (Club_id, Club_Name, Professor, Location, Introduction, Main_Research) VALUES
(3, 'PDA-pro', '홍장의', 'S4-1 116', 'C/C++, Android 기반 연구 동아리', 'Android');

-- 학생 초기 데이터 삽입
INSERT IGNORE INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id) VALUES
('2020039001', '차은우', '소프트웨어학과', 3, '010-1234-5678', '동아리장', TRUE, 1);
INSERT IGNORE INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id) VALUES
('2020039010', '김연신', '소프트웨어학과', 3, '010-2345-6789', '일반부원', TRUE, 1);
INSERT IGNORE INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id) VALUES
('2020039002', '손흥민', '소프트웨어학과', 3, '010-3456-7890', '동아리장', TRUE, 2);
INSERT IGNORE INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id) VALUES
('2020041001', '박지성', '소프트웨어학부', 3, '010-4567-8901', '일반부원', TRUE, 1);
INSERT IGNORE INTO Student (Student_id, Sname, Department, Year, Phone, Role, Enrollment_Status, Club_id) VALUES
('2020039003', '장원영', '소프트웨어학과', 1, '010-5678-9012', '일반부원', TRUE, 1);
