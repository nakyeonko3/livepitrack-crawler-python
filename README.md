# 법정가축전염병 사이트 크롤링

## 목표

- 법정가축전염병 사이트에서 발생 데이터를 크롤링하여 저장

## 기술 스텍

### python
- Python 3.10.10
- requests 2.32.3
- pandas 2.2.3
- lxml 5.3.1
- openpyxl 3.1.5
- playwright 1.50.0

## 실행 방법

1. 가상환경 생성
```
python -m venv .venv
```

1. 가상환경 활성화
```
.venv\Scripts\activate
```

1. 필요한 패키지 설치
```
pip install -r requirements.txt
```

설치가 안되면
```bash
pip install requests lxml openpyxl playwright
```

playwright 설치하기
```bash
pip install pytest-playwright
playwright install
```


4. 실행
```bash
python index.py
```

5. 실행 결과
output 폴더에 csv와 excel 파일이 생성됨.


## 커스텀하는 방법(질병명, 날짜, 발생지역등을 바꿔서 크롤링하고 싶을 때)

## 방법
1. index.py 코드 확인하기
2. custom_params 변수값 확인하기 아래 `custom_params 변수값 분석`을 참고해서 커스텀을 할 수 있음
![Image](https://i.imgur.com/NK0fh1U.png)
3. custom_params 변수값을 바꿔서 크롤링
예시
```python
# custom_params 설정
# 기본 파라미터 설정 (사용자 입력 기반)
custom_params = { 
    "turmGubun": "02", # 02: 발생일
    "occrFromDt": "2000-01-13", # 시작일
    "occrToDt": "2025-03-13", # 종료일
    "dissCl": "0504", # 질병명: 사슴만성소모성질병
    "lstkspCl": "", # 축종: 전체
    'ctprvn': '', # 발생지역: 전체
    "legalIctsdGradSe": "" ,# 법정전염병: 전체
}
```


## custom_params 변수값 분석

| 키               | 값                           | 설명                             |
|------------------|------------------------------|----------------------------------|
| csSignature      | f8kcFfnwghfIToSYbM6uxQ%3D%3D | 시그니처                         |
| turmGubun        | 01                           | 발생일(01), 진단일(02) 선택        |
| occrFromDt       | 2024-03-13                   | 시작일                          |
| occrToDt         | 2025-03-13                   | 종료일                          |
| dissCl           | "0007"                       | 질병명(질병코드)                           |
| ctprvn           | ""                           | 발생지역                         |
| lstkspCl         | ""                           | 축종(가축)                         |
| legalIctsdGradSe | ""                           | 법정전염병                       |


### cssSignature
- **무시해도 되는 값**

### turmGubun
- "01": 진단일을 기준으로 검색
- "02": 발생일을 기준으로 검색

### occrFromDt
- "YYYY-MM-DD" 
- 발생일자(시작) or 진단일자(시작)

### occrToDt
- "YYYY-MM-DD" 
- 발생일자(종료) or 진단일자(종료)

### dissCI
- 질병명
- "" : 전체
- "0007" : 가금티푸스
- "0099" : 결핵병
- "0111" : 고병원성 조류인플루엔자
- "0191" : 구제역
- "0333" : 뉴캣슬병
- "0406" : 돼지생식기호흡기증후군
- "0412" : 돼지열병
- "0418" : 돼지오제스키병
- "0504" : 사슴만성소모성질병
- "0683" : 브루셀라병
- "1442" : 추백리
- "0296" : 낭충봉아부패병 
- "1003" : 아프리카돼지열병
- "0446" : 럼피스킨

### ctprvn	 
- 발생 지역
- "" : 전체
- "11" : 서울특별시
- "26" : 부산광역시
- "27" : 대구광역시
- "28" : 인천광역시
- "29" : 광주광역시
- "30" : 대전광역시
- "31" : 울산광역시
- "36" : 세종특별자치시
- "41" : 경기도
- "51" : 강원특별자치도
- "43" : 충청북도
- "44" : 충청남도
- "52" : 전북특별자치도
- "46" : 전라남도
- "47" : 경상북도
- "48" : 경상남도
- "50" : 제주특별자치도

### signgu
- 세부 발생 지역
- "" : 전체

### lstkspCl
- 축종
- "" : 전 체
- "4120" : 소
- "4141" : 산양
- "4142" : 면양
- "4130" : 돼지
- "4150" : 닭
- "4184" : 사슴
- "4162" : 오리
- "4163" : 거위
- "4161" : 칠면조
- "4164" : 메추리
- "4186" : 벌
- "4143" : 염소

### legalIctsdGradSe
- 법정전염병명
- "" : 전체
- "1" : 1종
- "2" : 2종
- "3" : 3종