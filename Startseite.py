import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt


st.title("Wilkommen bei  unserer Startseite")

person_data = person.get_person_data()
person_names_list = person.get_person_names(person_data)



# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

#St.session_state werden abgefragt
if "current-user" not in st.session_state:
    st.session_state.current_user ="None"

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

if 'ekg_tests' not in st.session_state:
    st.session_state.ekg_tests= "None"


#EKG Data kann geladen werden 
st.write("## Upload EKG Data")
st.session_state.result_link = st.file_uploader("Upload your EKG data file", type=["csv", "txt"])
# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

# Eine Auswahlbox, das Ergebnis wird in current_user gespeichert
st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options = person_names_list, key="sbVersuchsperson")


st.write(st.session_state.current_user,"wird zurzeit gewählt")
current_user_list = person.find_person_data_by_name(st.session_state.current_user) 

st.write("Geburtsjahr = ",current_user_list["date_of_birth"],)
st.write(st.session_state.ekg_tests)


current_ekg_data= ekgdata("data/ekg_data/01_Ruhe_short.txt")
current_ekg_data.plot_time_series()
st.pyplot(fig=current_ekg_data.fig)




# Anlegen des Session State. Bild, wenn es kein Bild gibt




# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
if st.session_state.current_user in person_names_list:
    image = Image.open(current_user_list["picture_path"])
# Anzeigen eines Bilds mit Caption
    st.image(image, caption=st.session_state.current_user)


