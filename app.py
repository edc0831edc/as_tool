import streamlit as st
import pandas as pd

# 1. 基礎配置與 Session State
if "page_title" not in st.session_state:
    st.session_state.page_title = "TM ROBOT Data Analytics"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

st.set_page_config(page_title=st.session_state.page_title, layout="wide")

# 2. TM ROBOT 品牌視覺 CSS (深灰/黑色背景、科技藍按鈕、方正圖卡)
st.markdown("""
    <style>
    /* 全域背景色 */
    .stApp { background-color: #ffffff; }
    
    /* 頂部導航模擬 */
    .nav-bar {
        background-color: #1a1a1a;
        padding: 15px 50px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    /* 文字顏色強制修正 */
    h1, h2, h3, h4, p, span, label, div, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
    }

    /* TM 風格按鈕 */
    .stButton>button {
        background-color: #004a99 !important; /* TM 藍 */
        color: white !important;
        border-radius: 0px !important; /* TM 風格較為方正 */
        padding: 10px 25px !important;
        border: none !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
    }

    /* 功能方塊 (Card) */
    .feature-card {
        border: 1px solid #e0e0e0;
        padding: 30px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background-color: #fcfcfc;
    }
    .feature-card:hover {
        border-top: 5px solid #004a99;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* 表格樣式 */
    .stTable {
        border: 1px solid #eee !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 仿官網導航列 ---
st.markdown("""
    <div class='nav-bar'>
        <div style='font-size: 24px; font-weight: bold;'>TM ROBOT <span style='font-weight: 300; font-size: 16px;'>| Data Service</span></div>
        <div style='font-size: 14px;'>SUPPORT / PRODUCTS / SOLUTIONS</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. 管理員功能 (右上角小按鈕) ---
with st.sidebar:
    st.write("### ⚙️ 管理員選單")
    if st.text_input("Access Code", type="password") == "666":
        new_title = st.text_input("網站標題", st.session_state.page_title)
        if st.button("更新網站資訊"):
            st.session_state.page_title = new_title
            st.rerun()

# --- 5. 主內容區域 ---
if st.session_state.current_page == "Home":
    st.markdown("<h1 style='text-align: center;'>數據。賦予機器人智慧。</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666 !important;'>提供高效率的 Log 解析方案，精確提取關鍵圈數數據。</p>", unsafe_allow_html=True)
    st.write("---")

    # 功能網格 (Grid)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.subheader("🔄 運轉圈數查詢")
        st.write("解析各軸關節最終圈數結算 (2100/2200)")
        if st.button("立即進入 ＞", key="btn_cycle"):
            st.session_state.current_page = "CycleQuery"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.subheader("📈 負載監測")
        st.write("分析馬達電流與力矩變動趨勢")
        st.button("即將推出", disabled=True, key="btn_load")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.subheader("🛠️ 故障診斷")
        st.write("自動識別錯誤代碼與系統異常")
        st.button("即將推出", disabled=True, key="btn_diag")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. 運轉圈數查詢內頁 ---
elif st.session_state.current_page == "CycleQuery":
    st.markdown("## 運轉圈數結算分析")
    if st.button("＜ 返回首頁"):
        st.session_state.current_page = "Home"
        st.rerun()
    
    st.write("---")
    
    # 功能區排版
    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("請上傳您的 Log 檔案，系統將自動掃描 J1-J6 軸數據。")
        uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])

    with c2:
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
            
            extracted_data = []
            # 嚴格遵循 Eddie 提供之邏輯：
            # 1. 找 2100 (Object 宣告)
            # 2. 往後找 2200 (位置)
            # 3. 抓 OK: (值)
            for axis in range(1, 7):
                t_2100 = f"({axis},2100,00,1814"
                t_2200 = f"({axis},2200,00,"
                hex_str = "N/A"
                dec_val = 0
                
                # 從後往前找結算數據
                for i in range(len(lines)-1, -1, -1):
                    if t_2100 in lines[i]:
                        for j in range(i, min(i+15, len(lines))):
                            if t_2200 in lines[j]:
                                if j+1 < len(lines) and "OK:" in lines[j+1]:
                                    try:
                                        # 提取 OK: 後的字串
                                        hex_str = lines[j+1].split("OK:")[1].strip().split()[0]
                                        # 轉換 16 進位為 10 進位
                                        dec_val = int(hex_str, 16)
                                        break
                                    except: continue
                        if hex_str != "N/A": break
                
                extracted_data.append({
                    "軸向": f"J{axis} 軸",
                    "十六進位字串 (Hex)": hex_str,
                    "十進位圈數 (Decimal)": f"{dec_val:,}" if hex_str != "N/A" else "N/A"
                })

            st.write("#### 解析結果清單")
            st.table(pd.DataFrame(extracted_data))
