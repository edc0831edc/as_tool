import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import streamlit.components.v1 as components

# --- 1. 加密安全模組 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
# 密碼 666 的加密值
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

# --- 2. 初始化狀態 ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False

st.set_page_config(page_title="TM Assistant", layout="wide")

# --- 3. 手機優化 CSS ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .nav-header { background-color: #1a1a1a; padding: 15px; color: white; border-bottom: 4px solid #004a99; margin-bottom: 20px; }
    .robot-card { border: 1px solid #ddd; border-radius: 15px; padding: 30px; text-align: center; background: #f9f9f9; margin-bottom: 20px; }
    @media (max-width: 600px) { .stButton>button { width: 100% !important; } }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stButton>button { background-color: #004a99 !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導航 ---
st.markdown("<div class='nav-header'><b>TM ROBOT | AI Service</b></div>", unsafe_allow_html=True)

# --- 5. 側邊欄：加密管控後台 ---
with st.sidebar:
    st.title("⚙️ 控制中心")
    user = st.session_state.logged_in_user
    
    with st.expander(f"👤 {user.upper()}"):
        if user == "guest":
            u_in = st.text_input("Admin ID")
            p_in = st.text_input("Security Key", type="password")
            if st.button("驗證登入"):
                if u_in == "admin" and check_hashes(p_in, ADMIN_HASH):
                    st.session_state.logged_in_user = "admin"
                    st.rerun()
                else: st.error("權限錯誤")
        else:
            if st.button("安全登出"):
                st.session_state.logged_in_user = "guest"
                st.rerun()

    if st.session_state.logged_in_user == "admin":
        st.markdown("---")
        st.write("📋 訪客活動紀錄")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True)
            if st.button("清空紀錄"):
                st.session_state.search_history = []
                st.rerun()
        else: st.caption("目前無紀錄")

# --- 6. 主頁面：機器人導引 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center;'>您好！我是 TM 數據助理</h2>", unsafe_allow_html=True)
    st.markdown("<div class='robot-card'><div style='font-size:60px;'>🤖</div><h4>系統狀態：線上</h4></div>", unsafe_allow_html=True)
    if st.button("啟動功能選單 ＞", use_container_width=True):
        st.session_state.show_menu = True
        st.rerun()

# --- 7. 功能內頁 (標籤切換) ---
else:
    if st.button("← 返回首頁"):
        st.session_state.show_menu = False
        st.rerun()
    
    tab1, tab2 = st.tabs(["🔄 運轉圈數查詢", "🎮 CS 1.6 網頁版"])
    
    with tab1:
        st.write("#### Log 解析工具")
        file = st.file_uploader("上傳 Log 檔案", type=["log", "txt"])
        if file:
            st.session_state.search_history.append({"Time": datetime.now().strftime("%H:%M"), "Action": "解析Log", "Target": file.name})
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
            st.success("數據提取成功")

    with tab2:
        st.write("#### 網頁版 CS 1.6")
        if st.button("🎮 進入遊戲並記錄"):
            st.session_state.search_history.append({"Time": datetime.now().strftime("%H:%M"), "Action": "開啟CS1.6", "Target": "WebGame"})
            st.toast("遊戲紀錄已存檔")
        
        # 遊戲組件
        components.iframe("https://play-cs.com/en/servers", height=600, scrolling=True)
