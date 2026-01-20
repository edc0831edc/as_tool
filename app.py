import streamlit as st
import pandas as pd

# --- 1. 初始化配置 ---
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Data Analytics"
if "show_tool" not in st.session_state:
    st.session_state.show_tool = False  # 控制是否顯示上傳功能

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# --- 2. CSS 強制視覺修正 (解決字體看不見與版面問題) ---
st.markdown(f"""
    <style>
    /* 強制設定全域背景與文字顏色 */
    .stApp {{ background-color: #ffffff; }}
    
    /* 所有的文字都強制設為深灰色/黑色，確保清晰 */
    p, span, label, h1, h2, h3, h4, .stMarkdown {{
        color: #1d1d1f !important;
        font-family: "SF Pro Display", "Helvetica Neue", sans-serif !important;
    }}
    
    /* 按鈕美化 */
    .stButton>button {{
        background-color: #0071e3;
        color: white !important;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 500;
    }}
    
    /* 右側容器邊框 */
    .right-box {{
        border: 1px solid #d2d2d7;
        padding: 30px;
        border-radius: 18px;
        background-color: #fafafa;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頂部導航列 (含管理員標題修改) ---
col_logo, col_admin = st.columns([4, 1])
with col_logo:
    st.title(f" {st.session_state.page_title}")
with col_admin:
    with st.popover("⚙️ 管理員"):
        user = st.text_input("帳號")
        pw = st.text_input("密碼", type="password")
        if st.button("登入"):
            if user == "eddie" and pw == "666":
                st.session_state.admin = True
        
        if st.session_state.get("admin"):
            new_title = st.text_input("修改標題", value=st.session_state.page_title)
            if st.button("更新"):
                st.session_state.page_title = new_title
                st.rerun()

st.markdown("---")

# --- 4. 主畫面佈局 ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("### 歡迎使用數據提取工具")
    st.write("這是一個專門為解析機器人 Log 檔案所設計的平台。簡單、精確、快速。")
    st.write("---")
    st.write("請點擊右側功能按鈕開始作業。")

with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 功能進入點：按鈕
    if st.button("🔄 運轉圈數查詢"):
        st.session_state.show_tool = True

    # 只有按下按鈕後，st.session_state.show_tool 變成 True，才顯示下面的內容
    if st.session_state.show_tool:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.write("#### 檔案解析系統")
        uploaded_file = st.file_uploader("請將 Log 檔案拖放到此處", type=["log", "txt"])

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            
            results = []
            # 嚴格執行 Eddie 的 2100 -> 2200 -> OK: 邏輯
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

            # 顯示結果表格
            st.write("##### 提取結果")
            st.table(pd.DataFrame(results))
            
            if st.button("關閉查詢區"):
                st.session_state.show_tool = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
