import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np



#Plot

column_names = ["Duration","Distance","OriginalPace","HeartRate","Cadence","PowerOriginal","CalculatedPace","CalculatedStrideLength","CalculatedAerobicEfficiencyPace","CalculatedAerobicEfficiencyPower","CalculatedEfficiencyIndex"]
data= pd.read_csv("activity.csv")
print(data)
power_mean= data["PowerOriginal"].mean()
power_max= data["PowerOriginal"].max()
heartrate_mean= data["HeartRate"].mean()
heartrate_max= data["HeartRate"].max()


#Plot erstellen
fig = px.line(data["PowerOriginal"])
fig.update_layout(xaxis_title="Time", yaxis_title="Power (Watts)")
fig2 = px.line(data["HeartRate"])
fig.update_layout(xaxis_title="Time (s)", yaxis_title="Power (Watt), Hertrate(Hz)")
fig2.update_traces(line=dict(color="red"))
fig.add_traces(fig2.data)


zone_0 = 0.5*heartrate_max
zone_1 = 0.6*heartrate_max
zone_2 = 0.7*heartrate_max
zone_3 = 0.8*heartrate_max
zone_4 = 0.9*heartrate_max
zone_5 = heartrate_max

fig.add_hline(zone_0, color="white")
# Plot the DataFrame



#data["zone_1"] = np.where(data["HeartRate"]> zone_0 and data["HeartRate"]< zone_1, True, False)
#data["zone_2"] = np.where(data["HeartRate"]> zone_1 and data["HeartRate"]< zone_2, True, False)
#data["zone_3"] = np.where(data["HeartRate"]> zone_2 and data["HeartRate"]< zone_3, True, False)
#data["zone_4"] = np.where(data["HeartRate"]> zone_3 and data["HeartRate"]< zone_4, True, False)
#data["zone_5"] = np.where(data["HeartRate"]> zone_4 and data["HeartRate"]< zone_5, True, False)










st.title("Leistung und Herzrate")
st.plotly_chart(fig)
st.write("Mittelewert Leistung =",round(power_mean), "Maximale Leistung =",round(power_max))
st.write("Mittelwert Herzrate =",round(heartrate_mean), "Maximale Herzrate =",round(heartrate_max))

