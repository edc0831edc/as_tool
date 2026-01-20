import streamlit as st
import pandas as pd

# 1. 頁面基礎配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Intelligence"
if "show_tool" not in st.session_state:
    st.session_state.show_tool = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. 強制高對比度 CSS (確保文字絕對清晰)
st.markdown(f"""
    <style>
    /* 強制全網頁純白背景 */
    .stApp {{
        background-color: #ffffff !important;
    }}

    /* 強制所有文字為「純黑色」，解決看不到字的問題 */
    h1, h2, h3, h4, h5, p, span, label, div, .stMarkdown, .stTable {{
        color: #000000 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}

    /* 主標題排版 */
    .hero-title {{
        font-size: 48px;
        font-weight: 700;
        line-height: 1.1;
        margin-top: 50px;
    }}
    .hero-subtitle {{
        font-size: 24px;
        color: #86868b !important; /* Apple 專屬灰色副標 */
        margin-top: 10px;
        margin-bottom: 30px;
    }}

    /* Apple 藍色圓角按鈕 */
    .stButton>button {{
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border-radius: 980px !important;
        padding: 12px 35px !important;
        font-size: 18px !important;
        border: none !important;
        font-weight: 500 !important;
    }}

    /* 點擊按鈕後出現的「內頁」容器 */
    .inner-page {{
        background-color: #f5f5f7; /* 淺灰色塊區分內頁 */
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #d2d2d7;
        margin-top: 20px;
    }}

    /* 表格樣式優化 */
    .stTable {{
        background-color: white !important;
        border-radius: 10px;
    }}
    
    /* 修正上傳檔案文字顏色 */
    [data-testid="stFileUploadDropzone"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頂部簡潔導航 ---
col_logo, col_admin = st.columns([5, 1])
with col_logo:
    st.markdown(f"<h2 style='margin:0;'> {st.session_state.page_title}</h2>", unsafe_allow_html=True)
with col_admin:
    # 管理員設定：點擊齒輪才開啟
    with st.popover("⚙️"):
        st.markdown("<p style='color:black;'>管理員登入</p>", unsafe_allow_html=True)
        pw = st.text_input("Password", type="password")
        if pw == "666":
            new_title = st.text_input("修改網頁標題", value=st.session_state.page_title)
            if st.button("確認更新"):
                st.session_state.page_title = new_title
                st.rerun()

st.markdown("<hr style='border: 0.5px solid #d2d2d7;'>", unsafe_allow_html=True)

# --- 4. 主畫面佈局 ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='hero-title'>大數據分析。<br>前所未有的簡單。</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>精確解析每一軸馬達運轉數據，<br>為您的機器人提供最強大的後盾。</div>", unsafe_allow_html=True)
    
    # 點擊此按鈕後，右側會出現工具
    if st.button("運轉圈數查詢 ＞"):
        st.session_state.show_tool = True
        st.rerun()

with col_right:
    if st.session_state.show_tool:
        # 這就是點擊按鈕後出現的「功能內頁」
        st.markdown('<div class="inner-page">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>檔案分析系統</h3>", unsafe_allow_html=True)
        st.write("請選擇或拖曳 Log 檔案至下方區塊：")
        
        uploaded_file = st.file_uploader("", type=["log", "txt"])

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            
            results = []
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
                
                results.append({"馬達軸向": f"J{axis}", "結算字串 (Hex)": final_hex})

            st.markdown("<br><b>解析完畢：</b>", unsafe_allow_html=True)
            st.table(pd.DataFrame(results))
            
            if st.button("✕ 關閉視窗"):
                st.session_state.show_tool = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # 未啟動時的空白導引
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; color:#86868b !important;'>← 點擊左側按鈕開始分析 Log</div>", unsafe_allow_html=True)
