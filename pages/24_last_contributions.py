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
        contribution_message = f"added a new resource : \n*{contribution[1]['Title']}*"
    elif contribution[1]["ContributionType"] == "Edit Resource":
        contribution_message = f"edited details of *{contribution[1]['Title']}*"
    elif contribution[1]["ContributionType"] == "Add Review":
        contribution_message = f"""added a review to *{contribution[1]['Title']}*: 
                                \n({print_stars(contribution[1]['ReviewRating'])}) {contribution[1]['Review']}"""
    elif contribution[1]["ContributionType"] == "Edit Review":
        contribution_message = f"""edited a review to *{contribution[1]['Title']}*: 
                                \n({print_stars(contribution[1]['ReviewRating'])}) {contribution[1]['Review']}"""

    st.write(f"**{contribution[1]['DateOfContribution']}** {contribution[1]['Username']} {contribution_message}")
    st.markdown("---")