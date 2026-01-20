import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 核心邏輯 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False
if "luffy_lv" not in st.session_state: st.session_state.luffy_lv = 1
if "luffy_size" not in st.session_state: st.session_state.luffy_size = 100 # 100% 為初始
if "luffy_exp" not in st.session_state: st.session_state.luffy_exp = 20

st.set_page_config(page_title="BANDAM DATA SYSTEM", layout="wide")

# --- 2. 仿圖中設計的專屬 CSS ---
st.markdown("""
<style>
    /* 全域深色背景 */
    .stApp { background-color: #050b10; color: #5ef3ff; }

    /* 頂部標題列 */
    .bandai-header {
        display: flex; justify-content: space-around;
        background: rgba(0, 50, 80, 0.4);
        border-top: 2px solid #ff0000; border-bottom: 2px solid #5ef3ff;
        padding: 10px; font-family: 'Courier New', monospace; font-weight: bold;
    }

    /* 魯夫寵物框 */
    .pet-box {
        border: 2px solid #5ef3ff; background: rgba(0,0,0,0.5);
        padding: 20px; border-radius: 10px; text-align: center;
        margin: 20px auto; max-width: 600px;
        box-shadow: 0 0 20px rgba(94, 243, 255, 0.2);
    }

    /* 魯夫圖片動畫 (變大效果) */
    .luffy-img {
        width: 150px; border: 2px solid #ffcc00; border-radius: 10px;
        transition: transform 0.3s ease-in-out;
    }

    /* 數據進度條 */
    .stat-container { text-align: left; margin: 10px 0; font-size: 14px; }
    .stat-bar { background: #1a2a33; height: 12px; border-radius: 6px; overflow: hidden; }
    .stat-fill-orange { background: #ff6600; height: 100%; }
    .stat-fill-green { background: #a2ff00; height: 100%; }

    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(180deg, #004a99 0%, #002244 100%) !important;
        color: white !important; border: 1px solid #5ef3ff !important;
        width: 100%; border-radius: 5px; height: 45px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部 UI ---
st.markdown("""
<div class='bandai-header'>
    <span style='color:white;'>◢ BANDAI HOBBY</span>
    <span style='color:#5ef3ff;'>BANDAM DATA SYSTEM</span>
    <span style='color:red;'>G.U.EST SYSTEM</span>
</div>
""", unsafe_allow_html=True)

# --- 4. 側邊欄紀錄 ---
with st.sidebar:
    st.markdown("### [ SYSTEM AUTH ]")
    if st.session_state.logged_in_user == "guest":
        u = st.text_input("PILOT ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("VERIFY"):
            if u == "admin" and check_hashes(p, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"; st.rerun()
    else:
        st.success(f"ONLINE: {st.session_state.logged_in_user}")
        if st.button("LOGOUT"): st.session_state.logged_in_user = "guest"; st.rerun()
        if st.session_state.logged_in_user == "admin":
            st.markdown("---")
            st.write("📋 任務紀錄")
            st.dataframe(pd.DataFrame(st.session_state.search_history), hide_index=True)

# --- 5. 主頁面：ONE PIECE PET SYSTEM ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center; letter-spacing:3px;'>“ONE PIECE PET SYSTEM”</h2>", unsafe_allow_html=True)
    
    # 魯夫區塊
    with st.container():
        # 依照 size 比例縮放魯夫
        zoom = st.session_state.luffy_size / 100
        st.markdown(f"""
        <div class='pet-box'>
            <div style='transform: scale({zoom}); display:inline-block;'>
                <img src='https://img.vavel.com/luffy-gear-5-1691176219803.jpg' class='luffy-img'>
            </div>
            <p style='margin-top:10px;'>🍖 正在待機中... 🍖</p>
            
            <div class='stat-container'>
                LV.{st.session_state.luffy_lv} 魯夫 [LUFFY] <br>
                HUNGER (能源): {st.session_state.luffy_size}%
                <div class='stat-bar'><div class='stat-fill-orange' style='width:{min(st.session_state.luffy_size/2.5, 100)}%'></div></div>
                EXP (經驗): {st.session_state.luffy_exp}%
                <div class='stat-bar'><div class='stat-fill-green' style='width:{st.session_state.luffy_exp}%'></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 底部按鈕區
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("FEED ME (餵食)"):
            st.session_state.luffy_size += 30
            st.session_state.luffy_exp = min(100, st.session_state.luffy_exp + 10)
            st.session_state.search_history.append({"Time": datetime.now().strftime("%H:%M"), "Action": "Feed Luffy"})
            
            if st.session_state.luffy_size > 250:
                st.error("💥 LUFFY OVERLOAD! 魯夫爆炸了！")
                st.balloons()
                st.session_state.luffy_size = 100 # 重生
                st.session_state.luffy_lv += 1
            st.rerun()
            
    with col_b:
        if st.button("SYSTEM MENU"):
            st.session_state.show_menu = True
            st.rerun()
            
    with col_c:
        if st.button("RESET PET"):
            st.session_state.luffy_size = 100
            st.session_state.luffy_lv = 1
            st.rerun()

# --- 6. 功能選單 ---
else:
    if st.button("↩ BACK TO SYSTEM"):
        st.session_state.show_menu = False; st.rerun()
    
    t1, t2 = st.tabs(["[ DATA ANALYZER ]", "[ ENTERTAINMENT ]"])
    with t1:
        st.subheader("🤖 機械臂軸向解析")
        file = st.file_uploader("UPLOAD LOG")
        if file: st.success("數據讀取中...")
    with t2:
        st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" style="text-decoration:none;"><div style="background:#e60012; color:white; padding:15px; text-align:center; border-radius:5px;">🎮 進入 CS 1.6 戰場</div></a>', unsafe_allow_html=True)
        st.markdown('<a href="http://game.slime.com.tw/" target="_blank" style="text-decoration:none;"><div style="background:#004a99; color:white; padding:15px; text-align:center; border-radius:5px; margin-top:10px;">👾 史萊姆遊戲區</div></a>', unsafe_allow_html=True)
