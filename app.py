import streamlit as st
import pandas as pd

# 1. 基礎設定
st.set_page_config(page_title="Eddie 的自動化工具", layout="wide")
st.title("🚀 Eddie 的自動化管理中心")

# 2. 登入權限設定 (Eddie 專屬)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.header("🔐 身分驗證")
    user = st.text_input("帳號")
    password = st.text_input("密碼", type="password")
    if st.button("管理員登入"):
        if user == "Eddie" and password == "666": 
            st.session_state.logged_in = True
            st.success("Eddie 歡迎回來！")
        else:
            st.error("登入失敗")

# 3. 功能選單
st.subheader("功能清單")
if st.button("🔄 運轉圈數查詢 (最終值)"):
    st.session_state.current_tool = "log_tool"

# 4. 運轉圈數查詢邏輯 (精準反向搜尋)
if st.session_state.get("current_tool") == "log_tool":
    st.divider()
    st.header("運轉圈數最終值查詢")
    st.info("系統將自動抓取 Log 文件中最後一次紀錄的 J1-J6 數據。")
    
    uploaded_file = st.file_uploader("請上傳 Log 檔案", type=["txt", "log"])

    if uploaded_file:
        # 讀取檔案內容
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        results = []

        # 從 J1 到 J6 依序搜尋
        for i in range(1, 7):
            target_key = f"{i},2200,00"
            hex_val = "N/A"
            dec_val = "N/A"

            # 【核心修改】從文件最後一行往回找
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].strip() == target_key:
                    # 找到關鍵字後，確認下一行是否有 OK:
                    if idx + 1 < len(lines) and "OK:" in lines[idx + 1]:
                        hex_val = lines[idx + 1].split("OK:")[1].strip()
                        # 執行 16 進位轉 10 進位
                        dec_val = int(hex_val, 16)
                        break # 找到最後一次出現的就跳出循環
            
            results.append({
                "馬達軸向": f"J{i}",
                "原始十六進制 (Hex)": hex_val,
                "十進制圈數 (Dec)": f"{dec_val:,}" if dec_val != "N/A" else "未找到"
            })
        
        # 顯示表格
        df = pd.DataFrame(results)
        st.success("數據提取成功！")
        st.table(df)

# 5. 管理面板 (登入後可見)
if st.session_state.logged_in:
    st.divider()
    st.header("🛠 Eddie 管理面板")
    st.write("目前狀態：已取得編輯權限")
    new_feat = st.text_input("輸入欲新增的功能名稱")
    if st.button("確認新增功能"):
        st.toast(f"功能 {new_feat} 已加入開發清單")