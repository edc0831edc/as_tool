import streamlit as st
import pandas as pd

# ... (前面的登入與 UI 設定保持不變) ...

if st.session_state.get("current_tool") == "log_tool":
    st.header("🔄 運轉圈數最終值查詢")
    uploaded_file = st.file_uploader("請上傳 Log 檔案", type=["txt", "log"])

    if uploaded_file:
        # 讀取所有行
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        results = []

        # 從 J1 搜尋到 J6
        for i in range(1, 7):
            keyword = f"{i},2200,00"
            hex_val = "未找到"
            dec_val = 0

            # 關鍵修改：從最後一行往回搜尋
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].strip() == keyword:
                    if idx + 1 < len(lines) and "OK:" in lines[idx+1]:
                        hex_val = lines[idx+1].split("OK:")[1].strip()
                        # 轉換為 10 進位
                        dec_val = int(hex_val, 16)
                        break 
            
            results.append({
                "馬達軸向": f"J{i}",
                "原始十六進制 (Hex)": hex_val,
                "十進制圈數 (Dec)": f"{dec_val:,}" # 加上千分位符號
            })
        
        # 顯示結果
        st.success("已成功抓取文件最後一次出現的數值！")
        st.table(pd.DataFrame(results))
