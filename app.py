import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import streamlit.components.v1 as components

# --- 1. 安全加密工具 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h

# 密碼 666 的 SHA-256 加密值
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

# --- 2. 初始化狀態 ---
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

st.set_page_config(page_title="TM Assistant", layout="wide")

# --- 3. 手機與 UI CSS 優化 ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .nav-header { background-color: #1a1a1a; padding: 15px; color: white; border-bottom: 4px solid #004a99; margin-bottom: 20px; }
    .robot-card { border: 1px solid #ddd; border-radius: 12px; padding: 25px; text-align: center; background: #f9f9f9; }
    
    /* 手機端按鈕自動延伸，方便點擊 */
    @media (max-width: 600px) {
        .stButton>button { width: 100% !important; height: 50px !important; }
    }
    
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stButton>button { background-color: #004a99 !important; color: white !important; font-weight: bold; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導航 ---
st.markdown("<div class='nav-header'><b>TM ROBOT | AI Service</b></div>", unsafe_allow_html=True)

# --- 5. 側邊欄：加密管控 ---
with st.sidebar:
    st.title("⚙️ 控制中心")
    
    # 使用 container 包裹登入區，讓狀態顯示更穩定
    login_area = st.container()
    with login_area:
        if st.session_state.logged_in_user == "guest":
            u_in = st.text_input("Admin ID", key="admin_id")
            p_in = st.text_input("Security Key", type="password", key="admin_pwd")
            if st.button("驗證身分"):
                if u_in == "admin" and check_hashes(p_in, ADMIN_HASH):
                    st.session_state.logged_in_user = "admin"
                    st.success("驗證成功！")
                    st.rerun()
                else:
                    st.error("密碼錯誤")
        else:
            st.success(f
