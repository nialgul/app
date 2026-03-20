import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time

# -------------------
# Firebase 연결
# -------------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred, {
        "databaseURL": st.secrets["firebase_db_url"]
    })

# -------------------
# 기본 설정
# -------------------
st.set_page_config(page_title="유챗", page_icon="💬")
st.title("💬 유챗 (실시간 채팅)")

# -------------------
# 사용자 설정
# -------------------
username = st.sidebar.text_input("닉네임", value="User")

# -------------------
# 온라인 유저 등록
# -------------------
online_ref = db.reference("online")

if username:
    online_ref.child(username).set({
        "time": str(datetime.now())
    })

# -------------------
# 메시지 가져오기
# -------------------
chat_ref = db.reference("chat")
messages = chat_ref.get()

# -------------------
# 채팅 출력
# -------------------
st.subheader("💬 채팅")

chat_box = st.container(height=400)

with chat_box:
    if messages:
        for key, msg in messages.items():
            st.markdown(f"**{msg['user']}**: {msg['text']}")

# -------------------
# 메시지 입력
# -------------------
msg = st.text_input("메시지 입력")

if st.button("전송"):
    if msg and username:
        chat_ref.push({
            "user": username,
            "text": msg,
            "time": str(datetime.now())
        })
        st.rerun()

# -------------------
# 온라인 유저 표시
# -------------------
st.subheader("👥 접속자")

online_users = online_ref.get()

if online_users:
    for user in online_users:
        st.write(f"🟢 {user}")

# -------------------
# 자동 새로고침
# -------------------
time.sleep(2)
st.rerun()
