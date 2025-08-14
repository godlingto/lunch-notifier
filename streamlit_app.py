# 파일명: app.py
import streamlit as st

aurora_html = """
<div style="
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background:
    radial-gradient(circle at 30% 30%, rgba(0, 255, 255, 0.5) 0%, transparent 70%),
    radial-gradient(circle at 70% 40%, rgba(255, 0, 255, 0.5) 0%, transparent 70%),
    radial-gradient(circle at 50% 80%, rgba(0, 255, 127, 0.5) 0%, transparent 70%);
  filter: blur(100px);
  z-index: 0;
  pointer-events: none;
  animation: auroraAnim 10s infinite alternate;
">
</div>

<style>
@keyframes auroraAnim {
  0% { transform: translate(0px, 0px); }
  100% { transform: translate(-30px, 30px); }
}
</style>
"""

# Streamlit 다크모드 강제 해제해보기
st.set_page_config(page_title="오로라", layout="wide", initial_sidebar_state="auto")

st.markdown(aurora_html, unsafe_allow_html=True)

st.title("✅ 오로라 효과 디버그 버전 V0.2")
st.write("배경에 형광색 오로라가 퍼지고 움직여야 정상입니다.")
