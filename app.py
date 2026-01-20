import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- 1. 安全加密工具 ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# 預設管理員密碼的 Hash 值 (這是 666 的加密值)
ADMIN_HASH = "104313f8e32d0834371900115049303a863d11b5e390c507c394c8e7e17a3a80"

# --- 2. 系統初始化 ---
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT AI Assistant"
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = "guest"
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "show_robot_menu" not in st.session_state:
    st.session_state.show_robot_menu = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 3. 手機優化與 TM 視覺 CSS ---
st.markdown(f"""
<style>
    .stApp {{ background-color: #ffffff; }}
    
    /* 手機字體調整 */
    @media (max-width: 600px) {{
        .hero-title {{ font-size: 24px !important; }}
        .robot-icon {{ font-size: 60px !important; }}
        .stButton>button {{ width: 100% !important; }}
    }}

    /* 頂部導航列 */
    .nav-header {{
        background-color: #1a1a1a;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-bottom: 3px solid #004a99;
    }}

    /* 機器人啟動區 */
    .robot-card {{
        border: 1px solid #eee;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        background: #fdfdfd;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* 側邊欄加密區塊樣式 */
    [data-testid="stSidebar"] {{
        background-color: #1a1a1a !important;
        border-right: 1px solid #333;
    }}
    [data-testid="stSidebar"] * {{ color: #ffffff !important; }}

    /* TM 藍色按鈕 */
    .stButton>button {{
        background-color: #004a99 !important;
        color: white !important;
        border-radius: 4px !important;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# --- 4. 頂部導航列 ---
st.markdown(f"""
<div class='nav-header'>
    <div style='font-size: 18px; font-weight: 700;'>TM ROBOT <span style='font-weight: 300;'>| Intelligence</span></div>
</div>
""", unsafe_allow_html=True)

# --- 5. 側邊欄：安全性管控後台 ---
with st.sidebar:
    st.markdown("### 🔐 安全管理中心")
    
    # 帳戶登入與加密校驗
    if st.session_state.logged_in_user == "guest":
        with st.expander("管理員登入"):
            user_input = st.text_input("Admin ID")
            pass_input = st.text_input("Security Key", type="password")
            if st.button("驗證身分"):
                if user_input == "admin" and check_hashes(pass_input, ADMIN_HASH):
                    st.session_state.logged_in_user = "admin"
                    st.success("身分已確認")
                    st.rerun()
                else:
                    st.error("密碼錯誤或權限不足")
    else:
        st.write(f"當前身分：{st.session_state.logged_in_user}")
        
        # 後台修改權限控管
        st.markdown("---")
        st.markdown("#### 🛠️ 核心設置")
        new_title = st.text_input("修改網頁標題", st.session_state.page_title)
        if st.button("更新網站資訊"):
            st.session_state.page_title = new_title
            st.toast("設定已更新")
            st.rerun()

        st.markdown("---")
        st.markdown("#### 📈 搜尋歷史回溯")
        if st.session_state.search_history:
            df = pd.DataFrame(st.session_state.search_history)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.caption("目前無紀錄")
            
        if st.button("安全登出"):
            st.session_state.logged_in_user = "guest"
            st.rerun()

# --- 6. 主頁面內容 (手機適應性排版) ---
if not st.session_state.show_robot_menu:
    st.markdown("<h2 class='hero-title' style='text-align:center; margin-top:30px;'>TM 智能助手</h2>", unsafe_allow_html=True)
    
    col_main1, col_main2, col_main3 = st.columns([1, 2, 1])
    with col_main2:
        st.markdown("""
        <div class='robot-card'>
            <div class='robot-icon' style='font-size: 80px;'>🤖</div>
            <p style='color:#666 !important; margin-top:10px;'>服務狀態：已連線</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("啟動運轉圈數查詢 ＞", use_container_width=True):
            st.session_state.show_robot_menu = True
            st.rerun()
else:
    # 功能內頁
    st.markdown("### 🔄 運轉圈數解析系統")
    if st.button("← 返回"):
        st.session_state.show_robot_menu = False
        st.rerun()

    st.write("---")
    
    # 使用 Container 讓手機顯示更整齊
    with st.container():
        st.markdown("#### 1. 上傳檔案")
        uploaded_file = st.file_uploader("選擇 Log 或 TXT 檔案", type=["log", "txt"])
        
        if uploaded_file:
            # 自動紀錄
            st.session_state.search_history.append({
                "時間": datetime.now().strftime("%m/%d %H:%M"),
                "帳戶": st.session_state.logged_in_user,
                "檔名": uploaded_file.name
            })
            
            # 數據解析邏輯
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            parsed_data = []
            
            for axis in range(1, 7):
                tag2100 = f"({axis},2100,00,1814"
                tag2200 = f"({axis},2200,00,"
                h_val, d_val = "N/A", 0
                
                for i in range(len(lines)-1, -1, -1):
                    if tag2100 in lines[i]:
                        for j in range(i, min(i+15, len(lines))):
                            if tag2200 in lines[j] and j+1 < len(lines) and "OK:" in lines[j+1]:
                                h_val = lines[j+1].split("OK:")[1].strip().split()[0]
                                d_val = int(h_val, 16)
                                break
                        if h_val != "N/A": break
                parsed_data.append({"軸向": f"J{axis}", "十六進位": h_val, "十進位圈數": f"{d_val:,}"})
            
            st.markdown("#### 2. 解析結果")
            # 手機端使用 dataframe 比較好滑動查看
            st.dataframe(pd.DataFrame(parsed_data), use_container_width=True, hide_index=True)
            st.success("數據提取完畢")
