import pandas as pd
import plotly.express as px
import streamlit as st

column_names = ["Duration","Distance","OriginalPace","HeartRate","Cadence","PowerOriginal","CalculatedPace","CalculatedStrideLength","CalculatedAerobicEfficiencyPace","CalculatedAerobicEfficiencyPower","CalculatedEfficiencyIndex"]
data= pd.read_csv("activity.csv")
print(data)
Power_mean= data["PowerOriginal"].mean()
power_max= data["PowerOriginal"].max()
fig = px.line(data["PowerOriginal"])
fig.update_layout(xaxis_title="Time", yaxis_title="Power (Watts)")
fig2 = px.line(data["HeartRate"])
fig.update_layout(xaxis_title="Time (s)", yaxis_title="Power (Watt), Hertrate(Hz)")
fig.add_traces(fig2.data)
fig.update_traces(line=dict(color=["aliceblue"]*2))
fig.show()
