import pymysql
import pandas as pd

# CSV 파일 로드
csv_file = r"c:\Users\user\Downloads\crawling_proj(강민성).csv"
df = pd.read_csv(csv_file, encoding='cp949')
df["변화량"] = df["변화량"].str.replace(',', '').astype(float) # 쉼표 제거 및 float 변환

# MySQL 연결 설정
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="crawling_proj_price"
)

cursor = connection.cursor() # 커서 생성
# print("SQL 연결 성공")

# 데이터 삽입 : 쿼리지정 후 for문으로 csv의 내용을 반복 삽입
insert_query = """
INSERT INTO commodities (name, price, change_amount, change_percent)
VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["상품명"],  
        float(row["가격"]), 
        float(row["변화량"]), 
        row["변화율"]        
    ))

connection.commit() #저장

# 연결 종료
cursor.close()
connection.close()
