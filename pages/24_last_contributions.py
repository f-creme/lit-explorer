import streamlit as st
import pandas as pd
import numpy as np
import pyodbc

# Function to print stars
def print_stars(rating):
    if isinstance(rating, (int, float, np.floating)):
        return "⭐️" * int(rating) + "✰" * (5 - int(rating))
    else:
        return "✰✰✰✰✰"

# Page title
st.title("Working History")
st.write("See here the last contributions of users.")

num_contributions = st.slider("Number of contributions", 1, 50, 1, help="Select the number of contributions to display")
st.write("")

try:
    # Read the last contributions from the database
    conn = pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )
    query = f"""
            SELECT TOP {num_contributions} 
                    Users.Username, Contributions.ContributionType, FORMAT(Contributions.ContributionDate, 'DD MMM. YYYY - HH:MM') AS [DateOfContribution], 
                    Resources.Title, Reviews.Rating AS ReviewRating, Reviews.Review AS Review
            FROM ((Users 
            INNER JOIN Contributions ON Users.UserLogin = Contributions.UserLogin) 
            INNER JOIN Resources ON Contributions.ResourceID = Resources.ResourceID)
            LEFT JOIN Reviews ON Contributions.ContributionID = Reviews.ContributionID  
            ORDER BY Contributions.ContributionDate DESC;
            """
    contributions = pd.read_sql(query, conn)
    conn.close()

except Exception as e:
    st.error(f"Unable to connect to the database: {e}")

for contribution in contributions.iterrows():
    if contribution[1]["ContributionType"] == "New Resource":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 0;">
                &#127381;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution[1]['DateOfContribution']}</strong> {contribution[1]['Username']} added a new resource : <i>{contribution[1]['Title']}</i>
            </p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)

    elif contribution[1]["ContributionType"] == "Edit Resource":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 0;">
                &#128221;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution[1]['DateOfContribution']}</strong> {contribution[1]['Username']} edited details of : <i>{contribution[1]['Title']}</i>
            </p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)

    elif contribution[1]["ContributionType"] == "Add Review":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 0;">
                &#128161;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution[1]['DateOfContribution']}</strong> {contribution[1]['Username']} added a review to <i>{contribution[1]['Title']}</i>
            </p>
            <p style="margin: 0; text-align: center;">{print_stars(contribution[1]['ReviewRating'])}</p>
            <p style="margin: 0;">&laquo; {contribution[1]['Review']} &raquo;</p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)

    elif contribution[1]["ContributionType"] == "Edit Review":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 0;">
                &#128161;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution[1]['DateOfContribution']}</strong> {contribution[1]['Username']} edited a review to <i>{contribution[1]['Title']}</i>
            </p>
            <p style="margin: 0; text-align: center;">{print_stars(contribution[1]['ReviewRating'])}</p>
            <p style="margin: 0;">&laquo; {contribution[1]['Review']} &raquo;</p>
        </div>
        <p style="margin: 10;">&nbsp;</p>
        """, unsafe_allow_html=True)