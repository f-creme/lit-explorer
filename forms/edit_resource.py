import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

@st.dialog("Edit Resource", width="large")
def edit_resource(resource_id):
    with st.form("Edit Resource"):
        try:
            # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )
            cursor = conn.cursor()

            # Load the Resources table
            articles_query = f"SELECT * FROM Resources WHERE ResourceID = {resource_id};"
            articles = pd.read_sql(articles_query, conn)
            
            # Edit form
            title = st.text_input("Title", value=articles.loc[0, 'Title'])
            authors = st.text_input("Authors", value=articles.loc[0, 'Authors'])
            journal = st.text_input("Journal", value=articles.loc[0, 'Journal'])
            date = st.text_input("Date", value=articles.loc[0, 'Date'])
            doi = st.text_input("DOI", value=articles.loc[0, 'DOI'])
            document_type = st.text_input("Document Type", value=articles.loc[0, 'Document Type'])
            article_type = st.text_input("Article Type", value=articles.loc[0, 'Article type'])
            application_field = st.text_input("Application Field", value=articles.loc[0, 'Application Field'])
            category = st.text_input("Category", value=articles.loc[0, 'Category'])
            sub_category = st.text_area("Sub Category", value=articles.loc[0, 'Sub Category'])
            specific_to_nitrosamines = st.text_input("Specific to Nitrosamines", value=articles.loc[0, 'Specific to Nitrosamines'])
            keywords = st.text_area("Keywords", value=articles.loc[0, 'Keywords'])
            summary = st.text_area("Summary", value=articles.loc[0, 'Summary'])
            

            submit = st.form_submit_button("Save Changes")
            if submit:
                # Update the Resources table using parameters
                update_query = """
                UPDATE Resources
                SET [Title] = ?,
                    [Authors] = ?,
                    [Journal] = ?,
                    [Date] = ?,
                    [DOI] = ?,
                    [Document Type] = ?,
                    [Article type] = ?,
                    [Application Field] = ?,
                    [Category] = ?,
                    [Sub Category] = ?,
                    [Specific to Nitrosamines] = ?,
                    [Keywords] = ?,
                    [Summary] = ? 
                WHERE ResourceID = ?;
                """
                params = (
                    title, authors, journal, date, doi,
                    document_type, article_type, application_field,
                    category, sub_category, specific_to_nitrosamines,
                    keywords, summary, resource_id
                )
                cursor.execute(update_query, params)
                

                try:
                    # Add the contribution to the Contributions table
                    query = "INSERT INTO Contributions (ResourceID, UserID, ContributionType, ContributionDate) VALUES (?, ?, ?, ?);"
                    params = (resource_id, st.session_state.userID, "Edit Resource", datetime.now())
                    cursor.execute(query, params)

                    conn.commit()
                    # Display success message
                    st.success(f"Resource '{title}' updated successfully.")

                    # Update the number of contributions in the Users table
                    query = f"UPDATE Users SET UserContributions = UserContributions + 1 WHERE UserID = {st.session_state.userID}   "
                    cursor.execute(query)
                    conn.commit()

                except Exception as e:
                    st.error(f"An error as occured when saving the contribution: {e}")

        except Exception as e:
            st.error(f"An error as occured when saving the modifications: {e}")

        finally:
            conn.close()
