import streamlit as st
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="Eddie Log Tool", layout="wide")
st.title("⚙️ 馬達圈數自動提取工具")

# 上傳檔案
uploaded_file = st.file_uploader("請上傳您的 Log 檔案 (.log 或 .txt)", type=["log", "txt"])

if uploaded_file:
    # 讀取檔案內容
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    
    results = []
    
    # 按照 Eddie 的手動邏輯：
    # 1. 從頭找 J1 到 J6
    for axis in range(1, 7):
        # 建立搜尋關鍵字，例如 (1,2100,00,1814
        target = f"({axis},2100,00,1814"
        found = False
        
        for i, line in enumerate(lines):
            if target in line:
                # 2. 找到關鍵字後，定位到「下面第 3 行」
                data_row_idx = i + 3
                if data_row_idx < len(lines) and "OK:" in lines[data_row_idx]:
                    # 3. 抓取 OK: 冒號後面的數值
                    try:
                        # 用冒號分割並取第一個空格後的字串
                        raw_val = lines[data_row_idx].split("OK:")[1].strip().split()[0]
                        results.append({
                            "馬達軸向": f"J{axis}",
                            "十六進制 (Hex)": raw_val,
                            "十進制圈數": int(raw_val, 16)
                        })
                        found = True
                        break # 抓到第一個就跳出，換下一軸
                    except:
                        continue
        
        if not found:
            results.append({"馬達軸向": f"J{axis}", "十六進制 (Hex)": "找不到數據", "十進制圈數": 0})

    # 顯示結果表格
    df = pd.DataFrame(results)
    
    # 美化數字顯示 (加千分位)
    df["十進制圈數"] = df["十進制圈數"].apply(lambda x: f"{x:,}")
    
    st.success("數據提取完成！")
    st.table(df)

    # 提供下載按鈕
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("下載