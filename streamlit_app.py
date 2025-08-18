import streamlit as st

st.title("📌 Streamlit 기본 사용법")  # 큰 제목
st.header("📝 텍스트 출력 예제")  # 헤더
st.subheader("✔️ 다양한 출력 방법")

st.text("이것은 일반 텍스트입니다.")
st.markdown("**이것은 굵은 글씨입니다.**")
st.write("st.write()는 다양한 데이터 타입을 출력할 수 있습니다.")

# 여러 개의 값 출력 가능
st.write("문자열", 123, {"키": "값"})
