from flask import Flask, request, jsonify, send_file, send_from_directory

from fetch_and_save_livestock_disease import fetch_and_save_livestock_disease_data

import concurrent.futures
import os

executor = concurrent.futures.ThreadPoolExecutor()

app = Flask(__name__)
app.json.ensure_ascii = False

OPTIONS = {
    "dissCl": {
        "": "전체",
        "0007": "가금티푸스",
        "0099": "결핵병",
        "0111": "고병원성 조류인플루엔자",
        "0191": "구제역",
        "0333": "뉴캣슬병",
        "0406": "돼지생식기호흡기증후군",
        "0412": "돼지열병",
        "0418": "돼지오제스키병",
        "0504": "사슴만성소모성질병",
        "0683": "브루셀라병",
        "1442": "추백리",
        "0296": "낭충봉아부패병",
        "1003": "아프리카돼지열병",
        "0446": "럼피스킨"
    },
    "lstkspCl": {
        "": "전체",
        "4120": "소",
        "4141": "산양",
        "4142": "면양",
        "4130": "돼지",
        "4150": "닭",
        "4184": "사슴",
        "4162": "오리",
        "4163": "거위",
        "4161": "칠면조",
        "4164": "메추리",
        "4186": "벌",
        "4143": "염소"
    },
    "ctprvn": {
        "": "전체",
        "11": "서울특별시",
        "26": "부산광역시",
        "27": "대구광역시",
        "28": "인천광역시",
        "29": "광주광역시",
        "30": "대전광역시",
        "31": "울산광역시",
        "36": "세종특별자치시",
        "41": "경기도",
        "51": "강원특별자치도",
        "43": "충청북도",
        "44": "충청남도",
        "52": "전북특별자치도",
        "46": "전라남도",
        "47": "경상북도",
        "48": "경상남도",
        "50": "제주특별자치도"
    },
    "legalIctsdGradSe": {
        "": "전체",
        "1": "1종",
        "2": "2종",
        "3": "3종"
    }
}

@app.route("/")
def index():
    return send_from_directory("./front/dist", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("./front/dist", path)

@app.route('/api/options', methods=['GET'])
def get_options():
    return jsonify(OPTIONS)

@app.route('/api/v1/animal-disease-report', methods=['POST'])
def generate_params():
    data = request.get_json()
    # params = create_params(data):
    selected_term = data.get('turmGubun', '01') # 선택지
    disease_code = data.get('dissCl', '') # 질병 코드 
    start_date = data.get('occrFromDt') # 시작일
    end_date = data.get('occrToDt') # 종료일

    if not start_date or not end_date:
        return jsonify({"error": "조회 기간 (시작일, 종료일)은 필수 입력 항목입니다."}), 400

    animal_kind = data.get('lstkspCl', '') # 축종 동물
    region = data.get('ctprvn', '') # 지역(도)
    disease_grade = data.get('legalIctsdGradSe', '') # 법정전염병명

    params = {
        'csSignature': 'f8kcFfnwghfIToSYbM6uxQ%3D%3D',
        'turmGubun': selected_term,
        'occrFromDt': start_date,
        'occrToDt': end_date,
        'dissCl': disease_code,
        'lstkspCl': animal_kind,
        'ctprvn': region,
        'signgu': "",
        'legalIctsdGradSe': disease_grade
    }

    future = executor.submit(fetch_and_save_livestock_disease_data, base_params=params)
    concurrent.futures.wait([future])

    directory = './output'
    if not os.path.isfile(f'{directory}/livestock_disease_data.xlsx'):
        return jsonify({"error": "File not found"}), 404

    return send_file(
        f'{directory}/livestock_disease_data.xlsx', 
        as_attachment=True,
        download_name='livestock_disease_data.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/download')
def download_file():
    path = "./output/livestock_disease_data.xlsx"  # 다운로드할 파일 경로
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
