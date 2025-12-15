import csv
data = []
with open("data.csv",newline='',encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["age"] = int(row["age"])
        row["score"] = int(row["score"])
        data.append(row)
print(data)

total = sum(person["score"] for person in data)
avg = total / len(data)
print("평균 점수:",  avg)

high_scores = [p for p in data if p["score"] >= 85]
for p in high_scores:
    print(p["name"], p["score"])