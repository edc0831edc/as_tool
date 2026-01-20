import streamlit as st
import pandas as pd

# --- 1. 初始化配置 ---
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Data Analytics"
if "show_tool" not in st.session_state:
    st.session_state.show_tool = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 2. CSS 強制修正：確保字體深黑、背景純白、取消元件重疊 ---
st.markdown(f"""
    <style>
    /* 強制全域白色背景 */
    .stApp {{ background-color: #ffffff !important; }}
    
    /* 強制所有文字為深黑色，確保 100% 可視度 */
    h1, h2, h3, h4, p, span, label, .stMarkdown, .stTable {{
        color: #000000 !important;
        font-family: "SF Pro Display", -apple-system, sans-serif !important;
    }}
    
    /* 修正按鈕樣式 */
    .stButton>button {{
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border-radius: 20px;
        padding: 0.6rem 2.5rem;
        border: none;
        font-weight: 600;
        width: auto;
    }}
    
    /* 右側功能區塊容器：增加留白防止重疊 */
    .feature-box {{
        background-color: #f5f5f7;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #d2d2d7;
        margin-top: 20px;
    }}
    
    /* 修正上傳元件的文字顏色 */
    .stFileUploader label {{
        color: #000000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頂部導航列 ---
col_logo, col_admin = st.columns([5, 1])
with col_logo:
    st.title(f" {st.session_state.page_title}")
with col_admin:
    with st.popover("⚙️ Settings"):
        if st.text_input("Admin Password", type="password") == "666":
            new_title = st.text_input("Rename Site", value=st.session_state.page_title)
            if st.button("Update"):
                st.session_state.page_title = new_title
                st.rerun()

st.markdown("---")

# --- 4. 主畫面佈局 (使用固定間隔的 Columns) ---
col_left, col_space, col_right = st.columns([1, 0.2, 1])

with col_left:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("數據提取。從未如此簡單。")
    st.write("這是一個專門為解析機器人 Log 檔案所設計的平台。簡單、精確、快速。")
    st.write("請點擊右側功能按鈕開始作業。")

with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 點擊按鈕才開啟功能
    if st.button("🔄 執行運轉圈數查詢"):
        st.session_state.show_tool = True

    if st.session_state.show_tool:
        # 使用一個具備 Padding 的區塊來包裹，避免重疊
        st.markdown('###') # 增加間距
        with st.container(border=True):
            st.subheader("檔案解析系統")
            uploaded_file = st.file_uploader("請選擇 Log 檔案 (.log / .txt)", type=["log", "txt"])

            if uploaded_file:
                content = uploaded_file.read().decode("utf-8")
                lines = content.splitlines()
                
                results = []
                # 執行 2100 -> 2200 -> OK: 邏輯
                for axis in range(1, 7):
                    target_2100 = f"{axis},2100,00,1814"
                    target_2200 = f"{axis},2200,00,"
                    final_hex = "N/A"
                    
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
                    
                    results.append({"馬達軸向": f"J{axis}", "十六進制": final_hex})

                # 顯示表格
                st.write("**提取結果：**")
                st.table(pd.DataFrame(results))
                
                if st.button("完成並關閉"):
                    st.session_state.show_tool = False
                    st.rerun()
