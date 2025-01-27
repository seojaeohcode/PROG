from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def parse_bond_table(page_source):
    """
    ESG채권 페이지의 'CI-GRID-BODY-TABLE' 테이블을 파싱하여
    발행기관( com_abbrv ), 표준코드( isu_cd ), 종목명( isu_nm ) 등을 추출합니다.
    """
    soup = BeautifulSoup(page_source, "html.parser")
    table = soup.select_one("table.CI-GRID-BODY-TABLE")
    if not table:
        return []

    rows = table.select("tbody tr")
    results = []
    for row in rows:
        # 발행기관
        org_td = row.select_one('td[data-name="com_abbrv"]')
        org_name = org_td.get_text(strip=True) if org_td else ""

        # 표준코드
        code_td = row.select_one('td[data-name="isu_cd"]')
        code = code_td.get_text(strip=True) if code_td else ""

        # 종목명
        name_td = row.select_one('td[data-name="isu_nm"]')
        name = name_td.get_text(strip=True) if name_td else ""

        results.append(
            {
                "발행기관": org_name,
                "표준코드": code,
                "종목명": name
            }
        )
    return results

# 1) 셀레니움 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 2) 페이지 접속
    url = "https://esgbond.krx.co.kr/contents/02/02010000/SRI02010000.jsp"
    driver.get(url)
    
    # 페이지 로딩 대기
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "CI-FREEZE-SCROLLER"))
    )

    # 3) 테이블 스크롤
    scroller = driver.find_element(By.CLASS_NAME, "CI-FREEZE-SCROLLER")
    last_height = driver.execute_script("return arguments[0].scrollHeight", scroller)

    while True:
        # 스크롤 다운
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroller)
        time.sleep(2)  # 데이터 로딩 대기

        # 새로운 높이
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroller)

        # 높이가 변동이 없다면 스크롤 종료
        if new_height == last_height:
            break

        last_height = new_height

    # 4) 최종 HTML로 테이블 파싱
    final_html = driver.page_source
    bond_data = parse_bond_table(final_html)

finally:
    driver.quit()

# 결과 출력
print(f"총 {len(bond_data)}개 항목을 수집했습니다.")
for item in bond_data:
    print(item)
