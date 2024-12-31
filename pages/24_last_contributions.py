import streamlit as st
import pandas as pd
import numpy as np
import pyodbc
from datetime import datetime

# Function to print stars
def print_stars(rating):
    if isinstance(rating, (int, float, np.floating)):
        return "⭐" * int(rating) + "✩" * (5 - int(rating))
    else:
        return "✩✩✩✩✩"

# Page title
st.title("Working History")
st.write("See here the last contributions of users.")

# Sidebar for filtering
st.sidebar.title("Filters")
st.sidebar.write("Select the type of contributions to display.")

# Filter options
contribution_types = ["New Resource", "Modified Resource", "Review"]
selected_types = st.sidebar.multiselect(
    "Contribution Types",
    options=contribution_types,
    default=contribution_types,
    help="Choose the types of contributions you want to display."
)

# Slider for number of contributions
num_contributions = st.sidebar.slider("Number of contributions", 1, 50, 10, help="Select the number of contributions to display")
st.write("")

try:
    # Read the last contributions from the database
    conn = pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )
    query = f"""
            SELECT 
                    Users.Username, Contributions.ContributionType, Contributions.ContributionDate AS [DateOfContribution], 
                    Resources.Title, Resources.Authors, Resources.Date, Reviews.Rating AS ReviewRating, Reviews.Review AS Review
            FROM ((Users 
            INNER JOIN Contributions ON Users.UserID = Contributions.UserID) 
            INNER JOIN Resources ON Contributions.ResourceID = Resources.ResourceID)
            LEFT JOIN Reviews ON Contributions.ContributionID = Reviews.ContributionID  
            ORDER BY Contributions.ContributionDate DESC;
            """
    contributions = pd.read_sql(query, conn)
    conn.close()

    # Map contribution types to the new categories
    contributions["ContributionType"] = contributions["ContributionType"].replace({
        "Edit Resource": "Modified Resource",
        "Add Review": "Review",
        "Edit Review": "Review"
    })

    # Filter data based on selected contribution types
    if selected_types:
        contributions = contributions[contributions["ContributionType"].isin(selected_types)]

    if num_contributions:
        contributions = contributions.head(num_contributions)

except Exception as e:
    st.error(f"Unable to connect to the database: {e}")

# Display filtered contributions
for _, contribution in contributions.iterrows():
    if contribution["ContributionType"] == "New Resource":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 5px;">
                &#127381;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution['DateOfContribution'].strftime('%d %b %Y')}</strong> &#183; {contribution['Username']} added a new resource
            </p>
            <h5 style="text-align: center; margin: 0;">{contribution['Title']}</h5>
            <p style="text-align: center; margin: 0px;"><i>By {contribution['Authors']} ({contribution['Date']})</p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)

    elif contribution["ContributionType"] == "Modified Resource":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 5px;">
                &#128221;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution['DateOfContribution'].strftime('%d %b %Y')}</strong> &#183; {contribution['Username']} edited details of
            </p>
            <h5 style="text-align: center; margin: 0;">{contribution['Title']}</h5>
            <p style="text-align: center; margin: 0;"><i>By {contribution['Authors']} ({contribution['Date']})</p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)

    elif contribution["ContributionType"] == "Review":
        st.markdown(f"""
        <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
            <p style="margin: 5px;">
                &#128161;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>{contribution['DateOfContribution'].strftime('%d %b %Y')}</strong> &#183; {contribution['Username']} added or edited a review for
            </p>
            <h5 style="text-align: center; margin: 0;">{contribution['Title']}</h5>
            <p style="text-align: center; margin: 0px;"><i>By {contribution['Authors']} ({contribution['Date']})</p>
            <p style="margin: 0; text-align: center;">{print_stars(contribution['ReviewRating'])}</p>
            <p style="margin: 0;">&laquo; {contribution['Review']} &raquo;</p>
        </div>
        <p style="margin: 0;">&nbsp;</p>
        """, unsafe_allow_html=True)
