import streamlit as st

# 1. 基礎設定：這裡就是你自訂首頁名稱的地方
st.set_page_config(page_title="Eddie 的專案中心")
st.title("🚀 Eddie 的自動化管理中心")

# 2. 簡單的登入權限
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.header("身分驗證")
    user = st.text_input("帳號")
    password = st.text_input("密碼", type="password")
    if st.button("管理員登入"):
        if user == "Eddie" and password == "666": # 這裡可以自訂密碼
            st.session_state.logged_in = True
            st.success("Eddie 歡迎回來！")
        else:
            st.error("登入失敗")

# 3. 功能方塊顯示區
st.subheader("功能清單")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 運轉圈數查詢"):
        st.session_state.current_tool = "log_tool"

# 4. 運轉圈數查詢的具體邏輯
if st.session_state.get("current_tool") == "log_tool":
    st.divider()
    st.header("運轉圈數查詢系統")
    uploaded_file = st.file_uploader("請上傳 Log 文件", type=["txt", "log"])

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        results = []

        for i in range(1, 7):
            keyword = f"{i},2200,00"
            found_val = "未找到"
            for idx, line in enumerate(lines):
                if line.strip() == keyword:
                    if idx + 1 < len(lines) and "OK:" in lines[idx+1]:
                        hex_val = lines[idx+1].split("OK:")[1].strip()
                        found_val = int(hex_val, 16) # 16進制轉10進制
                        break
            results.append({"軸向": f"J{i}", "圈數(10進制)": found_val})
        
        st.table(results)

# 5. 管理員專屬：新增/修改功能
if st.session_state.logged_in:
    st.divider()
    st.header("🛠 Eddie 管理面板")
    st.text_input("新增功能名稱")
    st.button("確認新增")