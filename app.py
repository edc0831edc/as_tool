import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 初始化狀態 (確保所有變數都存在)
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT AI Assistant"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "show_robot_menu" not in st.session_state:
    st.session_state.show_robot_menu = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. 核心 CSS 樣式 (修正文字顯色與區塊對比)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    
    /* 頂部導航列樣式 */
    .nav-header {
        background-color: #1a1a1a;
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        margin-bottom: 20px;
    }

    /* 機器人互動區 */
    .robot-box {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 50px;
        text-align: center;
        background-color: #fcfcfc;
        margin-top: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* 側邊欄深色文字修正 */
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* 強制主頁面文字為深灰色 */
    h1, h2, h3, p, label, .stMarkdown {
        color: #1a1a1a !important;
    }

    /* TM 藍色方塊按鈕 */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 2px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導覽列 ---
st.markdown(f"""
<div class='nav-header'>
    <div style='font-size: 22px; font-weight: 700;'>TM ROBOT <span style='font-weight: 300;'>| Data Service</span></div>
</div>
""", unsafe_allow_html=True)

# --- 4. 側邊欄與管理員選單 ---
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    # 帳戶頭像與登入 (Popover)
    current_user = st.session_state.logged_in_user
    label_text = f"👤 {current_user.upper()}"
    with st.popover(label_text):
        if current_user == "guest":
            u = st.text_input("Admin ID")
            p = st.text_input("Password", type="password")
            if st.button("Login"):
                if u == "admin" and p == "666":
                    st.session_state.logged_in_user = "admin"
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        else:
            st.write(f"Logged in as: {current_user}")
            if st.button("Logout"):
                st.session_state.logged_in_user = "guest"
                st.rerun()

    st.markdown("---")
    
    # 搜尋紀錄 (僅管理員可見)
    if st.session_state.logged_in_user == "admin":
        st.markdown("#### 📋 User Activity Log")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), hide_index=True)
        else:
            st.info("No records yet.")

# --- 5. 主內容區域 ---
if not st.session_state.show_robot_menu:
    # 機器人首頁
    st.markdown("<h1 style='text-align:center;'>您好！我是 TM 數據助理</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>點擊下方按鈕啟動我的機器人功能。</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class='robot-box'>
            <div style='font-size: 80px;'>🤖</div>
            <h3 style='margin-top:20px;'>TM AI Assistant</h3>
            <p style='color:#666 !important;'>Status: Online</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("啟動功能選單 ＞", use_container_width=True):
            st.session_state.show_robot_menu = True
            st.rerun()
else:
    # 功能選單頁面
    st.markdown("### 🤖 機器人助手：功能清單")
    if st.button("← 返回首頁"):
        st.session_state.show_robot_menu = False
        st.rerun()
    
    st.write("---")
    
    # 功能區標籤
    tab1, tab2 = st.tabs(["🔄 運轉圈數查詢", "🔧 更多工具"])
    
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("#### Log 檔案分析")
            st.write("請將檔案拖曳至下方：")
            file = st.file_uploader("", type=["log", "txt"])
            
        with c2:
            if file:
                # 紀錄搜尋紀錄
                st.session_state.search_history.append({
                    "Timestamp": datetime.now().strftime("%H:%M:%S"),
                    "User": st.session_state.logged_in_user,
                    "File": file.name
                })
                
                # 提取邏輯
                lines = file.read().decode("utf-8").splitlines()
                final_results = []
                for axis in range(1, 7):
                    t2100 = f"({axis},2100,00,1814"
                    t2200 = f"({axis},2200,00,"
                    hex_s, dec_s = "N/A", 0
                    
                    for i in range(len(lines)-1, -1, -1):
                        if t2100 in lines[i]:
                            for j in range(i, min(i+15, len(lines))):
                                if t2200 in lines[j] and j+1 < len(lines) and "OK:" in lines[j+1]:
                                    hex_s = lines[j+1].split("OK:")[1].strip().split()[0]
                                    dec_s = int(hex_s, 16)
                                    break
                            if hex_s != "N/A": break
                    final_results.append({"軸向": f"J{axis}", "Hex": hex_s, "十進位圈數": f"{dec_s:,}"})
                
                st.markdown("#### 解析結果清單")
                st.table(pd.DataFrame(final_results))
                st.success("數據提取成功。")

    with tab2:
        st.info("更多診斷功能開發中，敬請期待。")
