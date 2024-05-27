import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt


st.title("Wilkommen bei  unserer Startseite")

person_data = person.get_person_data()
person_names_list = person.get_person_names(person_data)
print(person_names_list)

# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

if "current-user" not in st.session_state:
    st.session_state.current_user ="None"

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

if 'result_link' not in st.session_state:
    st.session_state.result_link = "None"

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

# Eine Auswahlbox, das Ergebnis wird in current_user gespeichert
st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options = person_names_list, key="sbVersuchsperson")

st.write(st.session_state.current_user,"wird zurzeit gewählt")
current_user_list = person.find_person_data_by_name(st.session_state.current_user) 

st.write("Geburtsjahr = ",current_user_list["date_of_birth"],)






# Anlegen des Session State. Bild, wenn es kein Bild gibt




# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
if st.session_state.current_user in person_names_list:
    image = Image.open(current_user_list["picture_path"])
# Anzeigen eines Bilds mit Caption
    st.image(image, caption=st.session_state.current_user)


