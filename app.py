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

# --- 3. UI 與 手機按鈕 CSS ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .nav-header { background-color: #1a1a1a; padding: 15px; color: white; border-bottom: 4px solid #004a99; margin-bottom: 20px; }
    .robot-card { border: 1px solid #ddd; border-radius: 12px; padding: 25px; text-align: center; background: #f9f9f9; }
    
    @media (max-width: 600px) {
        .stButton>button { width: 100% !important; height: 50px !important; }
    }
    
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    .stButton>button { background-color: #004a99 !important; color: white !important; font-weight: bold; }
    
    /* 遊戲區標題樣式 */
    .game-title { color: #004a99; font-weight: bold; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導航 ---
st.markdown("<div class='nav-header'><b>TM ROBOT | AI Service</b></div>", unsafe_allow_html=True)

# --- 5. 側邊欄：管理員後台 ---
with st.sidebar:
    st.title("⚙️ 控制中心")
    if st.session_state.logged_in_user == "guest":
        u_in = st.text_input("Admin ID")
        p_in = st.text_input("Security Key", type="password")
        if st.button("驗證身分"):
            if u_in == "admin" and check_hashes(p_in, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"
                st.rerun()
            else:
                st.error("密碼錯誤")
    else:
        st.success(f"權限：{st.session_state.logged_in_user}")
        if st.button("安全登出"):
            st.session_state.logged_in_user = "guest"
            st.rerun()

    if st.session_state.logged_in_user == "admin":
        st.markdown("---")
        st.subheader("📋 系統活動紀錄")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True, hide_index=True)
            if st.button("清空所有紀錄"):
                st.session_state.search_history = []
                st.rerun()

# --- 6. 主內容區域 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center;'>您好！我是 TM 數據助理</h2>", unsafe_allow_html=True)
    st.markdown("<div class='robot-card'><div style='font-size:60px;'>🤖</div><h4>系統已連線</h4></div>", unsafe_allow_html=True)
    if st.button("啟動功能選單 ＞", use_container_width=True):
        st.session_state.show_menu = True
        st.rerun()
else:
    if st.button("← 返回"):
        st.session_state.show_menu = False
        st.rerun()
    
    # 三個功能標籤
    tab1, tab2, tab3 = st.tabs(["🔄 圈數查詢", "🎮 CS 1.6", "🕹️ 史萊姆遊戲"])
    
    with tab1:
        file = st.file_uploader("選擇 Log 檔案", type=["log", "txt"])
        if file:
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "解析檔案", "細節": file.name})
            lines = file.read().decode("utf-8").splitlines()
            res = []
            for ax in range(1, 7):
                t1, t2 = f"({ax},2100,00,1814", f"({ax},2200,00,"
                h, d = "N/A", 0
                for i in range(len(lines)-1, -1, -1):
                    if t1 in lines[i]:
                        for j in range(i, min(i+15, len(lines))):
                            if t2 in lines[j] and j+1 < len(lines) and "OK:" in lines[j+1]:
                                h = lines[j+1].split("OK:")[1].strip().split()[0]
                                d = int(h, 16)
                                break
                        if h != "N/A": break
                res.append({"軸向": f"J{ax}", "十六進位": h, "圈數": f"{d:,}"})
            st.dataframe(pd.DataFrame(res), use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("<h3 class='game-title'>經典戰場 CS 1.6</h3>", unsafe_allow_html=True)
        game_url = "https://play-cs.com/zh/servers"
        st.markdown(f'<a href="{game_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#004a99; color:white; padding:15px; text-align:center; border-radius:5px; font-weight:bold;">🚀 開啟新分頁進入 CS 1.6</div></a>', unsafe_allow_html=True)
        if st.button("記錄進入 CS 1.6"):
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "遊戲", "細節": "CS 1.6"})

    with tab3:
        st.markdown("<h3 class='game-title'>🕹️ 史萊姆第一個家</h3>", unsafe_allow_html=True)
        if st.button("記錄使用遊戲區"):
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "遊戲", "細節": "史萊姆遊戲區"})
            st.toast("已紀錄至後台")
        
        # 嵌入史萊姆網頁
        slime_url = "http://game.slime.com.tw/"
        components.iframe(slime_url, height=800, scrolling=True)
