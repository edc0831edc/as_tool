import streamlit as st
import pandas as pd

# 1. 頁面基礎配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Data Analysis"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 套用自定義 CSS 營造 Apple 官網感 (SF Pro 字體風格、留白、陰影)
st.markdown("""
    <style>
    .main { background-color: #f5f5f7; }
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        background-color: #0071e3;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0077ed; border: none; }
    .stExpander { border: none !important; box-shadow: 0 4px 12px rgb(0,0,0,0.08); background: white; border-radius: 12px !important; }
    h1 { font-weight: 600; color: #1d1d1f; letter-spacing: -0.02em; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部導航列 (Apple Style) ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.title(st.session_state.page_title)
with col_t2:
    # 帳戶登入依然保留在側邊或隱藏，但功能已經移出
    with st.popover("👤 Account"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Sign In"):
            if user == "eddie" and pw == "666":
                st.session_state.logged_in = True
                st.success("Admin access granted")
            else:
                st.error("Invalid credentials")
        
        if st.session_state.get("logged_in"):
            new_title = st.text_input("Rename Site", value=st.session_state.page_title)
            if st.button("Update"):
                st.session_state.page_title = new_title
                st.rerun()

# --- 主視覺區 ---
st.markdown("---")
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("### 精準、可靠、自動化")
    st.markdown("""
    透過先進的數據提取演算法，我們為您簡化了 Log 檔案的解析流程。
    不需要登入，立即
