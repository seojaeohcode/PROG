from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# 1) 크롬 옵션 설정
webdriver_options = webdriver.ChromeOptions()
#webdriver_options.add_argument('--headless')            # 창을 띄우지 않고 실행
webdriver_options.add_argument('--no-sandbox')          # 로컬에서는 큰 의미 없지만 무해
webdriver_options.add_argument('--disable-dev-shm-usage')
webdriver_options.add_argument('--disable-gpu')         # (선택) GPU 가속 비활성화
webdriver_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
)

# 2) webdriver_manager로 크롬드라이버 자동 설치/갱신
service = Service(ChromeDriverManager().install())

# 3) 드라이버 생성
driver = webdriver.Chrome(service=service, options=webdriver_options)

# 4) 암묵적 대기 (필요 시)
driver.implicitly_wait(5)

# 5) 테스트할 URL
url = 'https://esg.krx.co.kr/contents/02/02030000/ESG02030000.jsp'
driver.get(url)

time.sleep(2)  # 페이지 로딩 간단 대기 (선택)

# 6) 페이지 제목 확인
print("페이지 제목:", driver.title)

# 7) 브라우저 종료
driver.quit()
