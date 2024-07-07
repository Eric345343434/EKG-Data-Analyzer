import streamlit as st
from function import person,ekgdata
from PIL import Image
import matplotlib.pyplot as plt



# Eine Überschrift der ersten Ebene
st.title("EKG-Data-Analyzer") 
st.write("Willkommen auf der Startseite ")


# Load the logo image
logo = Image.open('Data\pictures\Logo.jpg')

# Display the logo
st.image(logo, caption='', use_column_width=True)










