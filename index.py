from numpy.dtypes import ObjectDType
import requests
import concurrent.futures
import pandas as pd
import time
import random
from lxml import html
import re
import openpyxl
import os


# custom_params 설정
# 기본 파라미터 설정 (사용자 입력 기반)
custom_params = { 
    "turmGubun": "02", # 02: 발생일
    "occrFromDt": "2000-01-13", # 시작일
    "occrToDt": "2025-03-13", # 종료일
    "dissCl": "0111", # 질병명: 고병원성 조류인플루엔자
    "lstkspCl": "", # 축종: 전체
    'ctprvn': '', # 발생지역: 전체
    "legalIctsdGradSe": "" ,# 법정전염병: 전체
}

PAGE_INDEX_XPATH = '//td[contains(text(), "전체 : ")][1]'
XPATH_TABLE_DATA = "/html/body/div[1]/div[2]/div[3]/form[2]/table[4]/tr[2]/td/table"
CSSIGNATURE = 'f8kcFfnwghfIToSYbM6uxQ%3D%3D'
SITE_URL = "https://home.kahis.go.kr/home/lkntscrinfo/selectLkntsOccrrncList.do"
REFERER_URL = "https://home.kahis.go.kr/home/"

# csv와 엑셀 파일을 저장할 폴더 위치
OUTPUT_DIR = 'output'



def fetch_page(page_index, base_params):
    """페이지별 데이터 요청 함수"""
    session = requests.Session()
    
    # 기본 파라미터에 페이지 인덱스 추가
    params = base_params.copy()
    params['pageIndex'] = str(page_index)
    
    # 요청 헤더
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": REFERER_URL,
        "User-Agent": "Mozilla/5.0"
    }
    
    # 랜덤 지연 추가 (서버 부하 방지)
    time.sleep(random.uniform(0.5, 1.5))
    
    try:
        response = session.post(
            SITE_URL, 
            data=params, 
            headers=headers
        )
        response.raise_for_status()  # HTTP 오류 검사
        return response.text
    except Exception as e:
        print(f"페이지 {page_index} 요청 실패: {str(e)}")
        return None



def fetch_and_save_livestock_disease_data(base_params):

    request_params = {
        "csSignature": CSSIGNATURE, # 시그니처
        "turmGubun": "02", # 01: 진단일, 02: 발생일
        "occrFromDt": "2000-01-13", 
        "occrToDt": "2025-03-13", 
        "dissCl": "", # 질병명
        "lstkspCl": "", # 축종 
        'ctprvn': '', # 발생지역
        'signgu': '', # 세부 발생지역
        "legalIctsdGradSe": "" ,# 법정전염병
        **base_params,
    }

    print(request_params)

    # 첫 페이지 요청하여 총 페이지 수 알아내기
    first_page_html = fetch_page(1, request_params)
    root = html.fromstring(first_page_html)

    total_pages_element = root.xpath(PAGE_INDEX_XPATH)[0]
    total_pages_text = total_pages_element.text.strip()
    total_pages = int(re.search(r'\d+(?=쪽\))', total_pages_text).group())
    print(f"전체 페이지수 {total_pages}")
    
    all_data = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 모든 페이지에 대한 요청을 제출
        future_to_page = {
            executor.submit(fetch_page, page, request_params): page
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
                    for _, row in enumerate(table_rows, 1):
                        cells = [td.text_content().strip() for td in row.xpath('.//td')]
                        all_data.append(cells)
                    print(f"페이지 {page} 처리 완료")
            except Exception as e:
                print(f"페이지 {page} 처리 중 오류 발생: {str(e)}")
    
    # 칼럼 이름 정의
    columns = ['Disease', 'Farm', 'Location', 'Date', 'Animal', 'Number', 'Diagnosis', 'End_date']

    # DataFrame 생성
    df = pd.DataFrame(all_data, columns=columns)

    df['Date'] = df['Date'].str.replace('\r', '', regex=False)

    # "Number" 컬럼을 숫자로 변환, 숫자가 아닌 값은 NaN으로 변환
    df['Number'] = pd.to_numeric(df['Number'], errors='coerce')

    # NaN을 0으로 변경 (원하는 경우)
    df['Number'] = df['Number'].fillna(0).astype(int)

    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(os.path.join(OUTPUT_DIR, 'livestock_disease_data.csv'), index=False, encoding='utf-8-sig')
    df.to_excel(os.path.join(OUTPUT_DIR, 'livestock_disease_data.xlsx'), index=False, engine='openpyxl')

    # ---------------저장 확인용 출력---------
    print("CSV 파일로 저장 완료: livestock_disease_data.csv, livestock_disease_data.xlsx")
    print(df)
    # -----------------------


if __name__ == "__main__":

    fetch_and_save_livestock_disease_data(base_params=custom_params)