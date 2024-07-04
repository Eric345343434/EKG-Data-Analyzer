import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt

try:
    st.session_state.current_ekg_list = ekgdata.load_by_ekg_id(ekgdata.get_ekg_ids_by_person_id(st.session_state.current_user_list))

    st.session_state.current_ekg_list_id = ekgdata.get_ekg_ids_by_person_id(st.session_state.current_ekg_list)

    st.write("## Ekg-Test auswählen") 
    
    #st.session_state.current_ekg_id = st.selectbox( "", options = st.session_state.current_ekg_list_id, key= "ekg_tests")
    
    st.session_state.current_ekg_id = st.selectbox(
        "",
        options=st.session_state.current_ekg_list_id,
        key="ekg_tests",
        index=st.session_state.current_ekg_list_id.index(st.session_state.current_ekg_id) if st.session_state.current_ekg_id in st.session_state.current_ekg_list_id else 0
    )




    st.write("Derzeit ist der Ekg_Test mit der ID", st.session_state.current_ekg_id ,"von", st.session_state.current_user,"ausgewählt")




    ekg_dict = ekgdata.load_by_id(st.session_state.current_ekg_id)
    st.write("Datum des Ekg-Tests =",ekg_dict["date"])


    ekgdata1= ekgdata(ekg_dict)
    st.write("Dauer des Ekg-Tests =",ekgdata.calc_duration(ekgdata1)*1000, "Millisekunden = ", ekgdata.calc_duration(ekgdata1), "Sekunden = ", ekgdata.calc_duration(ekgdata1)/60, "Minuten")
    peaks = ekgdata1.find_peaks()
    st.write("Heartrate:", ekgdata.estimate_hr(peaks))


    

except AttributeError:
    st.title("Wählen sie zuerst die Person aus")
