import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面配置與資料初始化
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT Data Hub"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
# 模擬資料庫：存儲所有帳戶的查詢紀錄
if "search_history" not in st.session_state:
    st.session_state.search_history = []

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. TM 風格高對比 CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .nav-bar {
        background-color: #1a1a1a;
        padding: 10px 50px;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }
    /* 側邊欄文字強制顯色 */
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* 頭像樣式 */
    .user-avatar {
        width: 45px; height: 45px;
        border-radius: 50%;
        background-color: #004a99;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; cursor: pointer; border: 2px solid #ffffff;
    }
    
    /* TM 藍色方塊 */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 0px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導航列 (含頭像登入) ---
col_nav_l, col_nav_r = st.columns([4, 1])
with col_nav_l:
    st.markdown(f"<h2 style='color:#1a1a1a; margin:15px 0;'>TM ROBOT <span style='font-weight:200;'>| {st.session_state.page_title}</span></h2>", unsafe_allow_html=True)

with col_nav_r:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.logged_in_user:
        # 已登入顯示頭像 (Popover 形式)
        with st.popover(f"👤 {st.session_state.logged_in_user}"):
            st.write(f"當前用戶: {st.session_state.logged_in_user}")
            if st.button("登出"):
                st.session_state.logged_in_user = None
                st.rerun()
    else:
        # 未登入顯示登入圖示
        with st.popover("🔑 Login"):
            user = st.text_input("帳號")
            pw = st.text_input("密碼", type="password")
            if st.button("登入系統"):
                if pw == "666": # 示範密碼
                    st.session_state.logged_in_user = user
                    st.rerun()

st.markdown("---")

# --- 4. 側邊欄：管理員後台查詢 ---
with st.sidebar:
    st.markdown("### 📊 後台管理系統")
    if st.session_state.logged_in_user == "admin": # 只有 admin 帳號可看
        if st.toggle("顯示所有用戶查詢紀錄"):
            st.markdown("#### 搜尋歷史回溯")
            if st.session_state.search_history:
                history_df = pd.DataFrame(st.session_state.search_history)
                st.dataframe(history_df, use_container_width=True)
            else:
                st.write("目前尚無查詢紀錄。")
    else:
        st.caption("僅限管理員帳戶訪問歷史紀錄")

# --- 5. 主內容區域：Log 提取功能 ---
if not st.session_state.logged_in_user:
    st.warning("請先點擊右上角頭像圖示進行登入，以使用數據分析功能。")
else:
    st.markdown(f"### 🔄 運轉圈數分析系統 (用戶: {st.session_state.logged_in_user})")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        uploaded_file = st.file_uploader("上傳 Log 檔案", type=["log", "txt"])
    
    with c2:
        if uploaded_file:
            # 紀錄搜尋行為到後台
            st.session_state.search_history.append({
                "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "帳戶": st.session_state.logged_in_user,
                "檔案名稱": uploaded_file.name
            })
            
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            results = []
            
            # 提取邏輯 (J1-J6)
            for axis in range(1, 7):
                t_2100 = f"({axis},2100,00,1814"
                t_
