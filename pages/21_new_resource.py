import streamlit as st
import pandas as pd
import pyodbc

st.title("Add a new resource")
st.header(f"📂 Library about  Nitrosamines :")

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

if submit:
    try:
        # Connection string for Access database
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        cursor = conn.cursor()

        # Insert into the Resources table using parameters
        insert_query = """
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

        cursor.execute(insert_query, params)
        conn.commit()
        conn.close()

        st.sidebar.success("Resource added successfully.")
    
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")