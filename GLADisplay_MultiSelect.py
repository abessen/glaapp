from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st
import time
import datetime as dt
from datetime import datetime, timezone, timedelta
import subprocess
import openpyxl

# Page setting
st.set_page_config(layout="wide")

st.subheader("Real-Time / Live Data Dashboard: ")

this_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
wb_file_path = this_dir / 'GLA_Data.xlsx'

# ----- SideBar  ____
ySelect = st.sidebar.multiselect(
    label="Select Scales",
    options=["Cv2", "Cv26", "Cv23", "Cv32", "Cv35", "Cv36"],
    default=["Cv2"]
)

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
        usecols='A:BS',
        nrows=1441,
    )

    # Filter the DataFrame based on selected scales
    df = df[['DateTime'] + ySelect]

    # Melt the DataFrame to "long" format
    df = df.melt(id_vars=['DateTime'], var_name='Scale', value_name='Value')

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('DateTime', axis=alt.Axis(labelOverlap="greedy", grid=False)),
        y=alt.Y('Value', scale=alt.Scale(zero=False)),
        color='Scale'
    )

    chart_placeholder.altair_chart(chart, use_container_width=True)

    thistime = datetime.now(timezone(timedelta(hours=-4), 'EDT'))
    timenow = thistime.strftime("%m-%d-%y %H:%M:%S")
    last_updated_placeholder.markdown(f"Scales: {', '.join(ySelect)} - Last updated on -- {timenow}")

    df1 = pd.read_excel(
        io=wb_file_path,
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=1487,
        usecols='BM:CD',
        nrows=26,
    )

    dataframe_placeholder1.dataframe(df1, width=1500, height=240)

    df2 = pd.read_excel(
        io=wb_file_path,
        engine='openpyxl',
        sheet_name='Sheet1',
        skiprows=1495,
        usecols='BM:CD',
        nrows=6,
    )

    dataframe_placeholder2.dataframe(df2, width=1500, height=240)

    # Name of the Python script you want to run
    script_name = "UpdLinks.py"

    # Run the Python script using the same Python interpreter as the current script
    result = subprocess.run(["python", script_name], capture_output=True, text=True)

    # Check if the script executed successfully
    if result.returncode == 0:
        print("Script executed successfully.")
        print("Script output:")
      #  print(result.stdout)
    else:
        print("Script execution failed.")
        print("Error output:")
      #  print(result.stderr)

    # Refresh data every 30 seconds
    time.sleep(30)



