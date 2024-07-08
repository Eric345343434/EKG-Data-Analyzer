import streamlit as st
from function import person, ekgdata

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

# Überprüfen, ob eine Person ausgewählt wurde
if "current_user" in st.session_state:
    person_name = st.session_state.current_user
    person_data = person.find_person_data_by_name(person_name)
    person_id = int(person.find_person_id_by_name(person_name))
    
    st.write(f"Person: {person_name}")
    
    # Eingabefelder für den neuen EKG-Test
    st.write("### Neuen EKG-Test hinzufügen")
    
    date = st.date_input("Datum des EKG-Tests")
    result_link = st.text_input("Pfad zum EKG-Datensatz")
    
    if st.button("EKG-Test hinzufügen"):
        # Fügen Sie den neuen EKG-Test zur Datenbank hinzu
        ekgdata.add_ekg_test(person_id, str(date), result_link)
        st.success("Neuer EKG-Test wurde erfolgreich hinzugefügt!")
else:
    st.error("Bitte wählen Sie zuerst eine Person aus.")
