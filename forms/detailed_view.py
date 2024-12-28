import streamlit as st
import pandas as pd
import pyodbc
import numpy as np
from datetime import datetime

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

            if articles['Reader'].values[0] == None:
                readers_names = "No readers recorded"
            else:
                readers_login = articles['Reader'].values[0].split(", ")
                readers_names = ""

                for login in readers_login:
                    reader_query = f"SELECT [Username] FROM [Users] WHERE [UserLogin] = '{login}';"
                    try:
                        reader_name = pd.read_sql(reader_query, conn)["Username"].iloc[0]
                        readers_names = readers_names + str(reader_name) + ", "
                    except:
                        error = 0
                    
                readers_names = readers_names[:-2]
            
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
            st.write(f"{readers_names}")

            st.subheader("Comments")
            if comments.empty:
                    st.info("No comments available.")
            else:
                for i in range(comments.shape[0]):
                    st.write(f"**{comments.loc[i,'Username']}** - {np.datetime64(comments.loc[i,'ReviewDate'], 'D').astype('datetime64[D]').astype(datetime).strftime("%d %b %Y")} ({print_stars(comments.loc[i,'Rating'])})")
                    st.write(f"{comments.loc[i,'Review']}")
                    st.write("")


            st.form_submit_button("Close", on_click=st.stop)

        except Exception as e:
            st.error(f"Unable to connect to the database: {e}")