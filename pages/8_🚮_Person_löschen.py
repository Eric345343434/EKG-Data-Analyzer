import streamlit as st
from function import person, ekgdata

# Überprüfung, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Bitte loggen Sie sich zuerst ein!")
    st.stop()

# Laden der Personendaten
person_data = person.get_person_data()
person_names_list = person.get_person_names(person_data)

# Auswahl der zu löschenden Person
st.write("## Person und EKG-Tests löschen")
selected_person = st.selectbox(
    "Wählen Sie eine Person zum Löschen aus",
    options=person_names_list,
    key="delete_person"
)

if selected_person:
    person_data = person.find_person_data_by_name(selected_person)
    person_id = int(person.find_person_id_by_name(selected_person))

    if st.button("Person und zugehörige EKG-Tests löschen"):
        # Löschen der Person und der zugehörigen EKG-Tests
        person.delete_person(person_id)
        st.success(f"Person {selected_person} und alle zugehörigen EKG-Tests wurden gelöscht.")
