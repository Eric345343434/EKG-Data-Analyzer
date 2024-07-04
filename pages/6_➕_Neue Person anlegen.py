import streamlit as st
from function import person
from PIL import Image

st.title("Neue Person hinzufügen")

# Eingabeformulare
firstname = st.text_input("Vorname")
lastname = st.text_input("Nachname")
year_of_birth = st.number_input("Geburtsjahr", min_value=1900, max_value=2024, step=1)
picture_path = st.text_input("Pfad zum Bild")

# Wenn der Button geklickt wird, füge die Person hinzu
if st.button("Person hinzufügen"):
    if firstname and lastname and year_of_birth and picture_path:
        person.add_person(firstname, lastname, year_of_birth, picture_path)
        st.success(f"Person {firstname} {lastname} wurde erfolgreich hinzugefügt!")
    else:
        st.error("Bitte füllen Sie alle Felder aus.")

# Optional: Anzeigen eines Beispielbildes
if picture_path:
    try:
        image = Image.open(picture_path)
        st.image(image, caption=f"Bild von {firstname} {lastname}")
        st.write(f"Wenn Sie der angelegten Person einen EkG-Test hinzufügen möchten, wählen Sie diese unter 'Personenauswahl' aus und gehen dann auf 'Neuer EKG-Test anlegen'")
    except Exception as e:
        st.error(f"Bild konnte nicht geladen werden: {e}")

