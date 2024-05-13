# 생성된 사용자 정보 예시
# 데이터베이스 이름 : DB_001
# 유저 이름 : DB_001
# 유저 암호 : 001001


import pymysql
import boto3

# RDS 연결 정보
rds_host = "DB_HOST"
db_username = 'DB_USER'
db_password = 'DB_PW'

# RDS에 연결
try:
    conn = pymysql.connections.Connection(host=rds_host, user=db_username, password=db_password)
except Exception as e:
    print(f"Error connecting to RDS: {e}")
    exit()

# 데이터베이스와 사용자 생성, 테이블 생성 및 초기 데이터 삽입
def create_database_and_user(user_index):
    user_name = f"DB_{user_index:03d}"
    db_name = f"DB_{user_index:03d}"
    user_password = f"{user_index:03d}{user_index:03d}"

    with conn.cursor() as cursor:
        # 데이터베이스 생성
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        
        # 사용자 생성 및 권한 부여
        cursor.execute(f"CREATE USER IF NOT EXISTS '{user_name}'@'%' IDENTIFIED BY '{user_password}';")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{user_name}'@'%';")

        # 생성된 데이터베이스 사용
        cursor.execute(f"USE {db_name};")

        # 테이블 생성 및 초기 데이터 삽입
        ## factories 테이블
        cursor.execute("CREATE TABLE factories (factory_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), locate VARCHAR(255));")
        ## itmes 테이블
        cursor.execute("CREATE TABLE items (item_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), price INT, quantity INT, factory_id INT, FOREIGN KEY (factory_id) REFERENCES factories(factory_id));")
        ## 샘플 데이터 입력
        cursor.execute("INSERT INTO factories (name, locate) VALUES ('Factory1', 'korea'), ('Factory2', 'usa');")
        cursor.execute("INSERT INTO items (name, price, quantity, factory_id) VALUES ('Item1', 10000, 1, 1), ('Item2', 20000, 2, 2), ('Item3', 30000, 3, 1);")

        conn.commit()

# 사용자 및 데이터베이스를 원하는 횟수만큼 생성
number_of_users = 40  # 생성할 사용자 및 데이터베이스 수
for i in range(1, number_of_users + 1):
    create_database_and_user(i)

# RDS 연결 종료
conn.close()


# pip install boto3 pymysql
# python3 students_database_creator.py
