import streamlit as st
from function import person, ekgdata
import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()


st.header("Wählen sie die beiden EKG-Daten aus, die Sie vergleichen wollen")

col1,col2 = st.columns(2)
with col1: 
    st.header("Ekg-Test 1")

    #Ekg Test 1
    person_data_1 = person.get_person_data()
    person_names_list_1 = person.get_person_names(person_data_1)

    st.session_state.current_user_1 = st.selectbox(
        "",
        options = person_names_list_1, key="sbVersuchspersons1")

    st.session_state.current_user_list_1 = person.find_person_data_by_name(st.session_state.current_user_1) 
    st.session_state.current_user_id_1 = int(person.find_person_id_by_name(st.session_state.current_user_1))

    st.session_state.current_ekg_list_id_1= ekgdata.get_ekg_ids_by_person_id(st.session_state.current_user_id_1)
    current_ekg_list_1 =[]
    for i in range(0,len(st.session_state.current_ekg_list_id_1)):
        current_ekg_list_1.append(ekgdata.load_by_ekg_id(st.session_state.current_ekg_list_id_1[i]))
    st.session_state.current_ekg_list_1 = current_ekg_list_1
    ekg_data_1= ekgdata.load_ekg_table()
    

    st.session_state.current_ekg_id_1 = st.selectbox(
            "",
            options=st.session_state.current_ekg_list_id_1,
            key="ekg_tests1",
           
        )   
        
    if "current_ekg_id" not in st.session_state:
            st.session_state.id = "None"

    ekg_dict_1 = ekg_data_1.get(doc_id=str(st.session_state.current_ekg_id_1))
    st.write("Datum =",ekg_dict_1["date"])

    ekgdata1= ekgdata(st.session_state.current_ekg_id_1)


        # Plot EKG data with peaks
    
           
with col2: 
     #Ekg Test 2
     st.header("Ekg-Test 2")
     person_data_2 = person.get_person_data()
     person_names_list_2 = person.get_person_names(person_data_2)

     st.session_state.current_user_2 = st.selectbox(
        "",
        options = person_names_list_2, key="sbVersuchspersons2")

     st.session_state.current_user_list_2 = person.find_person_data_by_name(st.session_state.current_user_2) 
     st.session_state.current_user_id_2 = int(person.find_person_id_by_name(st.session_state.current_user_2))

     st.session_state.current_ekg_list_id_2= ekgdata.get_ekg_ids_by_person_id(st.session_state.current_user_id_2)
     current_ekg_list_2 =[]
     for i in range(0,len(st.session_state.current_ekg_list_id_2)):
        current_ekg_list_2.append(ekgdata.load_by_ekg_id(st.session_state.current_ekg_list_id_2[i]))
     st.session_state.current_ekg_list_2 = current_ekg_list_2
     ekg_data_2= ekgdata.load_ekg_table()
     if len(st.session_state.current_ekg_list_id_2) > 1 :
                IN = 1
     else:
                IN = 0
     

     st.session_state.current_ekg_id_2 = st.selectbox(
            "",
            options=st.session_state.current_ekg_list_id_2,
            key="ekg_tests2",
            index = IN
        )   
        
     if "current_ekg_id_2" not in st.session_state:
            st.session_state.id = "None"
     ekg_dict_2 = ekg_data_2.get(doc_id=str(st.session_state.current_ekg_id_2))
     st.write("Datum =",ekg_dict_2["date"])

     ekgdata2= ekgdata(st.session_state.current_ekg_id_2)
     

     

        # Plot EKG data with peaks
st.session_state.user_input_ekg_start= int(st.slider("Geben sie den Start Wert des Plots an",0, max([len(ekgdata1.df["Time in ms"]),len(ekgdata2.df["Time in ms"])]),0,step=100))
st.session_state.user_input_ekg_end= int(st.slider("Geben sie den End Wert des Plots an",0, max([len(ekgdata1.df["Time in ms"]),len(ekgdata2.df["Time in ms"])]),1000,step=100))


ekgdata1.df["Time_0"]=ekgdata1.df0()
ekgdata2.df["Time_0"]=ekgdata2.df0()


df1 = ekgdata1.df.copy()[st.session_state.user_input_ekg_start:st.session_state.user_input_ekg_end]
df1['Peaks'] = 0
valid_peaks_1 = [p for p in ekgdata1.peaks_index if p in df1.index]
df1.loc[valid_peaks_1, 'Peaks'] = 1
df2 = ekgdata2.df.copy()[st.session_state.user_input_ekg_start:st.session_state.user_input_ekg_end]
df2['Peaks'] = 0
valid_peaks_2 = [p for p in ekgdata2.peaks_index if p in df2.index]
df2.loc[valid_peaks_2, 'Peaks'] = 1


