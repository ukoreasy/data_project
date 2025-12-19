# 🚀 My AI & Web Project Playground

이 저장소는 **AI 기술(OpenCV, Data Analysis)**을 **웹 서비스(Flask)**에 적용해보는 학습 프로젝트입니다.
매일 새로운 기능을 하나씩 구현하며 스펙트럼을 넓혀가고 있습니다.

---

## 📅 프로젝트 기록

### [Day 3] AI 화가 필터 (Cartoon Filter) 🎨 (2025.12.19)
OpenCV의 이미지 필터링 기술을 활용하여 일반 사진을 웹툰 그림체로 변환하는 프로젝트입니다.

- **핵심 기술:**
    - **Adaptive Thresholding:** 이미지의 윤곽선(Edge)을 검출하여 스케치 효과 구현
    - **Bilateral Filter:** 엣지는 보존하면서 피부 등 면적 부분만 뭉개는(Blur) 회화적 효과
    - **Bitwise Operation:** 스케치와 채색된 이미지를 비트 연산으로 합성
- **주요 기능:**
    - 사용자 사진 입력 시 자동으로 만화 화풍으로 변환 및 저장

### [Day 2] AI 퍼스널 컬러 진단기 🎨 (2025.12.19)
사용자의 얼굴 사진을 분석하여 **웜톤(Warm)**과 **쿨톤(Cool)**을 진단해주는 서비스입니다.

- **핵심 기술:**
    - **OpenCV:** Haar Cascade로 얼굴 위치 탐지, ROI 추출
    - **Color Space:** RGB를 **Lab 색공간**으로 변환하여 `b` 채널(Yellow vs Blue) 분석
    - **Logic:** 피부 색상 값을 통계적으로 분석하여 톤 판별
- **주요 기능:**
    - 사진 업로드 시 얼굴 자동 인식 및 크롭
    - 진단 결과에 따른 맞춤형 스타일링 코멘트 (배경색 변경)

### [Day 1] 학생 성적 관리 & 밝기 분석 📊 (2025.12.18)
학생들의 성적 데이터를 시각화하고, 증명사진의 밝기를 분석하는 기초 서비스입니다.

- **핵심 기술:** Pandas, Matplotlib, OpenCV (Grayscale)
- **주요 기능:**
    - CSV 데이터 연동 및 성적 그래프 시각화
    - 이미지 평균 밝기 계산 알고리즘

---

## 🛠️ 기술 스택 (Tech Stack)
- **Language:** Python 3.10
- **Web Framework:** Flask
- **AI/Vision:** OpenCV, Numpy
- **Data:** Pandas, Matplotlib
- **Deploy:** Ngrok

---

## 🏃‍♂️ 실행 방법 (How to run)

1. **가상환경 활성화**
   ```bash
   .\venv\Scripts\activate