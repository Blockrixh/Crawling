import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


service = Service('chromedriver')  
options = Options()
options.add_argument('--start-maximized')
# driver = webdriver.Chrome(service=service, options=options)

url = "https://kgeop.go.kr/info/infoMap.do"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
wait = WebDriverWait(driver, 10)


# 주소 목록 불러오기
df = pd.read_csv(r"C:\Users\julee\proj\kei\missed.csv", encoding = 'utf-8-sig')
addresses = df["address"].tolist()


# 2. 도움말 닫기 버튼
try:
    close_btn = driver.find_element(By.CLASS_NAME, "btnHelpClose")
    close_btn.click()
    print("[2] 도움말 닫기 완료")
except:
    print("[2] 도움말 창 없음 → 계속 진행")


results = []
batch_size = 500

# 주소 만들기
for i, address in enumerate(addresses, start=1):
    print(f"[{i}] 검색 중: {address}")
    try:
        # 주소 입력
        input_box = driver.find_element(By.ID, "josuKeyword")
        input_box.click()
        time.sleep(0.8)
        driver.execute_script("arguments[0].value = '';", input_box)
        driver.execute_script(f"arguments[0].value = '{address}';", input_box)
        driver.execute_script("""
            const input = arguments[0];
            const event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
        """, input_box)

        # 검색 클릭
        search_btn = driver.find_element(By.CLASS_NAME, "btnSearch")
        search_btn.click()
        time.sleep(2)

        # 검색 결과 클릭
        result_box = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jusoResult"]/div/div'))
        )
        result_box.click()
        time.sleep(1)

        # 상세정보 클릭
        detail_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btnMoreInfo"))
        )
        detail_btn.click()
        time.sleep(2)

        # 데이터 추출
        category = driver.find_element(By.XPATH, '//*[@id="contentArea"]/div[2]/div/div[2]/div/section[2]/div/div[2]/table/tbody/tr[2]/td[1]').text.strip()
        owner = driver.find_element(By.XPATH, '//*[@id="contentArea"]/div[2]/div/div[2]/div/section[2]/div/div[2]/table/tbody/tr[2]/td[2]').text.strip()
        date = driver.find_element(By.XPATH, '//*[@id="contentArea"]/div[2]/div/div[2]/div/section[2]/div/div[2]/table/tbody/tr[2]/td[3]').text.strip()
        reason = driver.find_element(By.XPATH, '//*[@id="contentArea"]/div[2]/div/div[2]/div/section[2]/div/div[2]/table/tbody/tr[2]/td[4]').text.strip()
    except Exception as e:
        category, owner, date, reason = "", "", "", ""

    # 결과 저장
    results.append({
        "address": address,
        "소유구분": category,
        "소유자": owner,
        "변동일자": date,
        "변동사유": reason
    })

    # 500개마다 저장
    if i % batch_size == 0 or i == len(addresses):
        part = i // batch_size + (1 if i % batch_size else 0)
        out_df = pd.DataFrame(results)
        out_df.to_csv(f"output_{part}.csv", index=False, encoding='utf-8-sig')
        print(f"{i}개 저장 완료: output_{part}.csv")

# 마무리
driver.quit()
print("전체 완료")
