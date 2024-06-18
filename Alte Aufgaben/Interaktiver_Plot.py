import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np



st.title("Interaktiver Plot")
#Plot


column_names = ["Duration","Distance","OriginalPace","HeartRate","Cadence","PowerOriginal","CalculatedPace","CalculatedStrideLength","CalculatedAerobicEfficiencyPace","CalculatedAerobicEfficiencyPower","CalculatedEfficiencyIndex"]
data= pd.read_csv("Data/activity.csv")
print(data)
power_mean= data["PowerOriginal"].mean()
power_max= data["PowerOriginal"].max()
heartrate_mean= data["HeartRate"].mean()
heartrate_max= data["HeartRate"].max()



#Plot erstellen
fig = px.line(data["PowerOriginal"])
fig.update_layout(xaxis_title="Time", yaxis_title="Power (Watts)")
fig2 = px.line(data["HeartRate"])
fig.update_layout(xaxis_title="Time (s)", yaxis_title="Power (Watt), Heartrate(Hz)")
fig2.update_traces(line=dict(color="red"))
fig.add_traces(fig2.data)











#Mittelwert und Maximum ausgeben
st.header("Leistung und Herzrate")
st.plotly_chart(fig)
st.write("Mittelewert Leistung =",round(power_mean), "Maximale Leistung =",round(power_max))
st.write("Mittelwert Herzrate =",round(heartrate_mean), "Maximale Herzrate =",round(heartrate_max))


st.subheader("Tabelle der verschiedenen Anstrengunszonen")
heartrate_input = st.number_input("Max Heartrate eingeben:", value=heartrate_max)
#Zonen Ober und Untergrenzen
zone_0 = 0.5*heartrate_input
zone_1 = 0.6*heartrate_input
zone_2 = 0.7*heartrate_input
zone_3 = 0.8*heartrate_input
zone_4 = 0.9*heartrate_input
zone_5 = heartrate_input

#Zone 1-5 Erstellen
filtered_data_1 = data[(data["HeartRate"]> zone_0)& (data["HeartRate"]< zone_1)]

filtered_data_2 = data[(data["HeartRate"]> zone_1)& (data["HeartRate"]< zone_2)]

filtered_data_3 = data[(data["HeartRate"]> zone_2)& (data["HeartRate"]< zone_3)]

filtered_data_4 = data[(data["HeartRate"]> zone_3)& (data["HeartRate"]< zone_4)]

filtered_data_5 = data[(data["HeartRate"]> zone_4)& (data["HeartRate"]< zone_5)]

#Zeit und Mittelwert ausrechnen
mean_1 = filtered_data_1["PowerOriginal"].mean()
mean_2 = filtered_data_2["PowerOriginal"].mean()
mean_3 = filtered_data_3["PowerOriginal"].mean()
mean_4 = filtered_data_4["PowerOriginal"].mean()
mean_5 =  filtered_data_5["PowerOriginal"].mean()
time_1 = filtered_data_1["Duration"].sum()
time_2 = filtered_data_2["Duration"].sum()
time_3 = filtered_data_3["Duration"].sum()
time_4 = filtered_data_4["Duration"].sum()
time_5 = filtered_data_5["Duration"].sum()

#Tabelle der verschiedenen Zonen erstellen
table= pd.DataFrame({\
    "Zone" : ["1", "2", "3", "4", "5"],
    "Zeit in der Zone(s)":[time_1, time_2, time_3, time_4, time_5],
    "Durschnittliche Leistung(W)": [round(mean_1),round(mean_2),round(mean_3),round(mean_4),round(mean_5)]
})\

st.dataframe(table, hide_index= True)

