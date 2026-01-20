import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import streamlit.components.v1 as components

# --- 1. 安全加密工具 ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# 密碼 666 的加密值
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

# --- 2. 初始化狀態 ---
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT AI Assistant"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "show_robot_menu" not in st.session_state:
    st.session_state.show_robot_menu = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 3. 核心 CSS 樣式 (含手機優化) ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .nav-header {
        background-color: #1a1a1a;
        padding: 15px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        margin-bottom: 20px;
        border-bottom: 4px solid #004a99;
    }
    .robot-box {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        background-color: #fcfcfc;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    @media (max-width: 600px) {
        .stButton>button { width: 100% !important; }
    }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導覽列 ---
st.markdown(f"<div class='nav-header'><div style='font-size: 20px; font-weight: 700;'>TM ROBOT | Data Hub</div></div>", unsafe_allow_html=True)

# --- 5. 側邊欄與管理員選單 ---
with st.sidebar:
    st.markdown("### ⚙️ System Control")
    curr_user = st.session_state.logged_in_user
    
    with st.popover(f"👤 {curr_user.upper()}"):
        if curr_user == "guest":
            u = st.text_input("Admin ID")
            p = st.text_input("Password", type="password")
            if st.button("Login"):
                if u == "admin" and check_hashes(p, ADMIN_HASH):
                    st.session_state.logged_in_user = "admin"
                    st.rerun()
                else:
                    st.error("Invalid")
        else:
            if st.button("Logout"):
                st.session_state.logged_in_user = "guest"
                st.rerun()

    if st.session_state.logged_in_user == "admin":
        st.markdown("---")
        st.markdown("#### 📋 Activity Logs")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), hide_index=True)
            if st.button("Clear Logs"):
                st.session_state.search_history = []
                st.rerun()
        else:
            st.info("No logs.")

# --- 6. 主內容區域 ---
if not st.session_state.show_robot_menu:
    st.markdown("<h1 style='text-align:center;'>您好！我是 TM 數據助理</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='robot-box'><div style='font-size: 80px;'>🤖</div><h3>TM Assistant</h3><p>Ready to Work</p></div>", unsafe_allow_html=True)
        if st.button("啟動功能選單 ＞", use_container_width=True):
            st.session_state.show_robot_menu = True
            st.rerun()
else:
    st.markdown("### 🤖 機器人助手選單")
    if st.button("← 返回首頁"):
        st.session_state.show_robot_menu = False
        st.rerun()
    
    tab1, tab2 = st.tabs(["🔄 運轉圈數查詢", "🎮 CS 1.6 網頁版"])
    
    with tab1:
        st.markdown("#### Log 檔案解析")
        file = st.file_uploader("請上傳檔案", type=["log", "txt"])
        if file:
            st.session_state.search_history.append({"Time": datetime.now().strftime("%H:%M"), "User": st.session_state.logged_in_user, "Action": "Parse Log"})
            lines = file.read().decode("utf-8").splitlines()
            res = []
            for axis in range(1, 7):
                t2100, t2200 = f"({axis},2100,00,1814", f"({axis},2200,00,"
                h, d = "N/A", 0
                for i in range(len(lines)-1, -1, -1):
                    if t2100 in lines[i]:
                        for j in range(i, min(i+15, len(lines))):
                            if t2200 in lines[j] and j+1 < len(lines) and "OK:" in lines[j+1]:
                                h = lines[j+1].split("OK:")[1].strip().split()[0]
                                d = int(h, 16)
                                break
                        if h != "N/A": break
                res.append({"軸向": f"J{axis}", "Hex": h, "圈數": f"{d:,}"})
            st.dataframe(pd.DataFrame(res), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("#### 🎮 戰場載入中...")
        if st.button("點此記錄並進入遊戲"):
            st.session_state.search_history.append({"Time": datetime.now().strftime("%H:%M"), "User": st.session_state.logged_in_user, "Action": "Open CS 1.6"})
        components.iframe("https://play-cs.com/en/servers", height=600, scrolling=True)
