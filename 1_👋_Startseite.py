import streamlit as st
from function import person
from PIL import Image
import json

# Funktion zum Laden der Benutzerdaten aus einer JSON-Datei
def load_users(file_path='users.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Funktion zum Speichern der Benutzerdaten in einer JSON-Datei
def save_users(users, file_path='users.json'):
    with open(file_path, 'w') as file:
        json.dump(users, file)

# Benutzer laden
users = load_users()

def login(username, password):
    if username in users and users[username] == password:
        return True
    return False

def register(username, password):
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# Überprüfe, ob der Benutzer eingeloggt ist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Zeige das Logo
st.title("EKG-Data-Analyzer")
try:
    logo = Image.open('data/pictures/Logo.jpg')
    st.image(logo, caption='', width=logo.width // 4)
except Exception as e:
    st.error(f"Logo konnte nicht geladen werden: {e}")

st.write("Willkommen auf der Startseite")

# Login
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
    
    # Registrierung
    st.title("Registrieren")
    reg_username = st.text_input("Neuer Benutzername")
    reg_password = st.text_input("Neues Passwort", type="password")
    
    if st.button("Registrieren"):
        if register(reg_username, reg_password):
            st.success("Registrierung erfolgreich! Bitte melden Sie sich an.")
        else:
            st.error("Benutzername existiert bereits. Bitte wählen Sie einen anderen Benutzernamen.")


if st.session_state.logged_in:
    st.write(f"Willkommen {st.session_state.username}!")
    st.write("Du bist erfolgreich eingeloggt!")
else:
    st.stop()












