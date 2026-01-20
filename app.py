import streamlit as st
import pandas as pd

# 1. 必須是 Streamlit 的第一個指令
if "page_title" not in st.session_state:
    st.session_state.page_title = "🤖 機器人數據分析系統"

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. 初始化登入狀態
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 側邊欄：帳戶功能 ---
st.sidebar.title("🔐 系統存取")

if not st.session_state.logged_in:
    # 登入介面
    with st.sidebar.container():
        user = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        if st.button("登入"):
            if user == "eddie" and pw == "666":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.sidebar.error("❌ 帳號或密碼錯誤")
else:
    # 登入後的顯示
    st.sidebar.success("✅ 歡迎 Eddie (最高權限)")
    
    # 最高權限：修改標題功能
    with st.sidebar.expander("🛠️ 管理員設置", expanded=True):
        new_title = st.text_input("修改網頁標題", value=st.session_state.page_title)
        if st.button("立即更新標題"):
            st.session_state.page_title = new_title
            st.rerun()
            
    if st.sidebar.button("登出系統"):
        st.session_state.logged_in = False
        st.rerun()

# --- 主畫面標題 (與管理員設置連動) ---
st.title(st.session_state.page_title)

# --- 主要功能區塊 ---
uploaded_file = st.file_uploader("請上傳 Log 檔案", type=["log", "txt"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()

    # 功能方塊
    with st.expander("🔍 運轉圈數查詢", expanded=True):
        results = []
        # 嚴格執行 Eddie 的三步搜尋法
        for axis in range(1, 7):
            target_2100 = f"{axis},2100,00,1814"
            target_2200 = f"{axis},2200,00,"
            final_hex = "N/A"
            
            # 從後往前找結算點
            for i in range(len(lines) - 1, -1, -1):
                if target_2100 in lines[i]:
                    # 往下找 2200 (限制在接下來 10 行內)
                    for j in range(i, min(i + 10, len(lines))):
                        if target_2200 in lines[j]:
                            # 2200 的下一行 OK:
                            if j + 1 < len(lines) and "OK:" in lines[j + 1]:
                                try:
                                    final_hex = lines[j+1].split("OK:")[1].strip().split()[0]
                                    break
                                except: continue
                    if final_hex != "N/A": break
            
            results.append({"馬達軸向": f"J{axis}", "運轉圈數 (Hex)": final_hex})

        # 顯示結果表格
        st.table(pd.DataFrame(results))
        st.caption("提取邏輯：2100 -> 2200 -> Next Line OK: [結算值]")
else:
    st.info("請上傳 Log 檔案以進行數據查詢。")
