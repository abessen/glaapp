from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st
import time
import datetime as dt
from datetime import datetime, timezone, timedelta

# Page setting
st.set_page_config(layout="wide")

# dashboard title
st.subheader("Real-Time / Live Data Dashboard: ")

this_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
wb_file_path = this_dir / 'GLA_Data.xlsx'

#  ----- SideBar  ____
ySelect = st.sidebar.selectbox(label="Select Scale", options=["Cv2", "Cv26", "Cv23", "Cv32", "Cv35", "Cv36"])

# Add a stop button
stop_button = st.sidebar.button("Stop")

chart_placeholder = st.empty()
last_updated_placeholder = st.empty()
dataframe_placeholder1 = st.empty()
dataframe_placeholder2 = st.empty()

while not stop_button:
    df = pd.read_excel(
        io=wb_file_path,
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=18,
        usecols='BL:BS',
        nrows=1441,
    )

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('DateTime', axis=alt.Axis(labelOverlap="greedy", grid=False)),
        y=alt.Y(ySelect))

    chart_placeholder.altair_chart(chart, use_container_width=True)

    thistime = datetime.now(timezone(timedelta(hours=-4), 'EDT'))
    timenow = thistime.strftime("%m-%d-%y %H:%M:%S")
    last_updated_placeholder.markdown(f"{ySelect} Scale : last updated on -- {timenow}")

    df = pd.read_excel(
        io=wb_file_path,
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=1487,
        usecols='BM:CD',
        nrows=26,
    )

    dataframe_placeholder1.dataframe(df, width=1500, height=240)

    df = pd.read_excel(
        io=wb_file_path,
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=1495,
        usecols='BM:CD',
        nrows=6,
    )

    dataframe_placeholder2.dataframe(df, width=1500, height=240)

    # Refresh data every 30 seconds
    time.sleep(30)
