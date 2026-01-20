import streamlit as st
import pandas as pd

# 1. 基礎配置與初始化
if "page_title" not in st.session_state:
    st.session_state.page_title = "🤖 機器人數據分析系統"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "首頁"

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 側邊欄：登入與導覽 ---
st.sidebar.title("🔐 系統選單")

if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        user = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        if st.form_submit_button("登入"):
            if user == "eddie" and pw == "666":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤")
else:
    st.sidebar.success(f"歡迎 Eddie (最高權限)")
    
    # 功能導覽按鈕
    if st.sidebar.button("🏠 回首頁"):
        st.session_state.current_page = "首頁"
        st.rerun()
        
    if st.sidebar.button("🔄 運轉圈數查詢"):
        st.session_state.current_page = "運轉圈數查詢"
        st.rerun()

    # 管理員設置
    with st.sidebar.expander("🛠️ 管理員設置"):
        new_title = st.text_input("修改網頁標題", value=st.session_state.page_title)
        if st.button("更新標題"):
            st.session_state.page_title = new_title
            st.rerun()
            
    if st.sidebar.button("登出"):
        st.session_state.logged_in = False
        st.session_state.current_page = "首頁"
        st.rerun()

# --- 主畫面顯示邏輯 ---
st.title(st.session_state.page_title)

if not st.session_state.logged_in:
    st.warning("請先由左側登入帳號以使用功能。")

elif st.session_state.current_page == "首頁":
    st.write("### 歡迎進入數據分析系統")
    st.info("請點選左側選單中的「運轉圈數查詢」開始作業。")

elif st.session_state.current_page == "運轉圈數查詢":
    st.write("## 🔄 運轉圈數查詢區")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("請上傳您的 Log 檔案 (.log / .txt)", type=["log", "txt"])

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        
        results = []
        # 嚴格執行 Eddie 的三步搜尋法 (2100 -> 2200 -> Next OK:)
        for axis in range(1, 7):
            target_2100 = f"{axis},2100,00,1814"
            target_2200 = f"{axis},2200,00,"
            final_hex = "N/A"
            
            # 由後往前找結算點
            for i in range(len(lines) - 1, -1, -1):
                if target_2100 in lines[i]:
                    for j in range(i, min(i + 15, len(lines))):
                        if target_2200 in lines[j]:
                            if j + 1 < len(lines) and "OK:" in lines[j + 1]:
                                try:
                                    final_hex = lines[j+1].split("OK:")[1].strip().split()[0]
                                    break
                                except: continue
                    if final_hex != "N/A": break
            
            results.append({"馬達軸向": f"J{axis}", "十六進制字串": final_hex})

        st.success("數據提取完畢")
        st.table(pd.DataFrame(results))
