# 생성된 사용자 정보 예시
# 데이터베이스 이름 : user_01
# 유저 이름 : db_01
# 유저 암호 : pw_01

import boto3
import pymysql

# RDS 연결 정보
rds_host = "AWS RDS 데이터베이스 엔드포인트"
db_username = 'RDS 사용자'
db_password = 'RDS 사용자 암호'
db_name="notes"

# RDS에 연결
try:
    conn = pymysql.connections.Connection(host=rds_host, user=db_username, password=db_password, database=db_name)
except Exception as e:
    print(f"Error connecting to RDS: {e}")
    exit()

# 사용자 및 데이터베이스 생성 및 권한 부여
def create_database_and_user(user_index):
    user_name = f"user_{user_index:02d}"
    db_name = f"db_{user_index:02d}"
    user_password = f"pw_{user_index:02d}"

    with conn.cursor() as cursor:
        # 데이터베이스 생성
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
        cursor.execute(create_db_query)

        # 사용자 생성 및 권한 부여
        create_user_query = f"CREATE USER IF NOT EXISTS '{user_name}'@'%' IDENTIFIED BY '{user_password}';"
        cursor.execute(create_user_query)
        grant_query = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{user_name}'@'%';"
        cursor.execute(grant_query)
        conn.commit()

# 사용자 및 데이터베이스를 원하는 횟수만큼 생성
number_of_users = 16  # 사용자 및 데이터베이스를 몇 개 생성할 지 지정
for i in range(0, number_of_users + 1):
    create_database_and_user(i)

# RDS 연결 종료
conn.close()

# pip install boto3 pymysql
# python3 database_creator.py
