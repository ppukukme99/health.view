# ────────────── Streamlit + matplotlib 한글 지원 최종본 ──────────────
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

# ----- 업로드한 나눔고딕 폰트 로드 -----
font_path = "fonts/NanumGothic-Regular.ttf"  # GitHub에 업로드한 폰트
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# -------------------- 건강수명 계산 함수 --------------------
def calculate_health_life(exercise_hours):
    if exercise_hours < 0:
        return "오류: 운동시간은 0 이상이어야 합니다!"
    elif exercise_hours < 1:
        health_life = 63 + (exercise_hours * 2)
    elif exercise_hours < 2:
        health_life = 65 + ((exercise_hours - 1) * 2)
    elif exercise_hours < 3:
        health_life = 67 + ((exercise_hours - 2) * 3)
    elif exercise_hours < 4:
        health_life = 70 + ((exercise_hours - 3) * 2)
    else:
        health_life = 72 + ((exercise_hours - 4) * 0.5)
    if health_life > 75:
        health_life = 75
    return round(health_life, 1)

# -------------------- 건강 등급 함수 --------------------
def get_health_grade(health_life):
    if health_life >= 73:
        return "우수"
    elif health_life >= 70:
        return "양호"
    elif health_life >= 67:
        return "보통"
    else:
        return "주의"

# -------------------- Streamlit 인터페이스 --------------------
st.title("🏃‍♂️ 주당 운동시간 건강수명 예측기by 박승리")
st.markdown("---")

# 입력 영역
col1, col2 = st.columns(2)
with col1:
    exercise_hours = st.slider("주당 운동시간 (시간)", 0.0, 10.0, 2.0, 0.1)
with col2:
    st.info("📊 한국 평균: 약 2.5시간")

if st.button("🔍 건강수명 분석하기", type="primary"):
    health_life = calculate_health_life(exercise_hours)

    if isinstance(health_life, str):
        st.error(f"❌ {health_life}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("예상 건강수명", f"{health_life}세")
        with col2:
            grade = get_health_grade(health_life)
            st.metric("건강 등급", grade)

        # 맞춤 조언
        if exercise_hours < 2:
            st.warning("💬 운동시간 부족! 주 2시간 이상!")
        elif exercise_hours < 4:
            st.success("💬 적절한 운동량!")
        else:
            st.balloons()
            st.success("🎉 우수한 운동량!")

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))
        hours = np.linspace(0, 6, 100)
        healths = [calculate_health_life(h) for h in hours]
        ax.plot(hours, healths, 'b-', linewidth=2, label='건강수명 곡선')
        ax.axvline(exercise_hours, color='red', linestyle='--', label=f'당신: {exercise_hours}시간')
        ax.set_xlabel('주당 운동시간', fontproperties=font_prop)
        ax.set_ylabel('건강수명 (세)', fontproperties=font_prop)
        ax.set_title('운동시간 vs 건강수명', fontproperties=font_prop)
        ax.legend(prop=font_prop)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# -------------------- 한국 소득별 실제 데이터 --------------------
st.markdown("### 📈 한국 소득별 실제 데이터")
real_data = pd.DataFrame({
    '소득분위': ['1분위(저)', '3분위(중)', '5분위(고)'],
    '평균운동시간': [1.8, 2.5, 3.2],
    '건강수명': [72.1, 73.5, 75.2]
})
st.dataframe(real_data)

st.caption("✅ 한글 폰트 정상 표시 및 Streamlit + matplotlib 연동 완료")

