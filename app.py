import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase.json")  # 키파일
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://YOUR-DATABASE.firebaseio.com/'
    })

st.set_page_config(page_title="유챗", page_icon="💬")

st.title("💬 실시간 채팅 (유챗 스타일)")

# 닉네임
user = st.sidebar.text_input("닉네임", value="User")

# 메시지 입력
msg = st.text_input("메시지 입력")

if st.button("전송") and msg:
    ref = db.reference("chat")
    ref.push({
        "user": user,
        "text": msg
    })

# 채팅 불러오기
chat_box = st.container()

while True:
    with chat_box:
        st.empty()
        ref = db.reference("chat")
        messages = ref.get()

        if messages:
            for key in messages:
                m = messages[key]
                st.write(f"**{m['user']}**: {m['text']}")

    time.sleep(2)
    st.rerun()
