import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 初始化配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT AI Assistant"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "guest"  # 預設為訪客
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "show_robot_menu" not in st.session_state:
    st.session_state.show_robot_menu = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. TM ROBOT 視覺與機器人元件 CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* 導航列 */
    .nav-bar {
        background-color: #1a1a1a;
        padding: 10px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    /* 機器人啟動區塊 (TM Robot 造型感) */
    .robot-trigger {
        border: 2px solid #004a99;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        background-color: #f8f9fa;
        transition: 0.3s;
        cursor: pointer;
        margin: 50px auto;
        max-width: 400px;
    }
    .robot-trigger:hover {
        box-shadow: 0 10px 30px rgba(0,74,153,0.2);
        transform: translateY(-5px);
    }

    /* 側邊欄深色修正 */
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* 文字顯色強制修正 */
    h1, h2, h3, p, label { color: #1a1a1a !important; }
    .dark-text { color: #ffffff !important; }

    /* TM 藍色方正按鈕 */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導航列 (頭像選單) ---
col_nav_l, col_nav_r = st.columns([4, 1])
with col_nav_l:
    st.markdown(f"<h2 style='margin:15px 0;'>TM ROBOT <span style='font-weight:200;'>| {st.session_state.page_title}</span></h2>", unsafe_allow_html=True)

with col_nav_r:
    st.markdown("<br>", unsafe_allow_html=True)
    current_user = st.session_state.logged_in_user
    # 使用 popover 製作頭像選單
    label = "👤 管理員" if current_user == "admin" else "👤 訪客 (Guest)"
    with st.popover(label):
        if current_user == "guest":
            user_input = st.text_input("管理員帳號")
            pw_input = st.text_input("密碼", type="password")
            if st.button("登入後台"):
                if user_input == "admin" and pw_input == "666":
                    st.session_state.logged_in_user = "admin"
                    st.rerun()
                else:
                    st.error("密碼錯誤")
        else:
            st.write(f"目前身分: {current_user}")
            if st.button("登出回訪客模式"):
                st.session_state.logged_in_user = "guest"
                st.rerun()

st.markdown("---")

# --- 4. 側邊欄：管理員查詢歷史 (僅 admin 可見) ---
with st.sidebar:
    st.markdown("### 📊 數據監控中心")
    if st.session_state.logged_in_user == "admin":
        st.markdown("#### 用戶查詢紀錄")
        if st.session_state.search_history:
