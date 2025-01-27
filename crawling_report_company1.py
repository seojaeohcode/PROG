# 지속가능경영보고서 제출기업 목록 크롤링.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

webdriver_options = webdriver.ChromeOptions()
#webdriver_options.add_argument('--headless')
webdriver_options.add_argument('--no-sandbox')
webdriver_options.add_argument('--disable-dev-shm-usage')
webdriver_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=webdriver_options)

def parse_table(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.select_one("table.esg_lank_tbl")
    if not table:
        return []

    rows = table.select("tbody tr")
    companies = []
    for row in rows:
        td_company = row.select_one('td[name="com_abbrv"]')
        if td_company:
            raw_text = td_company.find(text=True, recursive=False)
            company_name = raw_text.strip() if raw_text else ""
            companies.append(company_name)
    return companies

try:
    driver.get('https://esg.krx.co.kr/contents/02/02030000/ESG02030000.jsp')
    time.sleep(5)

    all_companies = []
    page_num = 1

    while True:
        page_source = driver.page_source
        companies = parse_table(page_source)

        print(f"\n[{page_num}페이지 회사명 리스트]")
        for c in companies:
            print("회사명:", c)
        all_companies.extend(companies)

        try:
            # 다음 페이지 버튼 (활성화된 next) 찾기
            next_li = driver.find_element(By.CSS_SELECTOR, "li.next:not(.disabled)")
        except NoSuchElementException:
            print("\n더 이상 '다음 페이지' 버튼이 없거나 비활성화. 종료.")
            break

        next_btn = next_li.find_element(By.TAG_NAME, "a")

        # 클릭 시도
        try:
            next_btn.click()
            page_num += 1
            time.sleep(5)
        except ElementNotInteractableException:
            print("\n'다음 페이지' 클릭 불가(마지막 페이지 추정). 종료.")
            break

finally:
    driver.quit()

# print("\n크롤링된 모든 회사:", all_companies)