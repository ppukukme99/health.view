import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 🔥 Streamlit Cloud(리눅스) 한글 깨짐 완전 해결
plt.rcParams['font.family'] = 'DejaVu Sans'   # 리눅스 기본 한글 지원 폰트
plt.rcParams['axes.unicode_minus'] = False    # 마이너스 깨짐 방지

# ------------------ 건강수명 계산 ------------------
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

# ------------------ 등급 계산 ------------------
def get_health_grade(health_life):
    if health_life >= 73:
        return "우수"
    elif health_life >= 70:
        return "양호"
    elif health_life >= 67:
        return "보통"
    else:
        return "주의"

# ------------------ Streamlit UI ------------------
st.title("🏃‍♂️ 주당 운동시간 건강수명 예측기")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    exercise_hours = st.slider("주당 운동시간 (시간)", 0.0, 10.0, 2.0, 0.1)
with col2:
    st.info("📊 한국 평균: 약 2.5시간")

# ------------------ 버튼 클릭 시 분석 ------------------
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

        # 조언
        if exercise_hours < 2:
            st.warning("💬 운동시간 부족! 주 2시간 이상! (건강수명 증가 효과 큼)")
        elif exercise_hours < 4:
            st.success("💬 적절한 운동량! 꾸준히 유지하세요.")
        else:
            st.balloons()
            st.success("🎉 훌륭한 운동량! 과도한 운동은 효과가 줄어듭니다.")

        # ------------------ 그래프 ------------------
        fig, ax = plt.subplots(figsize=(10, 6))
        hours = np.linspace(0, 6, 200)
        healths = [calculate_health_life(h) for h in hours]

        ax.plot(hours, healths, linewidth=2, label='건강수명 변화')
        ax.axvline(exercise_hours, color='red', linestyle='--', label=f'당신의 운동시간 ({exercise_hours}시간)')
        ax.set_xlabel("주당 운동시간(시간)")
        ax.set_ylabel("예상 건강수명(세)")
        ax.set_title("운동시간에 따른 건강수명 변화")
        ax.legend()
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

# ------------------ 실제 데이터 ------------------
st.markdown("### 📈 한국 소득별 운동시간·건강수명 데이터")

real_data = pd.DataFrame({
    '소득분위': ['1분위(저)', '3분위(중)', '5분위(고)'],
    '평균운동시간': [1.8, 2.5, 3.2],
