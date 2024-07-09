import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt


# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

if "current_ekg_id" not in st.session_state or not st.session_state.current_ekg_id:
    st.warning("Versuchen sie zuerst die Person und die Ekg-ID auszuwählen")
    st.stop()

ekg_data= ekgdata.load_ekg_table()
ekg_dict = ekg_data.get(doc_id=str(st.session_state.current_ekg_id))
st.write("Datum des Ekg-Tests =",ekg_dict["date"])

ekgdata1= ekgdata(st.session_state.current_ekg_id)

user_input_ekg_start= int(st.slider("Geben sie den Start Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),0,step=100))
user_input_ekg_end= int(st.slider("Geben sie den End Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),10000,step=100))

    # Plot EKG data with peaks
if user_input_ekg_start < user_input_ekg_end:
    st.plotly_chart(ekgdata1.plot_ekg_with_peaks(user_input_ekg_start,user_input_ekg_end))
st.write("Derzeit ist der Ekg_Test mit der ID", st.session_state.current_ekg_id ,"von", st.session_state.current_user,"ausgewählt")
user_input_ekg_start_2= int(st.slider("Geben sie den Start Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),0,step=10000,key="Slider3"))
user_input_ekg_end_2= int(st.slider("Geben sie den End Wert des Plots an",0, len(ekgdata1.df["Time in ms"]),100000,step=10000,key="Slider4"))
if user_input_ekg_start_2 < user_input_ekg_end_2:
    st.plotly_chart(ekgdata1.plot_ekg_with_peaks_hr(user_input_ekg_start_2,user_input_ekg_end_2))
st.title("EKG-Graph konnte nicht geladen werden!")
