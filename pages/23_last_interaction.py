import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

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
            Reviews.ReviewDate, Reviews.Review, Reviews.Rating, Users.Username, Resources.Title, Resources.Authors 
            FROM (Reviews INNER JOIN Users ON Reviews.UserID = Users.UserID) 
            INNER JOIN Resources ON Reviews.ResourceID = Resources.ResourceID  
            ORDER BY ReviewDate DESC;
        """

        # Execute the query and load the results into a DataFrame
        recent_reviews = pd.read_sql(query, conn)

        conn.close()

        # Display the results in a table
        for index, row in recent_reviews.iterrows():

            if isinstance(row['ReviewDate'], pd.Timestamp):
                formatted_date = row['ReviewDate'].strftime("%d %b. %Y")
            else:
                formatted_date = datetime.strptime(row['ReviewDate'], "%Y-%m-%d").strftime("%d %b. %Y")

            st.markdown(f"""
            <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
                <h4 style="margin: 0;">{row['Title']}</h1>
                <p><i>By {row['Authors']}</i></p>
                <p style="margin: 0;"><strong>{row['Username']}</strong> - {formatted_date} ({"⭐️" * int(row['Rating'])}{"✰" * (5 - int(row['Rating']))})</p>
                <p style="margin: 0;">&laquo; {row['Review']}  &raquo;</p>
            </div>
            <p style="margin: 10;">&nbsp;</p>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Unable to connect to the database: {e}")

else:
    st.info("Unable to connect to the database.")