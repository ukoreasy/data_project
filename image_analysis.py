#image_analysis.py
import csv
import cv2 
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows 기준)
font_path = 'C:/Windows/Fonts/malgun.ttf'
try:
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
except:
    print("한글 폰트 설정 실패: 기본 폰트로 진행합니다.")

class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._read_csv(filename)
        
    def _read_csv(self, filename):
        data = []
        try:
            with open(filename, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["age"] = int(row["age"])
                    row["score"] = int(row["score"])
                    data.append(row)
        except FileNotFoundError:
            print(f"오류: {filename} 파일을 찾을 수 없습니다.")
        return data
    
    def calculate_average(self):
        if not self.data:
            return 0
        return sum(p["score"] for p in self.data) / len(self.data)

    def filter_scores(self, threshold=85):
        return [p for p in self.data if p["score"] >= threshold]
   
    def above_average(self):
        avg = self.calculate_average()
        return [p for p in self.data if p["score"] > avg]
    
    def sort_by_age(self):
        return sorted(self.data, key=lambda x: x["age"])
    
    def plot_score_distribution(self):
        scores = [p['score'] for p in self.data]
        names = [p['name'] for p in self.data]
        
        plt.figure(figsize=(8, 5))
        plt.bar(names, scores, color='skyblue')
        plt.xlabel("학생 이름")
        plt.ylabel("점수")
        plt.title("학생별 점수 분포")
        plt.savefig("score_distribution.png")
        print("\n[시각화] 'score_distribution.png' 파일 생성 완료")

    # 💡 save_csv 업그레이드: 필드명(fieldnames)을 밖에서 받아올 수 있게 수정
    def save_csv(self, data_to_save, output_filename, fieldnames=None):
        if fieldnames is None:
            fieldnames = ["name", "age", "score"] # 기본값
            
        with open(output_filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_save)

# -----------------------------------------------------
# 💡 4주차 핵심: 이미지 분석 기능 (OpenCV)
# -----------------------------------------------------

def analyze_image_brightness(image_path):
    """이미지 경로를 받아 평균 명암도(밝기)를 계산하여 반환합니다."""
    # 이미지를 흑백으로 읽기
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) 
    
    if image is None:
        if not os.path.exists(image_path):
            print(f"❌ 파일 없음: {image_path}")
        else:
            print(f"❌ 로드 실패 (파일 손상 가능성): {image_path}")
        return None

    # 평균 밝기 계산
    average_brightness = cv2.mean(image)[0]
    return average_brightness

def process_image_integration(processor, image_folder="sample_images"):
    """기존 데이터에 이미지 분석 결과를 합칩니다."""
    
    # 원본 데이터 복사 (원본 훼손 방지)
    extended_data = [p.copy() for p in processor.data]
    
    print(f"\n--- '{image_folder}' 폴더에서 이미지 분석 시작 ---")
    
    for person in extended_data:
        # data.csv의 이름(name)을 이용해 이미지 파일 경로 생성 (예: sample_images/kim.jpg)
        img_file = os.path.join(image_folder, f"{person['name']}.jpg") 
        
        brightness = analyze_image_brightness(img_file)
        
        if brightness is not None:
            print(f"✅ {person['name']}: 밝기 {brightness:.2f}")
            person['brightness'] = round(brightness, 2)
        else:
            print(f"⚠️ {person['name']}: 이미지 분석 실패 (밝기 0 처리)")
            person['brightness'] = 0
            
    return extended_data

# -----------------------------------------------------
# 메인 실행
# -----------------------------------------------------

def main():
    # 1. 데이터 로드
    processor = DataProcessor("data.csv")
    print(f"기존 데이터 로드 완료: {len(processor.data)}명")

    # 2. 이미지 데이터 통합 실행
    # (주의: sample_images 폴더에 kim.jpg, lee.jpg 등이 있어야 함)
    extended_data = process_image_integration(processor, image_folder="sample_images")
    
    # 3. 결과 확인
    print("\n[최종 통합 데이터]")
    for row in extended_data:
        print(row)

    # 4. CSV 저장
    # 'brightness'라는 새로운 열이 추가되었으므로 fieldnames를 명시해줍니다.
    fieldnames_extended = ["name", "age", "score", "brightness"]
    processor.save_csv(extended_data, "extended_data_with_brightness.csv", fieldnames_extended)
    print("\n[완료] 'extended_data_with_brightness.csv' 파일이 생성되었습니다.")

if __name__ == "__main__":
    main()