import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# Page title
st.title("Contributors")
st.write("See here the contributors to the platform.")

try:
    conn = pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )
    query = f"SELECT * FROM Users;"
    contributors = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f":x: Error fetching contributors: {e}")
    st.stop()

# Sort contributors by contributions (descending) and assign ranks
contributors = contributors.sort_values(by="UserContributions", ascending=False).reset_index(drop=True)
contributors["Rank"] = contributors.index + 1  # Assign ranks starting from 1

# Sidebar for filtering
st.sidebar.subheader("Research")
filter_name = st.sidebar.text_input("Filter by Name", help="Type the name of the contributor to filter")

if filter_name:
    contributors = contributors[contributors["Username"].str.contains(filter_name, case=False, na=False)]


# Define CSS styles for the ranks
rank_styles = {
    1: "7px solid gold",      # Gold for the top contributor
    2: "6px solid silver",    # Silver for the second
    3: "5px solid darksalmon"     # Bronze for the third
}

for _, contributor in contributors.iterrows():
    rank = contributor["Rank"]
    border_style = rank_styles.get(rank, "none")  # Default to no border if not top 3
    
    rounded_image_css = f"""
                        <style>
                            .rounded-image-{rank} {{
                                display: block;
                                margin: 0 auto;
                                border-radius: 50%;
                                width: 110px; 
                                height: 110px;
                                object-fit: cover;
                                border: {border_style};
                            }}
                        </style>
                        <img class="rounded-image-{rank}" src="{contributor["UserPicURL"]}" alt="Rounded Image">
                        """
    
    col1, col2 = st.columns([2,6], vertical_alignment="center", gap="small")
    with col1:
        st.markdown(rounded_image_css, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<h5 style="text-align: LEFT;">{contributor["Username"]}</h5>""", unsafe_allow_html=True)
        col3, col4 = st.columns([3,3], gap="small")
        with col3:
            st.markdown(f"""
                        <p style="margin: 0;">{contributor["UserRole"]}</p>
                        <p style="margin: 0;">{contributor["UserContributions"]} contributions since {np.datetime64(contributor["UserRegDate"], 'D').astype('datetime64[D]').astype(datetime).strftime("%d %b %Y")}</p>
                        <p style="margin: 0;">{contributor["UserMail"]}</p>
                        """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                        <p style="margin: 0;">{contributor["UserDesc"]}</p>
                        """, unsafe_allow_html=True)
    st.markdown("""<p style="margin: 10px;">&nbsp;</p>""", unsafe_allow_html=True)


