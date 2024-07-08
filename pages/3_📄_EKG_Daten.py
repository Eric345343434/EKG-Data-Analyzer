import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

try:
    st.session_state.current_ekg_list_id= ekgdata.get_ekg_ids_by_person_id(st.session_state.current_user_id)
    current_ekg_list =[]
    for i in range(0,len(st.session_state.current_ekg_list_id)):
        current_ekg_list.append(ekgdata.load_by_ekg_id(st.session_state.current_ekg_list_id[i]))
    st.session_state.current_ekg_list = current_ekg_list
    ekg_data= ekgdata.load_ekg_table()
    
    st.write("## Ekg-Test auswählen") 
    
    
    st.session_state.current_ekg_id = st.selectbox(
        "",
        options=st.session_state.current_ekg_list_id,
        key="ekg_tests"
    )   
    
    if "current_ekg_id" not in st.session_state:
        st.session_state.id = "None"
    
    
    
    
    st.write("Derzeit ist der Ekg_Test mit der ID", st.session_state.current_ekg_id ,"von", st.session_state.current_user,"ausgewählt")
    
    
    
    
    ekg_dict = ekg_data.get(doc_id=str(st.session_state.current_ekg_id))
    st.write("Datum des Ekg-Tests =",ekg_dict["date"])
    
    
    ekgdata1= ekgdata(st.session_state.current_ekg_id)
    st.write("Dauer des Ekg-Tests =",ekgdata1.calc_duration()*1000, "Millisekunden = ", ekgdata1.calc_duration(), "Sekunden = ", ekgdata1.calc_duration()/60, "Minuten")
    peaks = ekgdata1.find_peaks()
    st.write("Heartrate:", ekgdata.estimate_hr(peaks))
except: 
    st.title("EKG-Daten konnten nicht geladen werden!")
    st.header("Versuchen sie zuerst die Person auszuwählen")


    

