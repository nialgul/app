import streamlit as st
import sqlite3
import datetime
import time

# -------------------------
# DB 연결
# -------------------------
conn = sqlite3.connect("chat.db", check_same_thread=False)
c = conn.cursor()

# 테이블 생성
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    text TEXT,
    time TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user TEXT PRIMARY KEY,
    last_seen REAL
)
""")

conn.commit()

# -------------------------
# UI 설정
# -------------------------
st.set_page_config(page_title="유챗 스타일 채팅", page_icon="💬")

st.title("💬 유챗 스타일 웹 채팅")

# -------------------------
# 닉네임 입력
# -------------------------
username = st.sidebar.text_input("닉네임", "User")

# -------------------------
# 온라인 상태 업데이트
# -------------------------
now = time.time()

c.execute("INSERT OR REPLACE INTO users (user, last_seen) VALUES (?, ?)", (username, now))
conn.commit()

# 최근 30초 내 접속 = 온라인
online_users = c.execute(
    "SELECT user FROM users WHERE last_seen > ?", (now - 30,)
).fetchall()

st.sidebar.write("🟢 온라인 유저")
for u in online_users:
    st.sidebar.write(f"👉 {u[0]}")

# -------------------------
# 메시지 출력
# -------------------------
st.subheader("채팅")

messages = c.execute("SELECT user, text, time FROM messages ORDER BY id DESC LIMIT 50").fetchall()

for m in reversed(messages):
    st.write(f"**{m[0]}**: {m[1]} ({m[2]})")

# -------------------------
# 메시지 입력
# -------------------------
msg = st.text_input("메시지 입력")

if st.button("전송") and msg:
    c.execute(
        "INSERT INTO messages (user, text, time) VALUES (?, ?, ?)",
        (username, msg, datetime.datetime.now().strftime("%H:%M:%S"))
    )
    conn.commit()
    st.rerun()

# -------------------------
# 자동 새로고침
# -------------------------
time.sleep(2)
st.rerun()
