import csv


def read_csv(filename):
    data = []
    with open("data.csv",newline='',encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["age"] = int(row["age"])
            row["score"] = int(row["score"])
            data.append(row)
    return data


#평균점수계산
def average_score(data):
    return sum(p["score"] for p in data) / len(data)

#조건 필터링
def filter_scores(data,threshold=85):
    return [p for p in data if p["score"]>=threshold]
#평균 이상 학생
def above_average(data, avg):
    return [p for p in data if p["score"]>avg]

#나이순 정렬
def sort_by_age(data):
    return sorted(data, key=lambda x: x["age"])


def save_csv(data, filename):
    with open(filename, "w", newline = '', encoding = "utf-8") as f:
        fieldnames = ["name", "age", "score"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in data:
            writer.writerow(p)
def main():
    data = read_csv("data.csv")
    print("전체 데이터: ", data)

    avg = average_score(data)
    print("전체평균점수:",avg)

    high_scores = filter_scores(data,85)
    print("\n점수 85이상 학생: ")

    for p in high_scores:
        print(p["name"], p["score"])
    save_csv(high_scores, "high_scores.csv")
    
    above_avg_students= above_average(data,avg)
    print("\n평균 이상 학생")
    for p in above_avg_students:
        print(p["name"], p["score"])
    save_csv(above_avg_students, "above_avg.csv")

    sorted_students = sort_by_age(data)
    print("\n나이순 정렬")
    for p in sorted_students:
        print(p["name"], p["age"], p["score"])
    
    print("\ncsv 파일 생성완료")
if __name__ == "__main__":
    main()


