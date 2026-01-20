import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 核心安全與狀態初始化 ---
def make_hashes(p): return hashlib.sha256(str.encode(p)).hexdigest()
def check_hashes(p, h): return make_hashes(p) == h
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state: st.session_state.search_history = []
if "show_menu" not in st.session_state: st.session_state.show_menu = False
if "luffy_size" not in st.session_state: st.session_state.luffy_size = 100 
if "luffy_lv" not in st.session_state: st.session_state.luffy_lv = 1
if "luffy_exp" not in st.session_state: st.session_state.luffy_exp = 20

st.set_page_config(page_title="BANDAM DATA SYSTEM", layout="wide")

# --- 2. 鋼彈科技 UI 樣式表 ---
st.markdown("""
<style>
    .stApp { background-color: #050b10; color: #5ef3ff; }
    
    .bandai-top {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(0, 30, 60, 0.6); padding: 10px 20px;
        border-top: 3px solid #ff0000; border-bottom: 1px solid #5ef3ff;
        font-family: 'monospace'; font-weight: bold;
    }

    .pet-monitor {
        border: 2px solid #5ef3ff; border-radius: 15px;
        background: rgba(0, 10, 20, 0.8); padding: 30px;
        text-align: center; margin: 10px auto; max-width: 600px;
        box-shadow: 0 0 25px rgba(94, 243, 255, 0.3);
    }

    .luffy-frame {
        display: inline-block; margin: 20px;
        border: 3px solid #5ef3ff; border-radius: 15px;
        overflow: hidden; background: #000;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 15px #5ef3ff;
    }

    .stat-label { text-align: left; font-size: 14px; margin-top: 10px; color: #5ef3ff; }
    .stat-bar-bg { background: #1a2a33; height: 12px; border-radius: 6px; margin: 5px 0; overflow: hidden; }
    .bar-orange { background: linear-gradient(90deg, #ff6600, #ffcc00); height: 100%; }
    .bar-green { background: linear-gradient(90deg, #a2ff00, #5ef3ff); height: 100%; }

    .stButton>button {
        background: linear-gradient(180deg, #004a99 0%, #001a33 100%) !important;
        color: white !important; border: 1px solid #5ef3ff !important;
        font-weight: bold; width: 100%; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 頂部導航 ---
st.markdown("""
<div class='bandai-top'>
    <div style='color:#ff0000;'>◢ BANDAI HOBBY</div>
    <div style='letter-spacing: 3px;'>BANDAM DATA SYSTEM</div>
    <div style='color:#5ef3ff;'>G.U.EST SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# --- 4. 側邊欄 ---
with st.sidebar:
    st.markdown("### [ SYSTEM AUTH ]")
    if st.session_state.logged_in_user == "guest":
        u = st.text_input("PILOT ID", key="user_id")
        p = st.text_input("PASSKEY", type="password", key="user_pw")
        if st.button("VERIFY"):
            if u == "admin" and check_hashes(p, ADMIN_HASH):
                st.session_state.logged_in_user = "admin"; st.rerun()
            else: st.error("ACCESS DENIED")
    else:
        st.success(f"ONLINE: {st.session_state.logged_in_user.upper()}")
        if st.button("LOGOUT"): st.session_state.logged_in_user = "guest"; st.rerun()
        if st.session_state.logged_in_user == "admin":
            st.markdown("---")
            st.write("📋 任務日誌")
            st.dataframe(pd.DataFrame(st.session_state.search_history), hide_index=True)

# --- 5. 主首頁：五檔魯夫養育系統 ---
if not st.session_state.show_menu:
    st.markdown("<h2 style='text-align:center; margin-top:20px; color:#5ef3ff;'>“ONE PIECE PET SYSTEM”</h2>", unsafe_allow_html=True)
    
    # 魯夫縮放邏輯
    scale = st.session_state.luffy_size / 100
    
    st.markdown(f"""
    <div class='pet-monitor'>
        <div class='luffy-frame' style='transform: scale({scale});'>
            <img src='https://static.wikia.nocookie.net/onepiece/images/a/af/Luffy_Gear_5_Anime_Infobox.png' width='200'>
        </div>
        <p style='color:#5ef3ff; font-weight:bold;'>狀態：五檔型態能量充填中...</p>
        
        <div class='stat-label'>UNIT: Gear 5 Luffy [LV.{st.session_state.luffy_lv}]</div>
        <div class='stat-label'>PRESSURE (爆炸壓力): {st.session_state.luffy_size}%</div>
        <div class='stat-bar-bg'><div class='bar-orange' style='width:{min(st.session_state.luffy_size/2.5, 100)}%'></div></div>
        
        <div class='stat-label'>EXPERIENCE (進化經驗): {st.session_state.luffy_exp}%</div>
        <div class='stat-bar-bg'><div class='bar-green' style='width:{st.session_state.luffy_exp}%'></div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍖 餵食 (RUBBER GUM-GUM)"):
            st.session_state.luffy_size += 40
            st.session_state.luffy_exp = min(100, st.session_state.luffy_exp + 10)
            st.session_state.search_history.append({"時間": datetime.now().strftime("%H:%M"), "動作": "餵食", "狀態": f"體型{st.session_state.luffy_size}%"})
            
            # 爆炸重啟邏輯
            if st.session_state.luffy_size > 260:
                st.balloons()
                st.error("💥 💥 💥 BOOM!!! 魯夫像氣球一樣爆炸了！重新啟動中... 💥 💥 💥")
                st.session_state.luffy_size = 100
                st.session_state.luffy_lv += 1
            st.rerun()
            
    with col2:
        if st.button("📂 數據選單"):
            st.session_state.show_menu = True
            st.rerun()
            
    with col3:
        if st.button("♻️ 格式化系統"):
            st.session_state.luffy_size = 100
            st.session_state.luffy_lv = 1
            st.rerun()

# --- 6. 功能選單 ---
else:
    if st.button("← 返回系統駕駛艙"):
        st.session_state.show_menu = False; st.rerun()
        
    t1, t2 = st.tabs(["📊 數據解析", "🎮 娛樂終端"])
    with t1:
        st.subheader("🤖 鋼彈軸向解析引擎")
        file = st.file_uploader("上傳 Log 檔案", type=["log", "txt"])
        if file:
            st.success("數據接收成功，正在讀取圈數...")
            # 這裡可以放入之前的 J1-J6 解析代碼

    with t2:
        st.markdown('<a href="https://play-cs.com/zh/servers" target="_blank" style="text-decoration:none;"><div style="background:#e60012; color:white; padding:15px; text-align:center; border-radius:5px; font-weight:bold;">啟動 CS 1.6</div></a>', unsafe_allow_html=True)
        st.markdown('<a href="http://game.slime.com.tw/" target="_blank" style="text-decoration:none;"><div style="background:#004a99; color:white; padding:15px; text-align:center; border-radius:5px; margin-top:10px; font-weight:bold;">進入史萊姆遊戲區</div></a>', unsafe_allow_html=True)
