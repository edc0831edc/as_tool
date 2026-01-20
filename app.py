import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 核心邏輯與狀態 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False
if "luffy_size" not in st.session_state: st.session_state.luffy_size = 50
if "bomb_count" not in st.session_state: st.session_state.bomb_count = 0

st.set_page_config(page_title="TM GUNDAM OS", layout="wide")

# --- 2. 仿 Gemini Share 連結風格的 CSS (深色、極簡、邊框發光) ---
st.markdown("""
<style>
    /* 全域背景：深灰黑色 */
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    
    /* 仿萬代紅導航條 */
    .nav-header {
        background: linear-gradient(90deg, #e60012 0%, #004a99 100%);
        padding: 12px 25px;
        border-radius: 5px;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(230, 0, 18, 0.3);
    }

    /* 駕駛艙主容器 */
    .cockpit-box {
        border: 1px solid #30363d;
        background: rgba(22, 27, 34, 0.8);
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        margin-top: 10px;
    }

    /* 魯夫氣球動態縮放 */
    .luffy-balloon {
        display: inline-block;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        filter: drop-shadow(0 0 10px #ffcc00);
        margin: 20px 0;
    }

    /* 萬代鋼彈風格按鈕 */
    .stButton>button {
        background: transparent !important;
        color: #00d4ff !important;
        border: 1px solid #00d4ff !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: rgba(0, 212, 255, 0.1) !important;
        box-shadow: 0 0 15px #00d4ff;
    }

    /* 側邊欄調整 */
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    
    /* 數據表格美化 */
    [data-testid="stMetricValue"] { color: #ffcc00 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. 介面頂部 ---
st.markdown("<div class='nav-header'>SYSTEM LOG: UC 0079 | BANDAI GUNDAM PROTOCOL</div>", unsafe_allow_html=True)

# --- 4. 側邊欄 ---
with st.sidebar:
    st.markdown("### 駕駛員認證")
    if st.session_state.logged_in_user == "guest":
        u = st.text_input("PILOT ID", placeholder="admin")
        p = st.text_input("PASSKEY", type="password")
        if st.button("AUTHENTICATE"):
            if u == "admin" and check_hashes(p, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"
                st.rerun()
    else:
        st.success(f"ONLINE: {st.session_state.logged_in_user.upper()}")
        if st.button("LOGOUT"):
            st.session_state.logged_in_user = "guest"
            st.rerun()

# --- 5. 首頁：魯夫氣球電子雞 ---
if not st.session_state.show_menu:
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.markdown("<div class='cockpit-box'>", unsafe_allow_html=True)
        # 魯夫圖像 (Emoji 代表，可隨 size 縮放)
        scale = st.session_state.luffy_size / 50
        st.markdown(f"""
            <div class='luffy-balloon' style='transform: scale({scale});'>
                <div style='font-size: 80px;'>👒</div>
                <div style='font-size: 100px;'>🍖</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### 魯夫壓力值：{st.session_state.luffy_size}% / 200%")
        st.markdown(f"**累計爆炸次數：{st.session_state.bomb_count}**")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.write("### 交互指令")
        if st.button("🍖 餵食 (RUBBER GUM-GUM)"):
            st.session_state.luffy_size += 30
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "餵食", "對象": "魯夫"})
            
            if st.session_state.luffy_size > 200:
                st.toast("魯夫到達極限了！")
                st.session_state.bomb_count += 1
                st.session_state.luffy_size = 50
                st.error("💥 魯夫像氣球一樣爆炸了！系統重新啟動...")
                st.balloons()
            st.rerun()
            
        if st.button("🛠️ 啟動全功能選單"):
            st.session_state.show_menu = True
            st.rerun()

# --- 6. 功能選單頁面 ---
else:
    if st.button("← EXIT TO COCKPIT"):
        st.session_state.show_menu = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["[ 數據分析 ]", "[ 娛樂終端 ]", "[ 系統紀錄 ]"])

    with tab1:
        st.markdown("#### 鋼彈軸向數據解析")
        file = st.file_uploader("UPLOAD LOG FILE", type=["log", "txt"])
        if file:
            # (此處插入你原有的 Log 解析邏輯程式碼)
            st.success("DATA PARSED SUCCESSFULLY.")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" class="game-link-button" style="color:#00d4ff; text-decoration:none;">🎮 開啟 CS 1.6 (NEW WINDOW)</a>', unsafe_allow_html=True)
        with col2:
            st.markdown('<a href="http://game.slime.com.tw/" target="_blank" class="game-link-button" style="color:#00d4ff; text-decoration:none;">👾 史萊姆遊戲區 (NEW WINDOW)</a>', unsafe_allow_html=True)

    with tab3:
        if st.session_state.logged_in_user == "admin":
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True)
