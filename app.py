import streamlit as st
import pandas as pd

# 網頁基本設定
st.set_page_config(page_title="Eddie Log Tool", layout="wide")
st.title("⚙️ 馬達圈數自動計算工具")

# 上傳 Log 檔案
uploaded_file = st.file_uploader("請上傳 Log 檔案", type=["log", "txt"])

if uploaded_file:
    # 讀取檔案
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    
    results = []
    
    # 按照 Eddie 的搜尋邏輯：先搜關鍵字，找 J1~J6，跳 3 行
    for axis in range(1, 7):
        target = f"({axis},2100,00,1814"
        found_data = None
        
        for i, line in enumerate(lines):
            if target in line:
                # 定位到關鍵字下方第 3 行 (i + 3)
                data_row_idx = i + 3
                if data_row_idx < len(lines) and "OK:" in lines[data_row_idx]:
                    # 抓取 OK: 後面的十六進制值
                    try:
                        raw_hex = lines[data_row_idx].split("OK:")[1].strip().split()[0]
                        found_data = raw_hex
                        break # 找到第一組就換下一軸
                    except:
                        continue
        
        if found_data:
            # 進行十進制計算 (十六進制轉整數)
            dec_val = int(found_data, 16)
            results.append({
                "馬達軸向": f"J{axis}",
                "十六進制 (Hex)": found_data,
                "十進制圈數 (Dec)": dec_val
            })
        else:
            results.append({
                "馬達軸向": f"J{axis}",
                "十六進制 (Hex)": "未找到",
                "十進制圈數 (Dec)": 0
            })

    # 轉成 DataFrame 並美化顯示
    df = pd.DataFrame(results)
    
    # 格式化數字加上千分位
    styled_df = df.copy()
    styled_df["十進制圈數 (Dec)"] = styled_df["十進制圈數 (Dec)"].apply(lambda x: f"{x:,}")
    
    # 顯示結果
    st.success(f"✅ 檔案 {uploaded_file.name} 處理完成！")
    st.subheader("📊 提取結果")
    st.table(styled_df)

    # 如果有數據，顯示計算後的總和或其他資訊 (選配)
    total_count = df["十進制圈數 (Dec)"].sum()
    st.info(f"💡 總累計圈數：{total_count:,}")

else:
    st.info("👋 Eddie，請上傳 Log 檔案，我會自動幫你搜尋 2100,00,1814 並計算數據。")