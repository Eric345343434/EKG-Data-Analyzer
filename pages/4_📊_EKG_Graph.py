import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt
try:

    ekg_dict = ekgdata.load_by_id(st.session_state.current_ekg_id)
    st.write("Datum des Ekg-Tests =",ekg_dict["date"])

    ekgdata1= ekgdata(ekg_dict)

    user_input_ekg_start= int(st.slider("Geben sie den Start Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),0,))
    user_input_ekg_end= int(st.slider("Geben sie den End Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),10000))

        # Plot EKG data with peaks
    st.plotly_chart(ekgdata1.plot_ekg_with_peaks(user_input_ekg_start,user_input_ekg_end))
except:
    st.title("Wählen sie zuerst den EKG_Test aus")