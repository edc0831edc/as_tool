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
            st.success(f"已登入：{st.session_state.logged_in_user}")
            if st.button("安全登出"):
                st.session_state.logged_in_user = "guest"
                st.rerun()

    # 僅管理員可見的紀錄
    if st.session_state.logged_in_user == "admin":
        st.markdown("---")
        st.subheader("📋 訪客活動紀錄")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True, hide_index=True)
            if st.button("清空所有紀錄"):
                st.session_state.search_history = []
                st.rerun()
        else:
            st.caption("尚無任何紀錄")

# --- 6. 主頁面內容 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center; color:#1a1a1a;'>您好！我是 TM 數據助理</h2>", unsafe_allow_html=True)
    st.markdown("<div class='robot-card'><div style='font-size:60px;'>🤖</div><h4>系統連線中...</h4></div>", unsafe_allow_html=True)
    st.write("")
    if st.button("啟動功能選單 ＞", use_container_width=True):
        st.session_state.show_menu = True
        st.rerun()
else:
    # 功能內頁
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("← 返回"):
            st.session_state.show_menu = False
            st.rerun()
    
    tab1, tab2 = st.tabs(["🔄 運轉圈數查詢", "🎮 CS 1.6 網頁版"])
    
    with tab1:
        st.markdown("### Log 數據解析引擎")
        file = st.file_uploader("選擇 Log 檔案", type=["log", "txt"])
        if file:
            # 紀錄動作
            st.session_state.search_history.append({
                "時間": datetime.now().strftime("%H:%M"),
                "使用者": st.session_state.logged_in_user,
                "動作": "解析檔案",
                "細節": file.name
            })
            
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
            st.success("解析完成！")

    with tab2:
        st.markdown("### 🎮 經典 CS 1.6 戰場")
        st.info("提示：手機玩家建議將螢幕「橫向旋轉」以獲得最佳體驗。")
        
        if st.button("進入遊戲並回報紀錄"):
            st.session_state.search_history.append({
                "時間": datetime.now().strftime("%H:%M"),
                "使用者": st.session_state.logged_in_user,
                "動作": "開啟遊戲",
                "細節": "CS 1.6 中文版"
            })
            st.toast("已紀錄至管理後台")
        
        # 使用更新後的網址
        components.iframe("https://play-cs.com/zh/servers", height=700, scrolling=True)
