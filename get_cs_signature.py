from playwright.sync_api import sync_playwright


def get_cs_signature():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://home.kahis.go.kr/home/lkntscrinfo/selectLkntsOccrrncList.do")
        cs_signature = page.query_selector('input[name="csSignature"]').get_attribute('value')
        browser.close()
        return cs_signature

if __name__ == "__main__":
    cs_signature = get_cs_signature()
    print(cs_signature)
