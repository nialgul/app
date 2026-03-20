import streamlit as st
import datetime
import time

# --- 페이지 설정 ---
st.set_page_config(page_title="구름 웹 메신저", page_icon="☁️", layout="centered")

# --- 하늘색 구름 테마 디자인 (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #87CEEB; }
    .chat-box { background-color: white; padding: 15px; border-radius: 15px; margin-bottom: 10px; border: 1px solid #eee; }
    .stButton>button { background-color: #FFFFFF; color: #87CEEB; border-radius: 20px; width: 100%; }
    .login-pane { background-color: white; padding: 40px; border-radius: 20px; box-shadow: 0px 10px 25px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 세션 상태 초기화 (데이터 유지) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 로그인 화면 ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: white;'>☁️ CLOUD TALK</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-pane">', unsafe_allow_html=True)
        server_ip = st.text_input("서버 IP 주소", value="210.95.17.72")
        user_id = st.text_input("아이디(닉네임)")
        user_pw = st.text_input("비밀번호", type="password")
        
        if st.button("로그인"):
            if user_id and user_pw:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 메인 채팅 화면 ---
else:
    st.markdown(f"<h2 style='color: white;'>☁️ {st.session_state.user_id}님의 구름방</h2>", unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.header("👤 내 정보")
        st.write(f"ID: {st.session_state.user_id}")
        st.selectbox("상태", ["온라인 ☀️", "자리비움 ☁️", "방해금지 🌙"])
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.rerun()

    # 채팅 메시지 출력
    chat_container = st.container(height=500)
    for msg in st.session_state.messages:
        chat_container.markdown(f"""
            <div class="chat-box">
                <b style="color: #87CEEB;">{msg['user']}</b> <small style="color: gray;">{msg['time']}</small><br>
                {msg['text']}
            </div>
        """, unsafe_allow_html=True)

    # 메시지 입력창
    with st.form("send_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        input_text = col1.text_input("메시지 입력", label_visibility="collapsed")
        if col2.form_submit_button("전송") and input_text:
            now = datetime.datetime.now().strftime("%H:%M")
            st.session_state.messages.append({"user": st.session_state.user_id, "text": input_text, "time": now})
            st.rerun()
