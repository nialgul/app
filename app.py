import streamlit as st
import datetime

# --- 페이지 디자인 ---
st.set_page_config(page_title="구름 웹 메신저", page_icon="☁️")

st.markdown("""
    <style>
    .stApp { background-color: #87CEEB; }
    .chat-bubble { 
        background-color: white; 
        padding: 15px; 
        border-radius: 20px; 
        margin-bottom: 10px; 
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 저장소
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 화면 구성 ---
st.title("☁️ 구름 웹 메신저")

# 채팅창
with st.container(height=400):
    for m in st.session_state.messages:
        st.markdown(f"""
            <div class="chat-bubble">
                <b style="color:#87CEEB;">{m['user']}</b> <small>{m['time']}</small><br>
                {m['text']}
            </div>
        """, unsafe_allow_html=True)

# 메시지 입력
with st.form("msg_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    user_id = st.sidebar.text_input("닉네임", value="익명")
    user_input = col1.text_input("메시지 입력", label_visibility="collapsed")
    if col2.form_submit_button("전송") and user_input:
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"user": user_id, "text": user_input, "time": now})
        st.rerun()
