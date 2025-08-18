import collections, re
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import Okt
import streamlit as st
from transformers import pipeline

st.set_page_config("텍스트 분석 대시보드(HF)", "🧠", layout="wide")

# ✅ Hugging Face 한국어 감성모델 (NSMC)
#  - 출력 예: [{'label': 'positive', 'score': 0.99}]
clf = pipeline("sentiment-analysis", model="daekeun-ml/koelectra-small-v3-nsmc")

okt = Okt()
STOP = set(["그리고","그러나","하지만","또한","이미","이것","저것","그","것","수","등","및","에서","으로","에게","보다","이다","하다"])

# 테스트 데이터 5가지
SAMPLES = {
 "리뷰A":"배달이 빨랐고 음식이 정말 맛있었습니다. 다시 주문할 의사 있어요!",
 "리뷰B":"가격 대비 품질이 별로였습니다. 양도 적고 포장도 허술했어요.",
 "뉴스A":"도시 재생 프로젝트가 본격화되며 지역 상권에 활기가 돌고 있다.",
 "피드백A":"UI가 직관적이지만 로딩 속도가 느려서 개선이 필요합니다.",
 "일기A":"오늘은 비가 내렸지만 산책을 하니 마음이 한결 편안해졌다."
}

def tokenize_ko(text):
    toks = [w for w,t in okt.pos(text, stem=True) if t in ("Noun","Adjective","Verb")]
    return [w for w in toks if w not in STOP and len(w)>1]

def stats(text):
    toks = tokenize_ko(text)
    return {
        "문자수": len(text),
        "단어수": len(toks),
        "고유단어수": len(set(toks)),
        "평균단어길이": round(np.mean([len(t) for t in toks]) if toks else 0,2)
    }, toks

def freq_df(tokens, topk=20):
    c = collections.Counter(tokens).most_common(topk)
    return pd.DataFrame(c, columns=["단어","빈도"])

def sentiment_hf(text):
    out = clf(text[:512])[0]  # 길면 잘라 처리
    label = "긍정🙂" if out["label"] == "positive" else "부정🙁"
    return label, float(out["score"])

st.title("🧠 텍스트 분석 대시보드 — Hugging Face 한국어 모델 적용")
c1, c2 = st.columns([2,3])

with c1:
    st.subheader("① 텍스트 입력")
    pick = st.selectbox("샘플 선택", list(SAMPLES.keys()))
    text = st.text_area("직접 입력(선택). 비우면 샘플 사용", height=140)
    text = (text or SAMPLES[pick]).strip()
    st.caption("샘플 5가지: " + ", ".join(SAMPLES.keys()))

    st.subheader("② 통계 분석")
    S, toks = stats(text)
    st.dataframe(pd.DataFrame([S]), use_container_width=True)

    st.subheader("③ 빈도 분석")
    topk = st.slider("상위 n 단어", 5, 30, 15)
    fdf = freq_df(toks, topk)
    st.dataframe(fdf, use_container_width=True)

with c2:
    st.subheader("④ 그래프 / 워드클라우드")
    if len(fdf):
        st.bar_chart(fdf.set_index("단어")["빈도"])
        wc = WordCloud(font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
                       background_color="white", width=800, height=300)
        fig = plt.figure(figsize=(8,3)); plt.axis("off")
        plt.imshow(wc.generate_from_frequencies(dict(zip(fdf["단어"], fdf["빈도"]))))
        st.pyplot(fig, use_container_width=True)

    st.subheader("⑤ 감성 분석 (Hugging Face)")
    label, prob = sentiment_hf(text)
    st.metric("감성", label, delta=round((prob*100),2))
    with st.expander("토큰 미리보기"):
        st.write(toks)

st.divider()
st.caption("Flow: 입력 → 통계 → 빈도 → 시각화 → 감성(HF koELECTRA)")
