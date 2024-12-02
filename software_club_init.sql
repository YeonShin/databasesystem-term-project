-- 데이터베이스가 존재하지 않다면 생성
CREATE DATABASE IF NOT EXISTS software_club;
USE software_club;

-- 동아리 테이블 생성
CREATE TABLE IF NOT EXISTS Club (
  Club_id INT AUTO_INCREMENT PRIMARY KEY,
  Club_Name VARCHAR(40) NOT NULL,
  Professor VARCHAR(20),
  Location VARCHAR(20),
  Introduction TEXT,
  Main_Research TEXT
);
-- 학부관리자 테이블 생성
CREATE TABLE IF NOT EXISTS Department_Manager (
  Employee_id INT AUTO_INCREMENT PRIMARY KEY,
  Ename VARCHAR(20) NOT NULL,
  Department VARCHAR(50) NOT NULL
);
-- 학생 테이블 생성
CREATE TABLE IF NOT EXISTS Student (
    Student_id INT AUTO_INCREMENT PRIMARY KEY,
    Sname VARCHAR(100) NOT NULL,
    Department VARCHAR(100),
    Year INT,
    Phone VARCHAR(20),
    Role ENUM('동아리장', '일반부원') NOT NULL,
    Enrollment_Status BOOLEAN,
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 공지사항 테이블 생성
CREATE TABLE IF NOT EXISTS Notice (
    Notice_id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(200) NOT NULL,
    Content TEXT NOT NULL,
    Posted_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Author_id INT,
    FOREIGN KEY (Author_id) REFERENCES Department_Manager(Employee_id)
);
-- 동아리실적 테이블 생성
CREATE TABLE IF NOT EXISTS Club_Awards (
    Club_id INT,
    Award VARCHAR(100),
    PRIMARY KEY (Club_id, Award),
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 동아리활동 테이블 생성
CREATE TABLE IF NOT EXISTS Activity (
    Activity_id INT AUTO_INCREMENT PRIMARY KEY,
    Aname VARCHAR(100) NOT NULL,
    Activity_Description TEXT,
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 동아리예산 테이블 생성
CREATE TABLE IF NOT EXISTS Budget (
    Budget_id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATETIME NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Usage VARCHAR(255),
    Club_id INT,
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);
-- 학부관리자-동아리 관리 관계 테이블 생성
CREATE TABLE IF NOT EXISTS Manages (
    Manager_id INT,
    Club_id INT,
    PRIMARY KEY (Manager_id, Club_id),
    FOREIGN KEY (Manager_id) REFERENCES Department_Manager(Employee_id),
    FOREIGN KEY (Club_id) REFERENCES Club(Club_id)
);