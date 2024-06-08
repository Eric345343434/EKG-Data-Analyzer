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

if "id" not in st.session_state:
    st.session_state.id = "None"





# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

# Eine Auswahlbox, das Ergebnis wird in current_user gespeichert
st.session_state.current_user = st.selectbox(
    "",
    options = person_names_list, key="sbVersuchspersons")

current_user_list = person.find_person_data_by_name(st.session_state.current_user) 
current_user_id = int(current_user_list["id"])
current_ekg_list = current_user_list["ekg_tests"]

# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
if st.session_state.current_user in person_names_list:
    image = Image.open(current_user_list["picture_path"])
# Anzeigen eines Bilds mit Caption
    st.image(image, caption=st.session_state.current_user)




st.write(st.session_state.current_user,"wird zurzeit gewählt")


st.session_state.current_ekg_list_id = ekgdata.get_ids(current_ekg_list)

st.write("## Ekg-Test auswählen") 
st.session_state.current_ekg_id = st.selectbox( "", options = st.session_state.current_ekg_list_id, key= "ekg_tests")	






st.write("Derzeit ist der Ekg_Test mit der ID", st.session_state.current_ekg_id ,"von", st.session_state.current_user,"ausgewählt")




ekg_dict = ekgdata.load_by_id(st.session_state.current_ekg_id)

ekgdata1= ekgdata(ekg_dict)
peaks = ekgdata1.find_peaks()
st.write( ekgdata.estimate_hr(peaks))
# Plot EKG data with peaks
st.plotly_chart(ekgdata1.plot_ekg_with_peaks())






