import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import time

# --- 1. 安全與狀態初始化 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False

# 電子雞初始狀態
if "pet" not in st.session_state:
    st.session_state.pet = {"name": "鋼彈幼體", "level": 1, "hunger": 50, "happy": 50, "exp": 0, "status": "待機中"}

st.set_page_config(page_title="TM Gundam OS", layout="wide")

# --- 2. 鋼彈科技風 CSS ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle, #1a1a2e 0%, #0f0f1a 100%); color: #00d4ff; }
    .nav-header { background: rgba(0, 74, 153, 0.2); padding: 15px; border-left: 5px solid #ff0000; border-bottom: 1px solid #00d4ff; margin-bottom: 20px; }
    
    /* 鋼彈風格卡片 */
    .gundam-card {
        border: 2px solid #00d4ff; background: rgba(0, 20, 40, 0.8);
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0 0 15px #00d4ff; margin: 0 auto; max-width: 450px;
    }
    .status-bar { background: #333; border-radius: 10px; margin: 5px 0; height: 15px; overflow: hidden; }
    .status-fill { background: linear-gradient(90deg, #00d4ff, #004a99); height: 100%; transition: 0.5s; }
    
    @media (max-width: 600px) { .stButton>button { width: 100% !important; height: 50px !important; } }
    .stButton>button { background: #004a99 !important; color: white !important; border: 1px solid #00d4ff !important; font-weight: bold; }
    .game-link-button {
        display: block; width: 100%; text-align: center; background: #ff0000; color: white !important;
        padding: 15px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; border: 1px solid white;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導航 ---
st.markdown("<div class='nav-header'><b>TM GUNDAM OS | UC 0079 SYSTEM</b></div>", unsafe_allow_html=True)

# --- 4. 側邊欄 ---
with st.sidebar:
    st.title("🛡️ 駕駛員認證")
    if st.session_state.logged_in_user == "guest":
        u_in = st.text_input("Pilot ID")
        p_in = st.text_input("Key", type="password")
        if st.button("驗證登入"):
            if u_in == "admin" and check_hashes(p_in, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"; st.rerun()
            else: st.error("認證失敗")
    else:
        st.success(f"Pilot: {st.session_state.logged_in_user.upper()}")
        if st.button("登出系統"): st.session_state.logged_in_user = "guest"; st.rerun()

    if st.session_state.logged_in_user == "admin":
        st.markdown("---")
        st.subheader("📋 任務日誌")
        if st.session_state.search_history:
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True, hide_index=True)

# --- 5. 主頁面：鋼彈互動 ---
if not st.session_state.show_menu:
    st.markdown("<h1 style='text-align:center; color:#fff; text-shadow: 0 0 10px #00d4ff;'>GUNDAM AI ASSISTANT</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='gundam-card'>
        <div style='font-size:80px;'>🤖</div>
        <h3 style='color:#fff;'>{st.session_state.pet['name']} LV.{st.session_state.pet['level']}</h3>
        <p>狀態: <span style='color:#ff0000;'>{st.session_state.pet['status']}</span></p>
        <div style='text-align:left; font-size:12px;'>
            能源 (飽食): {st.session_state.pet['hunger']}% <div class='status-bar'><div class='status-fill' style='width:{st.session_state.pet['hunger']}%'></div></div>
            動力 (心情): {st.session_state.pet['happy']}% <div class='status-bar'><div class='status-fill' style='width:{st.session_state.pet['happy']}%'></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍼 補充能源"):
            st.session_state.pet['hunger'] = min(100, st.session_state.pet['hunger'] + 20)
            st.session_state.pet['status'] = "能源補充中"
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "養育", "細節": "餵食鋼彈"})
            st.rerun()
    with col2:
        if st.button("🎮 模擬對戰"):
            st.session_state.pet['happy'] = min(100, st.session_state.pet['happy'] + 20)
            st.session_state.pet['exp'] += 15
            st.session_state.pet['status'] = "模擬訓練中"
            if st.session_state.pet['exp'] >= 100:
                st.session_state.pet['level'] += 1
                st.session_state.pet['exp'] = 0
                st.toast("⚡ 鋼彈升級了！")
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "養育", "細節": "心情提升"})
            st.rerun()
    with col3:
        if st.button("啟動選單 ＞", use_container_width=True):
            st.session_state.show_menu = True; st.rerun()

# --- 6. 功能選單 ---
else:
    if st.button("← 返回機庫"): st.session_state.show_menu = False; st.rerun()
    
    t1, t2, t3, t4 = st.tabs(["🔄 解析", "🎮 CS1.6", "🕹️ 史萊姆", "📟 養育紀錄"])
    
    with t1:
        file = st.file_uploader("上傳 Log", type=["log", "txt"])
        if file:
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "解析", "細節": file.name})
            # ... (原本的解析代碼)
            st.success("數據讀取完畢")

    with t2:
        st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" class="game-link-button">🚀 開啟 CS 1.6 戰場</a>', unsafe_allow_html=True)

    with t3:
        st.markdown('<a href="http://game.slime.com.tw/" target="_blank" class="game-link-button">👾 開啟史萊姆遊戲區</a>', unsafe_allow_html=True)

    with t4:
        st.subheader("📟 電子雞成長日誌")
        logs = [h for h in st.session_state.search_history if h['動作'] == "養育"]
        if logs: st.table(logs)
        else: st.info("目前還沒有養育紀錄")
