import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 安全認證功能 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

# 初始化狀態
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False

st.set_page_config(page_title="TM AI Assistant", layout="wide")

# --- 2. 專業機器人風格 CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .nav-header { 
        background-color: #1a1a1a; padding: 20px; color: white; 
        border-bottom: 5px solid #004a99; text-align: center;
        font-family: 'Arial Black', sans-serif;
    }
    
    /* 機器人卡片視覺 */
    .robot-container {
        border: 1px solid #ddd; border-radius: 15px;
        padding: 30px; text-align: center;
        background: white; margin: 20px auto; max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .robot-icon { font-size: 80px; margin-bottom: 10px; }

    /* 按鈕樣式 */
    .stButton>button {
        background-color: #004a99 !important; color: white !important;
        font-weight: bold; width: 100%; height: 50px; border-radius: 8px;
    }
    
    /* 連結按鈕樣式 */
    .link-box {
        display: block; width: 100%; text-align: center;
        background-color: #004a99; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 8px;
        font-weight: bold; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部標題 ---
st.markdown("<div class='nav-header'>TM ROBOT | AI INTERACTIVE SYSTEM</div>", unsafe_allow_html=True)

# --- 4. 側邊欄控制 ---
with st.sidebar:
    st.title("⚙️ 控制中心")
    if st.session_state.logged_in_user == "guest":
        u = st.text_input("管理員帳號")
        p = st.text_input("安全密碼", type="password")
        if st.button("登入驗證"):
            if u == "admin" and check_hashes(p, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"; st.rerun()
            else: st.error("驗證失敗")
    else:
        st.success(f"目前使用者：{st.session_state.logged_in_user}")
        if st.button("安全登出"): st.session_state.logged_in_user = "guest"; st.rerun()
        
        if st.session_state.logged_in_user == "admin":
            st.markdown("---")
            st.subheader("📋 系統紀錄回傳")
            if st.session_state.search_history:
                st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True, hide_index=True)

# --- 5. 首頁內容：TM AI 機器人 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center; color:#1a1a1a;'>您好！我是 TM 數據助理</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='robot-container'>
        <div class='robot-icon'>🤖</div>
        <h3>SYSTEM ONLINE</h3>
        <p>已準備好為您解析數據與提供娛樂服務</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚡ 啟動功能功能選單"):
            st.session_state.show_menu = True
            st.rerun()

# --- 6. 功能選單頁面 ---
else:
    if st.button("← 返回首頁"):
        st.session_state.show_menu = False; st.rerun()
        
    tab1, tab2, tab3 = st.tabs(["🔄 圈數查詢", "🕹️ 史萊姆遊戲", "🎮 CS 1.6"])
    
    with tab1:
        st.subheader("Log 數據解析引擎")
        file = st.file_uploader("請上傳 Log 檔案", type=["log", "txt"])
        if file:
            st.info("正在分析 Log 軸向數據...")
            # 這裡保留你原本的軸向解析 logic 即可

    with tab2:
        st.subheader("🕹️ 史萊姆第一個家")
        st.markdown('<a href="http://game.slime.com.tw/" target="_blank" class="link-box">🚀 開啟遊戲區 (新視窗)</a>', unsafe_allow_html=True)
        if st.button("紀錄進入：史萊姆"):
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "遊戲", "詳細": "史萊姆"})
            st.toast("已紀錄至管理後台")

    with tab3:
        st.subheader("🎮 CS 1.6 網頁版")
        st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" class="link-box">🔫 進入戰場 (新視窗)</a>', unsafe_allow_html=True)
        if st.button("紀錄進入：CS 1.6"):
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "遊戲", "詳細": "CS 1.6"})
            st.toast("已紀錄至管理後台")
