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
def average_score(data):
    return sum(p["score"] for p in data) / len(data)


def filter_scores(data,threshold=85):
    return [p for p in data if p["score"]>=threshold]

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
    above_avg = [p for p in data if p["score"]>avg]
    sorted_by_age = sorted(data, key=lambda x: x["age"])
    print("\nhigh_scores.csv 파일 생성완료")
if __name__ == "__main__":
    main()


