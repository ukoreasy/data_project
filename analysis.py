import cv2
import numpy as np
import os
import urllib.request

# 1. 얼굴 인식 모델 준비
cascade_filename = 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_filename):
    url = 'https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml'
    urllib.request.urlretrieve(url, cascade_filename)

def analyze_personal_color(image_path):
    # 이미지 읽기
    img = cv2.imread(image_path)
    if img is None:
        return "이미지 오류", 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade_filename)
    
    # 얼굴 찾기 시도
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("⚠️ 얼굴 인식 실패! (전체 이미지 분석함)")
        target_area = img
    else:
        print(f"✅ 얼굴 {len(faces)}개 발견! (중앙부만 잘라냄)")
        x, y, w, h = faces[0]
        
        # [핵심 수정] 얼굴 박스의 정중앙 50%만 잘라냅니다.
        # 머리카락, 배경, 옷을 제외하고 '피부'만 남기기 위함입니다.
        center_x = x + int(w * 0.25)
        center_y = y + int(h * 0.25)
        center_w = int(w * 0.5)
        center_h = int(h * 0.5)
        
        target_area = img[center_y:center_y+center_h, center_x:center_x+center_w]

    # 👇 [디버깅] 컴퓨터가 분석한 영역을 사진으로 저장해서 눈으로 확인하자!
    cv2.imwrite('debug_face.jpg', target_area)
    print("📸 분석한 영역을 'debug_face.jpg'로 저장했습니다. 확인해보세요!")

    # --- Lab 색공간 분석 (파랑 vs 노랑) ---
    lab_img = cv2.cvtColor(target_area, cv2.COLOR_BGR2Lab)
    L, a, b = cv2.split(lab_img)
    
    b_mean = np.mean(b)
    
    # 동양인 피부 기준값 (조절 가능)
    threshold = 143 

    print(f"📊 b값(노란끼): {b_mean:.2f} (기준: {threshold})")

    if b_mean > threshold:
        return "웜톤 (Warm)", b_mean
    else:
        return "쿨톤 (Cool)", b_mean

# 실행
if __name__ == "__main__":
    result, score = analyze_personal_color("test.jpg") 
    print(f"결과: {result}")