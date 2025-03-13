from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 실제 브라우저 모드
    page = browser.new_page()
    page.goto("https://home.kahis.go.kr/home/lkntscrinfo/selectLkntsOccrrncList.do")

    # csSignature 값 추출 (JavaScript에서 값이 동적으로 생성되었다면)
    cs_signature = page.query_selector('input[name="csSignature"]').get_attribute('value')
    
    # 이후 csSignature와 필요한 데이터를 POST 요청에 사용할 수 있습니다.
    print(cs_signature)
    
    browser.close()