fig= go.Figure()
fig.add_scatter(x=ekgdata1.df[ "Time_0"], y=df1['EKG in mV'], mode='lines', name='EKG-Test 1', marker=dict(color='blue'))
fig.add_scatter(x=ekgdata2.df[ "Time_0"], y=df2['EKG in mV'], mode='lines', name='EKG-Test 2', marker=dict(color='cyan'))
fig.add_scatter(x=df1.loc[valid_peaks_1, "Time_0"]-st.session_state.user_input_ekg_start, y=df1.loc[valid_peaks_1, 'EKG in mV'], mode='markers', name='Peaks 1', marker=dict(color='darkred'))
fig.add_scatter(x=df2.loc[valid_peaks_2, "Time_0"]-st.session_state.user_input_ekg_start, y=df2.loc[valid_peaks_2, 'EKG in mV'], mode='markers', name='Peaks 2', marker=dict(color='tomato'))
fig.update_layout(xaxis_title="Time (ms)", yaxis_title="EKG (mV)")
st.plotly_chart(fig)

#Herzrate-Plot
st.session_state.user_input_ekg_start_2= int(st.slider("Geben sie den Start Wert des Plots an",0, max([len(ekgdata1.df["Time in ms"]),len(ekgdata2.df["Time in ms"])]),0,key="slider3",step=1000))
st.session_state.user_input_ekg_end_2= int(st.slider("Geben sie den End Wert des Plots an",0, max([len(ekgdata1.df["Time in ms"]),len(ekgdata2.df["Time in ms"])]),100000,key="slider4",step=1000))
df1_h = ekgdata1.df.copy()[st.session_state.user_input_ekg_start_2:st.session_state.user_input_ekg_end_2]
df1_h['Peaks'] = 0
valid_peaks_1_h = [p for p in ekgdata1.peaks_index if p in df1_h.index]
df1_h.loc[valid_peaks_1_h, 'Peaks'] = 1
hr_1=[]
for z in range(0,int(len(valid_peaks_1_h)-10)):
    time_differences = [valid_peaks_1_h[i] - valid_peaks_1_h[i - 1] for i in range(1+z, 10+z) if valid_peaks_1_h[i] - valid_peaks_1_h[i - 1] > 200]
    if len(time_differences) > 0:
        avg_time_diff = sum(time_differences) / len(time_differences)
        avg_time_diff_s = avg_time_diff / 1000
        heart_rate = 60 / avg_time_diff_s
        if heart_rate/2 > int(ekgdata1.estimate_hr(ekgdata1.peaks)/2):
             hr_1.append(heart_rate/2)


df2_h = ekgdata2.df.copy()[st.session_state.user_input_ekg_start_2:st.session_state.user_input_ekg_end_2]
df2_h['Peaks'] = 0
valid_peaks_2_h = [p for p in ekgdata2.peaks_index if p in df2_h.index]
df2_h.loc[valid_peaks_2_h, 'Peaks'] = 1
hr_2=[]
for x in range(0,int(len(valid_peaks_2_h)-10)):
    time_differences_2 = [valid_peaks_2_h[b] - valid_peaks_2_h[b - 1] for b in range(1+x, 10+x) if valid_peaks_2_h[b] - valid_peaks_2_h[b - 1] > 200]
    if len(time_differences_2) > 0:
        avg_time_diff_2 = sum(time_differences_2) / len(time_differences_2)
        avg_time_diff_s_2 = avg_time_diff_2 / 1000
        heart_rate_2 = 60 / avg_time_diff_s_2
        if heart_rate_2/2 > int(ekgdata2.estimate_hr(ekgdata2.peaks)/2):
             hr_2.append(heart_rate_2/2)

fig2= go.Figure()
fig2.update_layout(xaxis_title="Time (ms)", yaxis_title="Herzrate")
fig2.add_scatter(x=df1_h.loc[valid_peaks_1_h, "Time_0"]-st.session_state.user_input_ekg_start_2, y=hr_1, mode='lines', name='Herzrate 1', marker=dict(color='darkred'))
fig2.add_scatter(x=df2_h.loc[valid_peaks_2_h, "Time_0"]-st.session_state.user_input_ekg_start_2, y=hr_2, mode='lines', name='Herzrate 2', marker=dict(color='blue'))
st.plotly_chart(fig2)
