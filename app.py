import streamlit as st
import pandas as pd

# 1. 初始化 Session State (用於儲存登入狀態與標題)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page_title" not in st.session_state:
    st.session_state.page_title = "🤖 機器人數據分析系統"

# 設定網頁基本配置 (標題會隨著變數連動)
st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 側邊欄：登入系統 ---
st.sidebar.title("🔐 系統存取")

if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        user = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        submit = st.form_submit_button("登入")
        
        if submit:
            if user == "eddie" and pw == "666":
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
else:
    st.sidebar.success(f"目前登入：{user if 'user' in locals() else 'eddie'} (最高權限)")
    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.rerun()

# --- 主畫面標題 ---
st.title(st.session_state.page_title)

# --- 最高權限專屬功能：修改標題 ---
if st.session_state.logged_in:
    with st.sidebar.expander("🛠️ 管理員設置"):
        new_title = st.text_input("修改網頁標題", value=st.session_state.page_title)
        if st.button("更新標題"):
            st.session_state.page_title = new_title
            st.rerun()

# --- 主要功能區 ---
uploaded_file = st.file_uploader("請上傳您的 Log 檔案 (.log / .txt)", type=["log", "txt"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()

    # --- 功能方塊：運轉圈數查詢 ---
    with st.expander("🔍 運轉圈數查詢", expanded=True):
        st.subheader("馬達結算數據提取")
        
        results = []
        # 嚴格執行：搜尋 x,2100 -> 下方找 x,2200 -> 下一行 OK:
        for axis in range(1, 7):
            target_2100 = f"{axis},2100,00,1814"
            target_2200 = f"{axis},2200,00,"
            found_val = "N/A"
            
            # 從後往前搜尋
            for i in range(len(lines) - 1, -1, -1):
                if target_2100 in lines[i]:
                    for j in range(i, min(i + 10, len(lines))):
                        if target_2200 in lines[j]:
                            if j + 1 < len(lines) and "OK:" in lines[j + 1]:
                                try:
                                    found_val = lines[j+1].split("OK:")[1].strip().split()[0]
                                    break
                                except: continue
                    if found_val != "N/A": break
            
            results.append({"馬達軸向": f"J{axis}", "十六進制 (Hex)": found_val})

        df = pd.DataFrame(results)
        st.table(df)
        st.info("💡 數據
