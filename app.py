import streamlit as st
import json
import difflib

st.set_page_config(page_title="어휘 확장 네트워크 앱", page_icon="🌐")

st.title("🌐 어휘 확장 네트워크 앱")
st.write("단어를 입력하면 연쇄적으로 어휘가 확장됩니다!")

# 데이터 불러오기
with open("vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)

# 형태 변환
def normalize(word):
    if word.endswith("파"):
        return word.replace("파", "픔")
    if word.endswith("러"):
        return word + "움"
    if word.endswith("려"):
        return word.replace("려", "림")
    if word.endswith("해"):
        return word.replace("해", "함")
    return word

# 연쇄 확장 함수
def expand_word(word, vocab):
    result = set()

    if word in vocab:
        first = vocab[word]["관련어"]
        result.update(first)

        for w in first:
            if w in vocab:
                result.update(vocab[w]["관련어"])

    return list(result)

# 유사 단어 추천
def suggest_words(word, vocab):
    return difflib.get_close_matches(word, vocab.keys(), n=5, cutoff=0.5)

word_input = st.text_input("단어를 입력하세요")
word = normalize(word_input)

if word:
    if word in vocab:
        st.subheader(f"'{word}' 어휘 확장")

        st.write("👉 유의어:", ", ".join(vocab[word]["유의어"]))
        st.write("👉 반의어:", ", ".join(vocab[word]["반의어"]))
        st.write("👉 관련어:", ", ".join(vocab[word]["관련어"]))
        st.write("👉 예문:", vocab[word]["예문"])

        st.divider()

        expanded = expand_word(word, vocab)

        st.subheader("🌐 확장된 어휘 네트워크")
        if expanded:
            st.write(", ".join(expanded))
        else:
            st.write("확장된 어휘가 없습니다.")

    else:
        st.warning("사전에 없는 단어예요 😢")

        suggestions = suggest_words(word, vocab)

        if suggestions:
            st.write("👉 혹시 이런 단어인가요?")
            for s in suggestions:
                st.write("-", s)

            st.divider()

            st.subheader("🌐 추천 단어 기반 확장")

            for s in suggestions:
                if s in vocab:
                    st.write(f"'{s}' 관련어:")
                    st.write(", ".join(vocab[s]["관련어"]))
        else:
            st.write("👉 비슷한 단어를 찾지 못했어요.")
