import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("📄 LogScope")
uploaded_file = st.file_uploader("Upload your .log file", type=["log", "txt"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post("http://127.0.0.1:8000/upload/", files=files)
        if response.status_code == 200:
            result = response.json()
            st.success(f"{result['parsed_entries']} log entries parsed from {result['filename']}")

            if "logs" in result:
                df = pd.DataFrame(result["logs"])
                st.info(f"Detected fields: {list(df.columns)}")

                if not df.empty:
                    # Access log timestamp fix
                    if "timestamp" in df.columns and df["timestamp"].dtype == object:
                        try:
                            df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")
                            if df["timestamp"].isnull().all():
                                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                        except Exception:
                            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

                    for col in df.columns:
                        if df[col].dtype == object and df[col].nunique() < 50:
                            selected = st.multiselect(f"Filter by {col}", sorted(df[col].dropna().unique()))
                            if selected:
                                df = df[df[col].isin(selected)]

                    st.dataframe(df)

                    plot_col = st.selectbox("Select column to visualize", df.columns)
                    st.plotly_chart(px.histogram(df, x=plot_col, title=f"Distribution of {plot_col}"))

                    if "timestamp" in df.columns and df["timestamp"].notnull().sum() > 0:
                        try:
                            time_df = df.groupby(df["timestamp"].dt.floor("S")).size().reset_index(name="count")
                            st.subheader("📈 Time Series Chart")
                            st.plotly_chart(px.line(time_df, x="timestamp", y="count"))
                        except Exception as e:
                            st.warning(f"Time series chart failed: {e}")
                    else:
                        st.warning("Timestamp could not be parsed in this log.")
        else:
            st.error(f"Upload failed. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
