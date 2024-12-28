import streamlit as st
import pandas as pd
import pyodbc

# Page title
st.title("Add a new resource")
st.header(f"📂 Library about  Nitrosamines :")

# Input fields
title = st.text_input("Title")
authors = st.text_input("Authors")
journal = st.text_input("Journal")
date = st.text_input("Date", help="Year of publication (YYYY)")
doi = st.text_input("DOI")
document_type = st.text_input("Document Type")
article_type = st.text_input("Article Type")
application_field = st.text_input("Application Field")
category = st.text_input("Category")
sub_category = st.text_area("Sub Category")
specific_to_nitrosamines = st.text_input("Specific to Nitrosamines")
keywords = st.text_area("Keywords")
summary = st.text_area("Summary")
reader = st.session_state.userLogin

submit = st.button("Save Resource", type="primary", use_container_width=True)

# If the user clicks the "Save Resource" button
if submit:
    try:
        # Connection string for Access database
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        cursor = conn.cursor()

        # Insert into the Resources table using parameters
        query = """
        INSERT INTO Resources
        ([Title], [Authors], [Journal], [Date], [DOI], [Document Type], [Article type], [Application Field], [Category], [Sub Category], [Specific to Nitrosamines], [Keywords], [Summary], [Reader])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            title, authors, journal, date, doi,
            document_type, article_type, application_field,
            category, sub_category, specific_to_nitrosamines,
            keywords, summary, reader
        )

        cursor.execute(query, params)
        conn.commit()

        # Get the ResourceID of the newly added resource
        try:
            query = f"SELECT ResourceID FROM Resources WHERE Title = '{title}' AND [Date] = {date}"
            resource_id = cursor.execute(query).fetchone()[0]
            
            try:
                # Insert into list of contributions
                query = "INSERT INTO Contributions (ResourceID, ContributionType, UserLogin) VALUES (?, ?, ?)"
                params = (resource_id, "New Resource", st.session_state.userLogin)
                cursor.execute(query, params)

                conn.commit()
                conn.close()

                # Success message
                st.sidebar.success("Resource added successfully.")
            
            except Exception as e:
                st.sidebar.error(f"An error occurred when adding the collaboration:\n {e}")
        
        except Exception as e:
            st.sidebar.error(f"An error occurred when retrieving the ResourceID:\n {e}")
    
    except Exception as e:
        st.sidebar.error(f"An error occurred when adding the resource to the database:\n {e}")