import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import numpy as np

from forms.modify_profile import modify_profile_dialog

col1, col2 = st.columns([4,1], vertical_alignment="center", gap="large")
with col1:
    st.title("My Profile")
    st.write(f"Login : {st.session_state.userLogin}")
with col2:
    st.write("")
    modify = st.button("Modify", help="Click to modify your details", use_container_width=True)

try:
    conn = pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )
    query = f"SELECT * FROM Users WHERE UserID={st.session_state.userID};"
    user_data = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f"❌ Error fetching user data: {e}")
    st.stop()

st.markdown("---")

rounded_image_css = f"""
<style>
    .rounded-image {{
        display: block;
        margin: 0 auto;
        border-radius: 50%;
        width: 250px; 
        height: 250px;
        object-fit: cover;
    }}
</style>
<img class="rounded-image" src="{user_data["UserPicURL"].values[0]}" alt="Rounded Image">
"""

col3, col4 = st.columns(2, vertical_alignment="center", gap="large")
with col3:
    st.markdown(rounded_image_css, unsafe_allow_html=True)
    
with col4:
    st.subheader(f"{user_data["Username"].values[0]}", anchor=False)
    st.write(user_data["UserDesc"].values[0])
    st.write(f":briefcase: {user_data["UserRole"].values[0]} \n\n :email: {user_data["UserMail"].values[0]}")
    st.write(f"	:speech_balloon: {user_data["UserContributions"].values[0]} contributions since {np.datetime64(user_data["UserRegDate"].values[0], 'D').astype('datetime64[D]').astype(datetime).strftime("%d %b %Y")}")


if modify:
    modify_profile_dialog()