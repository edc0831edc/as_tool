import streamlit as st
import pandas as pd

st.set_page_config(page_title="Eddie Log Tool", layout="wide")
st.title("⚙️ 馬達圈數快速計算器 (Eddie 專用版)")

uploaded_file = st.file_uploader("請上傳 Log 檔案", type=["log", "txt"])

if uploaded_file:
    # 這裡用進度條提示，但邏輯很快就會跑完
    with st.spinner('正在極速搜尋數據...'):
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        
        results = []
        found_axes = {}
        # 建立 1~6 軸的搜尋標籤
        target_keys = {f"({i},2100,00,1814": f"J{i}" for i in range(1, 7)}

        # 極速掃描：一條龍找完即停
        for i, line in enumerate(lines):
            for key, axis_label in target_keys.items():
                if axis_label not in found_axes and key in line:
                    # 關鍵：找到指令，直接定位下 3 行
                    try:
                        data_row = lines[i + 3]
                        if "OK:" in data_row:
                            hex_val = data_row.split("OK:")[1].strip().split()[0]
                            found_axes[axis_label] = hex_val
                    except:
                        pass
            
            # 只要 J1~J6 都拿到了，就立刻結束，後面的幾萬行都不看了
            if len(found_axes) == 6:
                break

        # 整理成表格並計算十進制
        final_list = []
        for i in range(1, 7):
            name = f"J{i}"
            h_val = found_axes.get(name, "未找到")
            if h_val != "未找到":
                d_val = int(h_val, 16)
                final_list.append({
                    "馬達軸向": name,
                    "十六進制 (Hex)": h_val,
                    "十進制圈數 (Dec)": f"{d_val:,}"
                })
            else:
                final_list.append({"馬達軸向": name, "十六進制 (Hex)": "未找到", "十進制圈數 (Dec)": "-"})

        st.success("✅ 提取完成！")
        st.table(pd.DataFrame(final_list))

else:
    st.info("👋 Eddie，請上傳檔案，我會用最快的速度幫你算出結果。")
