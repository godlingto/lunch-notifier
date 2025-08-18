import os
import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="💡 분야별 아이디어 생성기", page_icon="💡", layout="wide")
st.title("💡 분야별 아이디어 생성기 (Streamlit)")

# ─────────────────────────────────────────────────────────
# 비밀키 로딩: 환경변수(코랩/로컬) → st.secrets(클라우드) 순서
# ─────────────────────────────────────────────────────────
def get_secret(key: str, default: str = "") -> str:
    v = os.getenv(key)
    if v:
        return v
    try:
        return st.secrets[key]  # 배포 시 App Settings > Secrets
    except Exception:
        return default

OPENAI_API_KEY = get_secret("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY가 비어 있습니다. (코랩: os.environ, 배포: App Settings > Secrets)")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ─────────────────────────────────────────────────────────
# 아이디어 생성 함수 (원래 Gradio의 generate_ideas를 그대로 포팅)
# ─────────────────────────────────────────────────────────
def generate_ideas(topic: str, count: int, temperature: float = 0.8) -> str:
    if not topic.strip():
        return "❌ 주제를 입력하세요."
    prompt = (
        f"'{topic}' 분야에서 새로운 아이디어를 {count}개 작성해 주세요.\n"
        "각 아이디어는 간결하고 창의적으로 작성하며, 번호를 붙여 주세요."
    )
    try:
        res = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "당신은 창의적인 아이디어를 제안하는 전문가입니다."},
                {"role": "user", "content": prompt},
            ],
            # temperature=temperature,
        )
        return (res.choices[0].message.content or "").strip()
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

# ─────────────────────────────────────────────────────────
# Streamlit UI
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 설정")
    topic = st.text_input("주제", placeholder="예: 교육, 헬스케어, 환경 보호 등", value="교육")
    count = st.slider("아이디어 개수", min_value=1, max_value=10, value=3, step=1)
    temperature = st.slider("창의성(temperature)", 0.0, 1.2, 0.8, 0.1)
    run = st.button("아이디어 생성")

st.markdown("주제와 개수를 설정한 뒤 **사이드바의 버튼**을 누르세요.")

if run:
    with st.status("아이디어 생성 중...", expanded=False):
        ideas_md = generate_ideas(topic, count, temperature)
    st.subheader("📝 결과")
    st.markdown(ideas_md)
