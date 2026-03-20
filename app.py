import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(page_title="구름 웹 메신저", page_icon="☁️")

# --- 디자인 스타일 ---
st.markdown("""
<style>
.stApp {
    background-color: #87CEEB;
}
.chat-bubble {
    background-color: white;
    padding: 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# 세션 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 제목
st.title("☁️ 구름 웹 메신저")

# 채팅 출력
with st.container(height=450):
    for m in st.session_state.messages:
        st.markdown(
            f'<div class="chat-bubble"><b>{m["user"]}</b>: {m["text"]}</div>',
            unsafe_allow_html=True
        )

# 입력 폼
with st.form("send", clear_on_submit=True):
    u_id = st.sidebar.text_input("닉네임", value="User")
    msg = st.text_input("메시지 입력")

    if st.form_submit_button("전송") and msg:
        st.session_state.messages.append({
            "user": u_id,
            "text": msg
        })
        st.rerun()
