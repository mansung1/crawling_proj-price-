from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# 로컬 CSV 파일 저장 경로
file_path = "C:/Users/user/Downloads/crawling_proj(price)/crawling_proj(강민성).csv" 

# Chrome 옵션 설정
options = Options()
options.add_argument("--headless")  # GUI 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)

# ChromeDriver 경로 설정
chrome_driver_path = "../chromedriver.exe"  # ChromeDriver 경로
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

#####################################################
# 실제 크롤링 진행
url = "https://ko.tradingeconomics.com/commodities"
driver.get(url)
# print(driver.page_source) # HTML 출력 확인

# 데이터 크롤링
rows = driver.find_elements(By.CSS_SELECTOR, "table tr")  # 테이블의 모든 행 가져오기
commodities = []

# 데이터를 테이블 행에서 추출
for row in rows[1:]:  # 첫 번째 행(헤더)은 제외
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) > 0:
        name = cols[0].text.strip()  # 상품명
        price = cols[1].text.strip()  # 가격
        change = cols[2].text.strip()  # 변화량
        percent_change = cols[3].text.strip()  # 변화율
        commodities.append([name, price, change, percent_change])

# 드라이버 종료
driver.quit()

#######################################################
# Pandas DataFrame으로 변환 및 저장
df = pd.DataFrame(commodities, columns=["상품명", "가격", "변화량", "변화율"])
df["상품명"] = df["상품명"].apply(lambda x: x.replace("\n", "[") + "]" if "\n" in x else x)  # '\n' 제거 및 변환
df["변화량"] = df["변화량"].str.replace(",", "").astype(float)  # 쉼표 제거 후 float 변환
# df # 확인

df.to_csv(file_path, index=False, encoding="cp949")  # CSV 파일 저장