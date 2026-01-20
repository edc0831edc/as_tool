import streamlit as st
import pandas as pd

# 1. 網頁標題與顯示名稱 (Eddie 可自行修改)
st.set_page_config(page_title="Eddie 專屬工具", layout="wide")
st.title("🚀 Eddie 的自動化管理中心")

# 2. 登入系統
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.header("🔐 管理員登入")
    user = st.text_input("帳號")
    password = st.text_input("密碼", type="password")
    if st.button("確認登入"):
        if user == "Eddie" and password == "666": # 這裡自訂你的密碼
            st.session_state.logged_in = True
            st.success(f"歡迎回來, {user}!")
        else:
            st.error("帳密錯誤")

# 3. 功能區塊
tab1, tab2 = st.tabs(["🔄 運轉圈數查詢", "🛠 功能管理"])

with tab1:
    st.header("運轉圈數最終值提取")
    st.info("上傳 Log 後，系統將自動提取 J1-J6 的最後一筆正確數值。")
    
    uploaded_file = st.file_uploader("選取 Log 文件", type=["txt", "log"])

    if uploaded_file:
        # 讀取檔案內容並按行切割
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        results = []

        # 定義 J1 ~ J6 搜尋目標
        for i in range(1, 7):
            target_key = f"{i},2200,00"
            hex_val = "N/A"
            dec_val = 0

            # 【核心邏輯】從最後一行開始往前搜尋
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].strip() == target_key:
                    # 找到關鍵字後，確認下一行是否包含 OK:
                    if idx + 1 < len(lines) and "OK:" in lines[idx + 1]:
                        hex_val = lines[idx + 1].split("OK:")[1].strip()
                        # 16 進位轉 10 進位
                        dec_val = int(hex_val, 16)
                        break # 找到最後一筆，立刻跳出這一個 J 的搜尋
            
            results.append({
                "軸向": f"J{i}",
                "原始十六進制 (Hex)": hex_val,
                "十進制圈數 (Dec)": f"{dec_val:,}" if hex_val != "N/A" else "未找到"
            })
        
        # 顯示結果表格
        st.success("數據讀取完畢！")
        st.table(pd.DataFrame(results))

with tab2:
    if st.session_state.logged_in:
        st.header("Eddie 管理面板")
        st.write("你可以在這裡管理未來要增加的功能模組。")
        st.text_input("新功能名稱")
        st.button("確認新增")
    else:
        st.warning("🔒 管理功能僅限 Eddie 登入使用。")