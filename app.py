
import csv
import os
import cv2  # OpenCV (이미지 분석용)
from flask import Flask, render_template, request 
from pyngrok import ngrok
from analysis import analyze_personal_color

# ---------------------------------------------------------
# 👇 [중요] 아까 발급받은 Ngrok 토큰을 따옴표 안에 넣으세요!
# 예: ngrok.set_auth_token("2AwX...")
ngrok.set_auth_token("36y9nODXgCAFuRGWfbOPN8dl10n_59fz5twTqPdncEY2ZM32")
# ---------------------------------------------------------

app = Flask(__name__)

# 🌍 Ngrok으로 외부 접속 주소 만들기 (포트 5000번)
try:
    public_url = ngrok.connect(5000).public_url
    print(f"\n * 🌍 내 사이트 접속 주소 (친구에게 공유 가능!): {public_url} \n")
except Exception as e:
    print(f"Ngrok 연결 오류 (무시 가능): {e}")

# 🛠️ 이미지 밝기 분석 함수 (OpenCV)
def analyze_image_brightness(image_path):
    # 이미지를 흑백으로 읽기
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        return None
    
    # 평균 밝기 계산 (소수점 둘째 자리까지)
    return round(cv2.mean(image)[0], 2)

# 🏠 메인 페이지 (데이터 보여주기)
@app.route('/')
def home():
    data = []
    # CSV 파일 읽어서 데이터 가져오기
    if os.path.exists('extended_data_with_brightness.csv'):
        with open('extended_data_with_brightness.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
            
    # 그래프 그리기용 리스트 만들기
    names = [row['name'] for row in data]
    scores = [int(row['score']) for row in data]
    brightness_values = [float(row['brightness']) for row in data]
    
    return render_template('index.html', 
                           students=data,
                           names=names,
                           scores=scores,
                           brightness_values=brightness_values)
@app.route('/color', methods=['GET', 'POST'])
def color_page():
    if request.method == 'GET':
        # 그냥 접속했을 때는 화면만 보여줌
        return render_template('color.html')
    
    # 사진을 업로드하고 버튼을 눌렀을 때 (POST)
    if request.method == 'POST':
        if 'file' not in request.files:
            return "파일이 없습니다."
        
        file = request.files['file']
        if file.filename == '':
            return "파일을 선택해주세요."

        # 1. 파일 저장
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # 2. AI 분석 엔진 가동! (우리가 만든 함수 호출)
        # analysis.py의 함수가 (결과문자열, 점수) 두 개를 돌려줍니다.
        result_text, score = analyze_personal_color(filepath)
        
        # 3. 결과에 따른 맞춤형 코멘트 (비즈니스 로직)
        if "쿨톤" in result_text:
            desc = "당신은 쿨톤! ❄️ 시크한 블랙이나 쨍한 화이트, 실버 액세서리가 찰떡입니다. LG 트윈스 유광 잠바가 아주 잘 어울리시겠네요!"
            color_code = "#E3F2FD" # 연한 파랑 배경
        else:
            desc = "당신은 웜톤! ☀️ 따뜻한 베이지, 브라운, 골드 액세서리가 분위기를 살려줍니다. 가을 분위기 미남이시군요!"
            color_code = "#FFF3E0" # 연한 주황 배경

        # 4. 결과 화면 보여주기
        return render_template('color.html', 
                               result=result_text, 
                               score=score,
                               desc=desc,
                               bg_color=color_code)

# 📸 파일 업로드 및 분석 처리 (POST 요청)
@app.route('/upload', methods=['POST'])
def upload_file():
    # 1. 사용자가 보낸 파일 받기
    if 'file' not in request.files:
        return "파일이 없습니다."
        
    file = request.files['file']
    
    if file.filename == '':
        return "파일을 선택하지 않았습니다."

    if file:
        # 2. 파일을 'uploads' 폴더에 저장
        if not os.path.exists('uploads'):
            os.makedirs('uploads')  # 폴더가 없으면 생성
        
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # 3. 저장된 파일 OpenCV로 분석
        brightness = analyze_image_brightness(filepath)
        
        # 4. 결과 보여주기 (기존 그래프 데이터도 같이 보내야 화면이 안 깨짐)
        # --- (기존 데이터 읽기 반복) ---
        data = []
        if os.path.exists('extended_data_with_brightness.csv'):
            with open('extended_data_with_brightness.csv', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader: data.append(row)
        
        names = [row['name'] for row in data]
        scores = [int(row['score']) for row in data]
        brightness_values = [float(row['brightness']) for row in data]
        # -----------------------------

        # index.html을 다시 띄우되, 이번엔 result_brightness(결과값)을 추가로 보냄!
        return render_template('index.html', 
                               students=data,
                               names=names,
                               scores=scores,
                               brightness_values=brightness_values,
                               result_brightness=brightness)

if __name__ == '__main__':
    app.run(port=5000)