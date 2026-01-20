import streamlit as st
import pandas as pd

st.set_page_config(page_title="Eddie Log Tool", layout="wide")
st.title("⚙️ 馬達圈數快速計算器")

uploaded_file = st.file_uploader("上傳 Log 檔案", type=["log", "txt"])

if uploaded_file:
    # 讀取檔案
    content = uploaded_file.read().decode("utf-8")
    lines = content.splitlines()
    
    results = []
    # 建立搜尋目標清單
    targets = {f"({i},2100,00,1814": f"J{i}" for i in range(1, 7)}
    found_axes = {}

    # 只掃描一遍檔案，速度最快
    for i, line in enumerate(lines):
        for key, axis_name in targets.items():
            if axis_name not in found_axes and key in line:
                # 找到關鍵字，直接看下方第 3 行
                try:
                    data_row = lines[i + 3]
                    if "OK:" in data_row:
                        hex_val = data_row.split("OK:")[1].strip().split()[0]
                        dec_val = int(hex_val, 16)
                        found_axes[axis_name] = {"Hex": hex_val, "Dec": dec_val}
                except:
                    continue
        
        # 如果 J1~J6 都抓到了，就提早停止搜尋，節省時間
        if len(found_axes) == 6:
            break

    # 整理成表格
    for i in range(1, 7):
        name = f"J{i}"
        data = found_axes.get(name, {"Hex": "未找到", "Dec": 0})
        results.append({
            "馬達軸向": name,
            "十六進制 (Hex)": data["Hex"],
            "十進制圈數 (Dec)": f"{data['Dec']:,}"
        })

    st.success("✅ 計算完成！")
    st.table(pd.DataFrame(results))
    
    # 顯示總合 (若有需要)
    total = sum(found_axes[name]["Dec"] for name in found_axes)
    st.metric("總累計圈數", f"{total:,}")

else:
    st.info("請上傳檔案，我會立即為您計算。")
