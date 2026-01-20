import streamlit as st
import pandas as pd

# 1. 初始化配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT Data Analytics"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. TM ROBOT 品牌視覺 CSS (修正深色色塊文字不可見問題)
st.markdown(f"""
    <style>
    /* 全域背景與基礎文字 */
    .stApp {{ background-color: #ffffff; }}
    
    /* 強制主畫面文字為深灰色/黑色 */
    h1, h2, h3, h4, .stMarkdown p, .stTable {{
        color: #1a1a1a !important;
    }}

    /* 頂部黑底導航列 */
    .nav-bar {{
        background-color: #1a1a1a;
        padding: 20px 50px;
        color: #ffffff !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }}

    /* --- 管理員介面 (側邊欄) 深色色塊修正 --- */
    [data-testid="stSidebar"] {{
        background-color: #1a1a1a !important;
    }}
    /* 強制側邊欄內所有文字、標籤、輸入框標題為白色 */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stButton p {{
        color: #ffffff !important;
    }}

    /* --- Log 提取功能區 (深色色塊) --- */
    .analysis-container {{
        background-color: #262626;
        padding: 40px;
        border-radius: 4px;
        color: #ffffff !important;
        border-left: 5px solid #004a99;
    }}
    /* 強制功能區塊內文字為白色 */
    .analysis-container h2, 
    .analysis-container h3, 
    .analysis-container h4, 
    .analysis-container p, 
    .analysis-container label {{
        color: #ffffff !important;
    }}

    /* TM 藍色方正按鈕 */
    .stButton>button {{
        background-color: #004a99 !important;
        color: #ffffff !important;
        border-radius: 0px !important;
        padding: 10px 30px !important;
        border: none !important;
        font-weight: 600 !important;
    }}
    
    /* 表格內的字體顏色 (提取結果) */
    .stTable td, .stTable th {{
        color: #1a1a1a !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 仿官網導航列 ---
st.markdown("""
    <div class='nav-bar'>
        <div style='font-size: 26px; font-weight: bold; color: white;'>TM ROBOT <span style='font-weight: 300; font-size: 18px;'>| Data Hub</span></div>
        <div style='font-size: 14px
