import streamlit as st
import pandas as pd
import pyodbc
import numpy as np
from datetime import datetime

from forms.edit_resource import edit_resource

def print_stars(rating):
    if rating == None:
        return "✰✰✰✰✰"
    else:
        return "⭐️" * int(rating) + "✰" * (5 - int(rating))

@st.dialog("Detailed View", width="large")
def show_resources_details(resourceID):
    with st.form("Detailed View"):

        try:
            # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )

            # Load the Articles table
            articles_query = f"SELECT * FROM Resources WHERE ResourceID = {resourceID};"
            articles = pd.read_sql(articles_query, conn)

            # Load Comments
            comments_query = f"""SELECT 
                                    [Reviews].[ReviewID], 
                                    [Reviews].[ResourceID], 
                                    [Reviews].[Rating], 
                                    [Reviews].[ReviewDate], 
                                    [Reviews].[Review], 
                                    [Users].[Username]
                                FROM [Reviews]
                                INNER JOIN [Users] ON [Reviews].[UserLogin] = [Users].[UserLogin] 
                                WHERE [Reviews].[ResourceID] = {resourceID} 
                                ORDER BY [Reviews].[ReviewDate] DESC;
                            """
            comments = pd.read_sql(comments_query, conn)

            # Load Readers
            readers_query = f"""SELECT Username 
                                FROM Users LEFT JOIN ReadingList ON Users.UserID = ReadingList.UserID 
                                WHERE ResourceID = {resourceID} AND Status = 3;"""
            readers = pd.read_sql(readers_query, conn)
            
            conn.close()

            st.header(f"{articles.loc[0,'Title']}")
            st.write(f"{print_stars(articles.loc[0,'Rating'])}")
            st.write(f"**Authors:** {articles.loc[0,'Authors']}")

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Journal:** {articles.loc[0,'Journal']}")
                st.write(f"**DOI:** {articles.loc[0,'DOI']}")
                st.write(f"**Document Type:** {articles.loc[0,'Document Type']}")
                st.write(f"**Category:** {articles.loc[0,'Category']}")
                
            with col2:
                st.write(f"**Date:** {int(articles.loc[0,'Date'])}")
                st.write(f"**Application Field:** {articles.loc[0,'Application Field']}")
                st.write(f"**Specific to Nitrosamines:** {articles.loc[0,'Specific to Nitrosamines']}")
                st.write(f"**Sub Category:** {articles.loc[0,'Sub Category']}")

            st.write(f"**Keywords:** {articles.loc[0,'Keywords']}")

            st.subheader("Summary")
            st.write(f"{articles.loc[0,'Summary']}")

            st.subheader("Readers")
            st.write(f"{', '.join(readers['Username'])}")

            st.subheader("Comments")
            if comments.empty:
                    st.info("No comments available.")
            else:
                for i in range(comments.shape[0]):
                    st.markdown(f"""
                    <div style="background-color: white; padding: 10px; border: 1px solid lightgray; border-radius: 5px;">
                        <p style="margin: 0;">
                            <strong>{comments.loc[i,'Username']}</strong> - {np.datetime64(comments.loc[i,'ReviewDate'], 'D').astype('datetime64[D]').astype(datetime).strftime("%d %b %Y")} ({print_stars(comments.loc[i,'Rating'])})
                        </p>
                        <p style="margin: 0;"> {comments.loc[i,'Review']} </p>
                    </div>
                    <p style="margin: 0;">&nbsp;</p>
                    """, unsafe_allow_html=True)

            st.write("")
            close_button = st.form_submit_button("Close", use_container_width=True, type="primary", on_click=st.stop, help="Click on the cross at top right if the window does not close.")

        except Exception as e:
            st.error(f"Unable to connect to the database: {e}")