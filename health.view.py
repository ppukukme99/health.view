import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===== 한글 깨짐 방지 =====
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ===== 앱 제목 =====
st.title("건강 상태 분석 도구 (Health Pattern Visualizer)")

# ===== 입력부 =====
st.header("1. 주관적 컨디션 입력")

condition = st.slider(
    "오늘의 컨디션(0~10)", 
    min_value=0, 
    max_value=10, 
    value=5
)

sleep_hours = st.number_input("수면 시간(시간)", min_value=0.0, max_value=24.0, value=7.0)

water = st.number_input("물 섭취량(ml)", min_value=0, max_value=5000, value=1500)

stress = st.selectbox("스트레스 수준", ["낮음", "보통", "높음"])

st.write("---")

# ===== 분석 =====
st.header("2. 분석 결과")

# 간단 점수 모델
score = (
    condition * 0.4 +
    (sleep_hours / 8) * 20 +
    (water / 2000) * 20 -
    (10 if stress == "높음" else 0)
)

st.subheader(f"✔ 건강 점수: {score:.1f} / 100")

# ===== 그래프 =====
st.header("3. 비교 그래프")

real_data = pd.DataFrame({
    "항목": ["컨디션", "수면", "수분", "스트레스"],
    "점수": [
        condition * 4,
        (sleep_hours / 8) * 100,
        (water / 2000) * 100,
        30 if stress == "높음" else (70 if stress == "보통" else 100)
    ]
})

fig, ax = plt.subplots()
ax.bar(real_data["항목"], real_data["점수"])
ax.set_ylim(0, 120)
ax.set_ylabel("점수(0~100)")

st.pyplot(fig)

st.write("---")

# ===== 조언 =====
st.header("4. 맞춤 조언")

if score >= 80:
    st.success("전반적으로 매우 좋습니다. 현재 패턴을 유지하세요.")
elif 50 <= score < 80:
    st.info("전체적으로 무난하지만, 수면과 수분 섭취를 조금 더 관리해보세요.")
else:
    st.warning("컨디션이 낮습니다. 수면 확보 및 스트레스 관리가 필요합니다.")

