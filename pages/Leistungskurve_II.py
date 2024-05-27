import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from function import hold_power

st.title("Leistungskurve II")



data= pd.read_csv("Data/activity.csv")
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

table =pd.DataFrame({
        "Zeit" : durations,
        "Leistung" : power_lvs,
})

st.dataframe(table, hide_index=True)


