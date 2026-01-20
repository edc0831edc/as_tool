import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import streamlit.components.v1 as components

# --- 1. 安全加密工具 (避免明文密碼) ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# "666" 的 SHA-256 Hash 值
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

# --- 3. 核心 CSS 樣式 (含手機端優化) ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* 頂部導航列 */
    .nav-header {
        background-color: #1a1a1a;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        margin-bottom: 15px;
        border-bottom: 3px solid #004a99;
    }

    /* 機器人互動區 */
    .robot-box {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background-color: #fcfcfc;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* 手機端 RWD 調整 */
    @media (max-width: 600px) {
        .nav-header { padding: 10px; font-size: 14px; }
        .robot-box { padding: 20px; }
        .stButton>button { width: 100% !important; }
    }

    /* 側邊欄深色修正 */
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* 文字顯色修正 */
    h1, h2, h3, p, label, .stMarkdown { color: #1a1a1a !important; }

    /* TM 藍色方塊按鈕 */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 2px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導覽列 ---
st.markdown(f"""
<div class='nav-header'>
    <div style='font-size: 18px; font-weight: 700;'>TM ROBOT <span style='font-weight: 300;'>| Intelligence</span></div>
</div>
""", unsafe_allow_html=True)

# --- 5. 側邊欄與安全性管控 ---
with st.sidebar:
    st.markdown("### 🔐 Security & Settings")
    
    current_user = st.session_state.logged_in_user
    label_text = f"👤 {current_user.upper()}"
    
    with st.popover(label_text):
        if current_user == "guest":
            u = st.text_input("Admin ID")
            p = st.text_input("Security Key", type="password")
            if st.button("Verify Identity"):
                if u == "admin" and check_hashes(p, ADMIN_HASH
