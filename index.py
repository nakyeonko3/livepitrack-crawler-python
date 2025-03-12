import requests
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd
import time
import random
import lxml
from lxml import html, etree
import re


PAGE_INDEX_XPATH = '//td[contains(text(), "전체 : ")][1]'
XPATH_TABLE_DATA = "/html/body/div[1]/div[2]/div[3]/form[2]/table[4]/tr[2]/td/table"
# XPATH_TABLE_DATA = "/html/body/div[1]/div[2]/div[3]/form[2]/table[4]/tr/td/table/tr"
def fetch_page(page_index, base_params):
    """페이지별 데이터 요청 함수"""
    session = requests.Session()
    
    # 기본 파라미터에 페이지 인덱스 추가
    params = base_params.copy()
    params['pageIndex'] = str(page_index)
    
    # 요청 헤더
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://home.kahis.go.kr/home/",
        "User-Agent": "Mozilla/5.0"
    }
    
    # 랜덤 지연 추가 (서버 부하 방지)
    time.sleep(random.uniform(0.5, 1.5))
    
    try:
        response = session.post(
            "https://home.kahis.go.kr/home/lkntscrinfo/selectLkntsOccrrncList.do", 
            data=params, 
            headers=headers
        )
        response.raise_for_status()  # HTTP 오류 검사
        return response.text
    except Exception as e:
        print(f"페이지 {page_index} 요청 실패: {str(e)}")
        return None


   

def main():
    # 기본 파라미터 설정 (사용자 입력 기반)
    base_params = {
        "csSignature": "f8kcFfnwghfIToSYbM6uxQ%3D%3D",
        "turmGubun": "01",
        "occrFromDt": "2024-03-13",
        "occrToDt": "2025-03-13",
        "dissCl": "",
        "lstkspCl": "",
        "legalIctsdGradSe": ""
    }
    
    # 첫 페이지 요청하여 총 페이지 수 알아내기
    first_page_html = fetch_page(1, base_params)
    root = html.fromstring(first_page_html)

    total_pages_element = root.xpath(PAGE_INDEX_XPATH)[0]
    total_pages_text = total_pages_element.text.strip()
    total_pages = int(re.search(r'\d+(?=쪽\))', total_pages_text).group())
    
    all_data = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
    # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # 모든 페이지에 대한 요청을 제출
        future_to_page = {
            executor.submit(fetch_page, page, base_params): page
            for page in range(1, total_pages + 1)
        }
        
        # 결과가 완료되는 대로 처리
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                html_content = future.result()
                if html_content:
                    # HTML 파싱 및 데이터 추출
                    root = html.fromstring(html_content)
                    table_data = root.xpath(XPATH_TABLE_DATA)[0]
                    table_rows = table_data.xpath('.//tr')
                    for i, row in enumerate(table_rows, 1):
                        cells = [td.text_content().strip() for td in row.xpath('.//td')]
                        all_data.append(cells)
                    print(f"페이지 {page} 처리 완료")
            except Exception as e:
                print(f"페이지 {page} 처리 중 오류 발생: {str(e)}")
    
    # 칼럼 이름 정의
    columns = ['가축전염병명', '농장명(농장주)', '농장소재지', '발생일자(진단일)', '축종(품종)', '발생두수(마리)', '진단기관', '종식일']

    # DataFrame 생성
    df = pd.DataFrame(all_data, columns=columns)

    # '\r' 제거 (Series에 적용해야 함)
    df['발생일자(진단일)'] = df['발생일자(진단일)'].str.replace('\r', '', regex=False)

    # 발생일자와 진단일을 분리
    # 발생일자 추출 - '(' 앞부분
    df['발생일자'] = df['발생일자(진단일)'].apply(lambda x: x.split('(')[0].strip())

    # 진단일 추출 - 괄호 안의 내용
    df['진단일'] = df['발생일자(진단일)'].apply(lambda x: x.split('(')[1].replace(')', '').strip() if '(' in x else '')

    # 기존 '발생일자(진단일)' 열 삭제
    df = df.drop(columns=['발생일자(진단일)'])

    종식일_값 = df['종식일'].copy()
    df = df.drop(columns=['종식일'])
    df['종식일'] = 종식일_값

    # CSV 파일로 저장
    df.to_csv('livestock_disease_data.csv', index=False, encoding='utf-8-sig')

    # 저장 확인용 출력
    print("CSV 파일로 저장 완료: livestock_disease_data.csv")
    print(df)
    
if __name__ == "__main__":
    main()


