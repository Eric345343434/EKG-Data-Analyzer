import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.title("Leistungskurve II")

def hold_power(values, times, power_lv):
    held_time = []
    start = None
    end = None

    for value, time in zip(values, times):

        if value >= power_lv and start is None:
            start = time

        if value < power_lv and end is None and start is not None:
            end = time
            held_time.append(end-start)
            start = None
            end = None

    return max(held_time)

data= pd.read_csv("activity.csv")
data.replace(np.nan,0, inplace=True)

print(data["PowerOriginal"].values[0])
values = data["PowerOriginal"].values
times = data["Duration"].index
print(times)

print(values)        
power_lvs = []  
durations = []
for power_lv in range(int(max(values)),int(min(values)),-1):
        power_lvs.append(power_lv)
        durations.append(hold_power(values, times, power_lv))





fig5 = px.line(x=durations, y=power_lvs)
fig5.update_layout(xaxis_title="Time", yaxis_title="Power (Watts)")
st.plotly_chart(fig5)



