import streamlit as st
import pandas as pd

# 1. 基礎配置
if "page_title" not in st.session_state:
    st.session_state.page_title = "Robot Intelligence"
if "show_tool" not in st.session_state:
    st.session_state.show_tool = False

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. Apple 精品等級 CSS 優化
st.markdown(f"""
    <style>
    /* 全域背景：Apple 經典淺灰白 */
    .stApp {{
        background-color: #f5f5f7;
    }}

    /* 字體與顏色：深黑色、SF Pro 風格 */
    h1, h2, h3, h4, p, span, label, .stMarkdown {{
        color: #1d1d1f !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        letter-spacing: -0.02em !important;
    }}

    /* 主標題大氣排版 */
    .main-hero {{
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: left;
    }}

    /* Apple 藍色膠囊按鈕 */
    .stButton>button {{
        background-color: #0071e3 !important;
        color: white !important;
        border-radius: 980px; /* 超圓角 */
        padding: 10px 30px !important;
        border: none !important;
        font-size: 17px !important;
        font-weight: 400 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 113, 227, 0.3);
    }}
    .stButton>button:hover {{
        background-color: #0077ed !important;
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(0, 113, 227, 0.4);
    }}

    /* 內頁卡片：毛玻璃白色容器 */
    .glass-card {{
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.04);
        margin-top: 20px;
    }}

    /* 隱藏預設元件邊框 */
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    .stFileUploader {{ border: none !important; }}
    
    /* 表格美化 */
    .stTable {{
        background: white;
        border-radius: 12px;
        overflow: hidden;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 頂部簡潔導航 ---
col_logo, col_admin = st.columns([5, 1])
with col_logo:
    st.markdown(f"<h3 style='margin:0;'> {st.session_state.page_title}</h3>", unsafe_allow_html=True)
with col_admin:
    with st.popover("⚙️ Admin"):
        pw = st.text_input("Password", type="password")
        if pw == "666":
            new_title = st.text_input("Site Name", value=st.session_state.page_title)
            if st.button("Save Changes"):
                st.session_state.page_title = new_title
                st.rerun()

# --- 4. 主視覺區域 (Hero Section) ---
st.markdown("<br><br>", unsafe_allow_html=True)

col_text, col_action = st.columns([1.2, 1], gap="large")

with col_text:
    st.markdown("<div class='main-hero'>大數據解析。<br>微秒級精確。</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #86868b !important; font-weight: 400;'>針對您的機器人 Log 檔案，提供最直覺的運轉圈數結算。讓複雜的數據，一眼看穿。</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    # 按鈕
    if st.button("🔄 開始查詢 ＞"):
        st.session_state.show_tool = True
        st.rerun()

with col_action:
    # 這裡就是你要求的「按鈕後才出現的內頁」
    if st.session_state.show_tool:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("分析工具")
        st.write("請將您的 .log 檔案拖移至此處")
        
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
                
                results.append({"馬達軸向": f"J{axis}", "數據 (Hex)": final_hex})

            # 顯示表格
            st.markdown("<br><b>解析結果：</b>", unsafe_allow_html=True)
            st.table(pd.DataFrame(results))
            
            if st.button("關閉分析"):
                st.session_state.show_tool = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # 未點擊按鈕時的留白圖案 (Placeholder)
        st.markdown("<div style='height: 300px; border: 2px dashed #d2d2d7; border-radius: 24px; display: flex; align-items: center; justify-content: center; color: #86868b;'>點擊左側按鈕開始分析</div>", unsafe_allow_html=True)
