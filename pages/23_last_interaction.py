import streamlit as st
import pandas as pd
import pyodbc
import math
from datetime import datetime

st.title("Last Interactions")
st.write("See here the last interactions with the resources of the database.")

if "dbPathway" in st.session_state:
    num_interactions = st.slider("Number of interactions", 1, 100, 1, help="Select the number of interactions to display")


    try:
        # Connection string for Access database
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        st.write(f"**{num_interactions} Most Recent Reviews:**")

        # Query to join Reviews and Resources and get the 10 most recent reviews
        query = f"""
        SELECT TOP {num_interactions} 
            FORMAT(Reviews.ReviewDate, 'YYYY-MM-DD') AS [Date], Reviews.Review, Reviews.Rating, Users.Username, Resources.Title, Resources.Authors 
            FROM (Reviews INNER JOIN Users ON Reviews.UserLogin = Users.UserLogin) 
            INNER JOIN Resources ON Reviews.ResourceID = Resources.ResourceID  
            ORDER BY ReviewDate DESC;
        """

        # Execute the query and load the results into a DataFrame
        recent_reviews = pd.read_sql(query, conn)

        conn.close()

        # Display the results in a table
        for index, row in recent_reviews.iterrows():
            st.subheader(f"**{row['Title']}**")
            st.write(f"**Authors:** {row['Authors']}")
            # Handle formatting of the Date column
            if isinstance(row['Date'], pd.Timestamp):
                formatted_date = row['Date'].strftime("%d %b. %Y")
            else:
                formatted_date = datetime.strptime(row['Date'], "%Y-%m-%d").strftime("%d %b. %Y")
            st.write(f"**{row['Username']}** - {formatted_date} ({"⭐️" * int(row['Rating'])})")
            st.write(f"{row['Review']}")
            st.markdown("---")

    except Exception as e:
        st.error(f"Unable to connect to the database: {e}")

else:
    st.info("Unable to connect to the database.")