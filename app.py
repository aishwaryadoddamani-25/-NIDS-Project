
import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime

st.set_page_config(page_title="NIDS Dashboard", page_icon="🛡️")

st.title("🛡️ NIDS Security Dashboard")
st.write("Network Intrusion Detection System")
st.caption(f"Last analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

data = {
    "Source_IP": [
        "192.168.1.10", "192.168.1.11", "192.168.1.12",
        "192.168.1.20", "192.168.1.20", "192.168.1.20",
        "192.168.1.30", "192.168.1.31", "192.168.1.32",
        "192.168.1.40"
    ],
    "Packets": [20, 25, 30, 1500, 1700, 1600, 28, 35, 22, 30],
    "Bytes": [1200, 1500, 1800, 90000, 95000, 92000, 1400, 1600, 1300, 1500],
    "Connections": [5, 6, 7, 200, 250, 220, 6, 8, 5, 7]
}

df = pd.DataFrame(data)

model = IsolationForest(contamination=0.3, random_state=42)
df["Prediction"] = model.fit_predict(
    df[["Packets", "Bytes", "Connections"]]
)

df["Status"] = df["Prediction"].map({
    1: "NORMAL",
    -1: "INTRUSION DETECTED"
})

st.subheader("Traffic Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Normal", int((df["Prediction"] == 1).sum()))
col3.metric("Alerts", int((df["Prediction"] == -1).sum()))

st.subheader("Traffic Analysis")
st.dataframe(
    df[["Source_IP", "Packets", "Bytes", "Connections", "Status"]],
    use_container_width=True,
    hide_index=True
)

st.subheader("🚨 Security Alerts")
alerts = df[df["Prediction"] == -1]

if alerts.empty:
    st.success("No suspicious sample records detected.")
else:
    for _, row in alerts.iterrows():
        st.error(
            f'{row["Source_IP"]} — {row["Packets"]} packets, '
            f'{row["Bytes"]} bytes, {row["Connections"]} connections'
        )

st.info(
    "Demo only: analyzes 10 fixed sample records. "
    "It does not monitor live phone network traffic."
)
