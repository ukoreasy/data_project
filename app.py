
import csv
import os
import cv2  # OpenCV (이미지 분석용)
from flask import Flask, render_template, request 
from pyngrok import ngrok

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