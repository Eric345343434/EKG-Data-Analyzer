import streamlit as st
from function import person
from PIL import Image

# Benutzer 
users = {
    "Flo": "Flo123",
    "Erik": "Erik123",
    "user1": "Bratwurst123"
}

def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Überprüfe, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Zeige das Logo
st.title("EKG-Data-Analyzer")
try:
    logo = Image.open('data/pictures/Logo.jpg')  # Achten Sie auf den korrekten Pfad
    st.image(logo, caption='', use_column_width=True)
except Exception as e:
    st.error(f"Logo konnte nicht geladen werden: {e}")

st.write("Willkommen auf der Startseite")

# Login-Formular
if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Erfolgreich eingeloggt!")
            st.experimental_rerun()
        else:
            st.error("Ungültige Anmeldeinformationen")

# Zeige den restlichen Inhalt nach erfolgreichem Login
if st.session_state.logged_in:
    st.write(f"Willkommen {st.session_state.username}!")
    st.write("Du bist erfolgreich eingeloggt!")
else:
    st.stop()











