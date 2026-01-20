import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 核心安全與狀態 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False

# 魯夫電子雞狀態：增加「體型 size」變數
if "luffy" not in st.session_state:
    st.session_state.luffy = {"name": "路飛", "size": 30, "status": "好餓，想吃肉！", "bombs": 0}

st.set_page_config(page_title="TM BANDAI GUNDAM OS", layout="wide")

# --- 2. BANDAI 鋼彈風格 CSS (經典白藍紅配色) ---
st.markdown("""
<style>
    /* BANDAI 鋼彈配色 */
    .stApp { background-color: #f0f0f0; color: #333; }
    
    .nav-header { 
        background-color: #e60012; /* BANDAI 紅 */
        padding: 10px 20px; 
        color: white; 
        border-bottom: 5px solid #004a99; /* 鋼彈藍 */
        font-family: 'Arial Black', sans-serif;
    }
    
    /* 魯夫顯示區 */
    .luffy-container {
        border: 4px solid #004a99;
        background: white;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin: 20px auto;
        max-width: 500px;
        position: relative;
        overflow: hidden;
    }
    
    .luffy-sprite {
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: inline-block;
    }

    /* 鋼彈風格按鈕 */
    .stButton>button {
        background-color: #004a99 !important;
        color: white !important;
        border: 2px solid #ffcc00 !important; /* 鋼彈黃 */
        border-radius: 0px !important;
        font-weight: bold;
        height: 50px;
    }
    
    .stButton>button:hover {
        background-color: #e60012 !important;
        border: 2px solid #white !important;
    }

    @media (max-width: 600px) {
        .stButton>button { width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導航 ---
st.markdown("<div class='nav-header'>TM ROBOT | <span style='color:#ffcc00;'>BANDAI</span> GUNDAM SYSTEM</div>", unsafe_allow_html=True)

# --- 4. 側邊欄 ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Bandai_Namco_Holdings_logo.svg/1200px-Bandai_Namco_Holdings_logo.svg.png", width=100)
    if st.session_state.logged_in_user == "guest":
        u = st.text_input("駕駛員 ID")
        p = st.text_input("密碼", type="password")
        if st.button("認證登入"):
            if u == "admin" and check_hashes(p, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"; st.rerun()
    else:
        st.write(f"當前駕駛員: {st.session_state.logged_in_user.upper()}")
        if st.button("登出"): st.session_state.logged_in_user = "guest"; st.rerun()

# --- 5. 主頁面：氣球魯夫電子雞 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center;'>橡膠氣球魯夫養育系統</h2>", unsafe_allow_html=True)
    
    # 計算尺寸比例
    current_size = st.session_state.luffy['size']
    
    # 魯夫容器
    st.markdown(f"""
    <div class='luffy-container'>
        <div class='luffy-sprite' style='font-size: {current_size}px;'>
            🍖👒🍖<br>🥤👨‍🌾🥤
        </div>
        <h3 style='margin-top:20px;'>體型規模: {current_size}%</h3>
        <p>狀態: <b>{st.session_state.luffy['status']}</b></p>
        <p style='color:red;'>已爆炸次數: {st.session_state.luffy['bombs']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍖 餵食大肉 (變大)", use_container_width=True):
            st.session_state.luffy['size'] += 25
            st.session_state.luffy['status'] = "好飽...還要吃！"
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "餵食", "細節": f"尺寸變為{st.session_state.luffy['size']}"})
            
            # 檢查是否爆炸
            if st.session_state.luffy['size'] > 250:
                st.balloons()
                st.error("💥 💥 💥 砰！！魯夫爆炸了！！ 💥 💥 💥")
                st.session_state.luffy = {"name": "路飛", "size": 30, "status": "重生成功，好餓！", "bombs": st.session_state.luffy['bombs']+1}
                st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "爆炸", "細節": "體型過大重生"})
            st.rerun()
            
    with col2:
        if st.button("🛠️ 進入功能選單", use_container_width=True):
            st.session_state.show_menu = True
            st.rerun()

# --- 6. 功能選單 ---
else:
    if st.button("← 返回格納庫"): st.session_state.show_menu = False; st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📊 數據解析", "🎮 遊戲區域", "📋 歷史日誌"])
    
    with tab1:
        st.subheader("鋼彈數據分析儀")
        # (這裡保留你原本的 Log 解析程式碼)
        st.info("請上傳 Log 進行軸向圈數計算")

    with tab2:
        st.markdown("### 外部連結啟動")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" style="text-decoration:none;"><div style="background:#004a99; color:white; padding:20px; text-align:center;">CS 1.6 戰場</div></a>', unsafe_allow_html=True)
        with col_g2:
            st.markdown('<a href="http://game.slime.com.tw/" target="_blank" style="text-decoration:none;"><div style="background:#e60012; color:white; padding:20px; text-align:center;">史萊姆遊戲</div></a>', unsafe_allow_html=True)

    with tab3:
        if st.session_state.logged_in_user == "admin":
            st.dataframe(pd.DataFrame(st.session_state.search_history), use_container_width=True)
