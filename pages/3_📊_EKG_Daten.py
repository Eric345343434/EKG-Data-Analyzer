import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt

try:
    st.session_state.current_ekg_list = st.session_state.current_user_list["ekg_tests"]

    st.session_state.current_ekg_list_id = ekgdata.get_ids(st.session_state.current_ekg_list)

    st.write("## Ekg-Test auswählen") 
    st.session_state.current_ekg_id = st.selectbox( "", options = st.session_state.current_ekg_list_id, key= "ekg_tests")	










    st.write("Derzeit ist der Ekg_Test mit der ID", st.session_state.current_ekg_id ,"von", st.session_state.current_user,"ausgewählt")




    ekg_dict = ekgdata.load_by_id(st.session_state.current_ekg_id)
    st.write("Datum des Ekg-Tests =",ekg_dict["date"])


    ekgdata1= ekgdata(ekg_dict)
    st.write("Dauer des Ekg-Tests =",ekgdata.calc_duration(ekgdata1)*1000, "Millisekunden = ", ekgdata.calc_duration(ekgdata1), "Sekunden = ", ekgdata.calc_duration(ekgdata1)/60, "Minuten")
    peaks = ekgdata1.find_peaks()
    st.write("Heartrate:", ekgdata.estimate_hr(peaks))


    user_input_ekg_start= int(st.slider("Geben sie den Start Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),0,))
    user_input_ekg_end= int(st.slider("Geben sie den End Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),10000))

    # Plot EKG data with peaks
    st.plotly_chart(ekgdata1.plot_ekg_with_peaks(user_input_ekg_start,user_input_ekg_end))

except AttributeError:
    st.title("Wählen sie zuerst die Person aus")
