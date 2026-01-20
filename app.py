import streamlit as st
import pandas as pd

# 1. 初始化配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Intelligence"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. Apple 風格自定義 CSS
st.markdown("""
    <style>
    /* 全域背景色與字體 */
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { font-family: "SF Pro Display", "Helvetica Neue", Arial, sans-serif; color: #1d1d1f; letter-spacing: -0.02em; }
    
    /* 按鈕樣式：Apple 經典藍與圓角 */
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #0077ed; transform: scale(1.02); }
    
    /* 側邊欄與彈窗簡約化 */
    .stSidebar { background-color: #f5f5f7; border-right: 1px solid #d2d2d7; }
    
    /* 讓上傳區塊更優雅 */
    .stFileUploader { border: 1px dashed #d2d2d7; border-radius: 12px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部導航列 ---
col_logo, col_admin = st.columns([4, 1])
with col_logo:
    st.title(f" {st.session_state.page_title}")
with col_admin:
    # 帳戶功能收納在右上方的小按鈕中
    with st.popover("Account"):
        if not st.session_state.logged_in:
            user = st.text_input("ID")
            pw = st.text_input("Password", type="password")
            if st.button("Sign In"):
                if user == "eddie" and pw == "666":
                    st.session_state.logged_in = True
                    st.rerun()
        else:
            st.write(f"Logged in as: eddie")
            new_title = st.text_input("Change Site Title", value=st.session_state.page_title)
            if st.button("Update"):
                st.session_state.page_title = new_title
                st.rerun()
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

st.markdown("---")

# --- 主畫面佈局：左側文案，右側功能 ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("## 數據提取。從未如此簡單。")
    st.markdown("""
    #### 精確鎖定每一軸馬達的運轉狀態。
    針對自動化設備 Log 檔案開發的專屬解析引擎，
    無需登入，即刻體驗極速與精準。
    """)
    st.markdown("---")
    st.caption("Designed by Eddie. 支援所有標準傳輸格式。")

with col_right:
    # 這裡就是你要求的「功能按鈕」與「右側介面」
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 使用一個清爽的容器包裹功能
    with st.container():
        st.write("### 運轉圈數查詢")
        st.write("上傳您的 Log 檔案，我們將為您自動定位結算數值。")
        
        uploaded_file = st.file_uploader("", type=["log", "txt"], key="main_uploader")

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            
            results = []
            # 嚴格執行 2100 -> 2200 -> OK: 邏輯
            for axis in range(1, 7):
                target_2100 = f"{axis},2100,00,1814"
                target_2200 = f"{axis},2200,00,"
                final_hex = "N/A"
                
                # 從後往前搜尋確保抓到最新結算
                for i in range(len(lines) - 1, -1, -1):
                    if target_2100 in lines[i]:
                        # 搜尋 2200 標記
                        for j in range(i, min(i + 15, len(lines))):
                            if target_2200 in lines[j]:
                                # 鎖定 OK: 字串
                                if j + 1 < len(lines) and "OK:" in lines[j + 1]:
                                    try:
                                        final_hex = lines[j+1].split("OK:")[1].strip().split()[0]
                                        break
                                    except: continue
                        if final_hex != "N/A": break
                
                results.append({"馬達軸向": f"J{axis}", "運轉圈數 (Hex)": final_hex})

            # 使用簡潔的表格呈現
            st.table(pd.DataFrame(results))
            st.success("Analysis complete.")
