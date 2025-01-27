# 경영보고서 제출 회사들
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def parse_table(page_source):
    """
    HTML에서 table.esg_lank_tbl -> td[name="com_nm"]의 회사명을 추출
    <td name="com_nm">
      <a href="...">회사명</a>
      <span class="icobox">N..</span>
    </td>
    """
    soup = BeautifulSoup(page_source, "html.parser")
    table = soup.select_one("table.esg_lank_tbl")
    if not table:
        return []

    rows = table.select("tbody tr")
    results = []
    for row in rows:
        td_company = row.select_one('td[name="com_nm"]')
        if td_company:
            # a 태그 텍스트만 빼오면 "NN" 등을 무시 가능
            link_tag = td_company.select_one("a")
            if link_tag:
                comp_name = link_tag.get_text(strip=True)
            else:
                # 혹시 <a>가 없으면 td 자체에서 첫 번째 텍스트
                raw_text = td_company.find(text=True, recursive=False)
                comp_name = raw_text.strip() if raw_text else ""
            results.append(comp_name)
    return results

webdriver_options = webdriver.ChromeOptions()
#webdriver_options.add_argument("--headless")
webdriver_options.add_argument("--no-sandbox")
webdriver_options.add_argument("--disable-dev-shm-usage")
webdriver_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=webdriver_options)

try:
    # 1) 페이지 접속
    url = "https://esg.krx.co.kr/contents/02/02040000/ESG02040000.jsp"
    driver.get(url)
    time.sleep(3)

    # 2) 날짜 필드를 'name'으로 찾아서 설정 (2024-01-01, 2024-12-31)
    #    => ID가 동적으로 변하므로 NAME으로 검색
    from_date = driver.find_element(By.NAME, "fr_work_dt")
    to_date   = driver.find_element(By.NAME, "to_work_dt")

    from_date.clear()
    from_date.send_keys("20240101")
    to_date.clear()
    to_date.send_keys("20241231")

    # 3) 조회 버튼 클릭
    search_btn = driver.find_element(By.CSS_SELECTOR, "button.sch_btn")
    search_btn.click()

    time.sleep(5)  # Ajax 로딩 대기

    all_companies = []
    page_num = 1

    while True:
        # 현재 페이지 HTML 파싱
        html = driver.page_source
        companies = parse_table(html)

        print(f"\n[{page_num}페이지 회사명]")
        for c in companies:
            print("회사명:", c)
        all_companies.extend(companies)

        # '다음 페이지' 찾기: <li class="next:not(.disabled)">
        try:
            next_li = driver.find_element(By.CSS_SELECTOR, "li.next:not(.disabled)")
        except NoSuchElementException:
            print("\n다음 페이지 없음 or disabled. 종료.")
            break

        # 클릭
        next_a = next_li.find_element(By.TAG_NAME, "a")
        try:
            next_a.click()
            page_num += 1
            time.sleep(4)
        except ElementNotInteractableException:
            print("\n다음 페이지 버튼 클릭 불가. 종료.")
            break

finally:
    driver.quit()

print(f"\n크롤링된 총 회사 수: {len(all_companies)}")
