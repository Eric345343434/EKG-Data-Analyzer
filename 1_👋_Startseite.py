import streamlit as st
from PIL import Image
import json

# Laden der Benutzerdaten aus einer JSON-Datei
def load_users(file_path='Data/users.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Speichern der Benutzerdaten in einer JSON-Datei
def save_users(users, file_path='Data/users.json'):
    with open(file_path, 'w') as file:
        json.dump(users, file)

# Benutzerdaten laden
users = load_users()

# Funktion zum Einloggen
def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Funktion zum Registrieren neuer Benutzer
def register(username, password):
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# Überprüfen, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Anwendungsstart
st.markdown("<h1 style='text-align: center; color: grey;'>EKG-Data-Analyzer</h1>", unsafe_allow_html=True)
# Anwendungsstart

col1,col2 = st.columns(2)

with col1:
    try:
        logo = Image.open('Data/pictures/Logo.jpg')
        st.image(logo, caption='', width=logo.width // 4)
    except Exception as e:
        st.error(f"Logo konnte nicht geladen werden: {e}")
with col2:
    st.write("Willkommen auf der Startseite")
    st.write("Um EKG-Daten analysieren zu können, müssen Sie sich anmelden")
    st.write("Falls Sie noch keinen Account besitzen, registrieren Sie sich bitte.")

# Login-Formular
col1,col2 = st.columns(2)

with col1:
    if not st.session_state.logged_in:
        st.title("Login")
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Erfolgreich eingeloggt!")
                st.experimental_rerun()  # Neuladen der Anwendung für sichtbare Änderungen
            else:
                st.error("Ungültige Anmeldeinformationen")
with col2:       
    # Registrierungsformular
    if not st.session_state.logged_in:
        st.title("Registrieren")
        reg_username = st.text_input("Neuer Benutzername")
        reg_password = st.text_input("Neues Passwort", type="password")
        
        if st.button("Registrieren"):
            if register(reg_username, reg_password):
                st.success("Registrierung erfolgreich! Bitte melden Sie sich an.")
            else:
                st.error("Benutzername existiert bereits. Bitte wählen Sie einen anderen Benutzernamen.")

# Anzeigen des Inhalts nach erfolgreichem Login
if st.session_state.logged_in:
    st.header(f"Willkommen {st.session_state.username}!")
    st.write("Du bist erfolgreich eingeloggt!")
else:
    st.stop()  # Stoppt die weitere Ausführung der Seite, wenn nicht eingeloggt











