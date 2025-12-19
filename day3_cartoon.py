import cv2

# ==========================================
# 👇 [여기만 수정하세요] 변환할 사진 파일 이름
filename = "spongebob.jpg" 
# ==========================================

# 1. 이미지 읽어오기
img = cv2.imread(filename)

if img is None:
    print(f"❌ 에러: '{filename}' 파일을 찾을 수 없어요! 파일명을 확인해주세요.")
    exit()

# 이미지 크기가 너무 크면 처리 속도가 느려지니 살짝 줄이기 (옵션)
# img = cv2.resize(img, (800, 600)) 

print("🎨 AI 화가가 그림을 그리는 중입니다... (잠시만 기다려주세요)")

# 2. [스케치 따기] 사진을 흑백으로 바꾸고, 테두리(Edge)만 남기기
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5) # 잡티(노이즈) 제거
# adaptiveThreshold: 조명에 따라 똑똑하게 테두리를 따주는 함수
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

# 3. [색칠하기] 사진을 뭉개서 만화처럼 단순하게 만들기
# bilateralFilter: 경계선은 살리고, 피부 같은 평면만 뽀샤시하게 뭉개는 고급 필터
color = cv2.bilateralFilter(img, 9, 75, 75)

# 4. [합체] '색칠한 그림' 위에 '테두리' 덮어쓰기
# bitwise_and: 두 이미지를 합치는 마법의 연산
cartoon = cv2.bitwise_and(color, color, mask=edges)

# 5. 결과 보여주기
cv2.imshow("Original", img)
cv2.imshow("Cartoon Filter", cartoon)

# 6. 결과 저장하기 (선택)
cv2.imwrite("my_cartoon_result.jpg", cartoon)
print("✅ 변환 완료! 'my_cartoon_result.jpg'로 저장되었습니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()