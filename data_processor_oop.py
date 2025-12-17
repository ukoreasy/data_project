#data_processor_oop.py
import csv
import matplotlib.pyplot as plt


# 1. DataProcessor 클래스 정의
class DataProcessor:
    # 2. 생성자: 객체가 만들어질 때 (DataProcessor("data.csv")) 딱 한 번 실행됨
    def __init__(self, filename):
        # 데이터를 한 번 읽어서 'self.data'라는 클래스 내부 변수에 저장합니다.
        # 이제 다른 메서드들은 self.data를 통해 이 데이터에 접근합니다.
        self.data = self._read_csv(filename)
        self.filename = filename
        
    # **Helper Method:** 파일 읽기는 클래스 외부에서 호출할 필요가 없으므로 _(언더바)를 붙여 내부에서만 사용하도록 관례적으로 표시합니다.
    def plot_score_distribution(self):
        scores = [p['score'] for p in self.data]
        names = [p['name'] for p in self.data]
        
        plt.figure(figsize=(8, 5))
        plt.bar(names, scores, color='skyblue')
        plt.xlabel("학생 이름")
        plt.ylabel("점수")
        plt.title("학생별 점수 분포")
        
        # 그래프를 이미지 파일로 저장
        plt.savefig("score_distribution.png")
        print("\n[시각화] 'score_distribution.png' 파일 생성 완료")
    def _read_csv(self, filename):
        data = []
        with open(filename, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 데이터 타입 변환은 여기서 처리하여 데이터의 일관성을 유지합니다.
                row["age"] = int(row["age"])
                row["score"] = int(row["score"])
                data.append(row)
        return data
    
    def calculate_average(self):
        if not self.data:
            return 0
        return sum(p["score"] for p in self.data) / len(self.data)
    #조건 필터링
    def filter_scores(self,threshold=85):
        return [p for p in self.data if p["score"]>=threshold]
   
    #평균 이상 학생
    def above_average(self):
        avg = self.calculate_average()
        return [p for p in self.data if p["score"]>avg]
    
    #나이순 정렬
    def sort_by_age(self):
        return sorted(self.data, key=lambda x: x["age"])
    
    def save_csv(self, data_to_save, output_filename):
        with open(output_filename, "w", newline = '', encoding = "utf-8") as f:
            fieldnames = ["name", "age", "score"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_save)
def main():
    processor = DataProcessor("data.csv")
    avg = processor.calculate_average()
    print("전체 데이터 평균 점수: ", avg)
    high_scores = processor.filter_scores(85)
    print("\n점수 85점 이상 학생:", high_scores)
    processor.save_csv(high_scores, "high_scores_oop.csv")
    above_avg_students = processor.above_average()
    print("\n평균 이상 학생:", above_avg_students)
    processor.save_csv(above_avg_students, "above_avg_oop.csv")
    sorted_students = processor.sort_by_age()
    print("\n나이순 정렬 (전체):", sorted_students)
    processor.plot_score_distribution()
    
if "__main__" == "__main__":
    main()