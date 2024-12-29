import streamlit as st
import pyodbc
from datetime import datetime

# Page title
st.title("Add a new resource")
st.header(f"📂 Library about  Nitrosamines :")

# Input fields
title = st.text_input("Title", help="Enter the title of the resource")
authors = st.text_input("Authors", help="Enter the authors of the resource")
col1, col2 = st.columns(2)
with col1:
    journal = st.text_input("Journal")
    doi = st.text_input("DOI")
    article_type = st.text_input("Article Type")
    category = st.text_input("Category")
    
with col2:
    date = st.text_input("Date", help="Enter the year of publication (YYYY)")
    document_type = st.text_input("Document Type")
    application_field = st.text_input("Application Field")
    specific_to_nitrosamines = st.selectbox("Is the resource specific to nitrosamines ?", ["Yes", "No"])
sub_category = st.text_area("Sub Category", help="""Enter the sub-categories separated by ", " (comma + space)""")
keywords = st.text_area("Keywords", help="""Enter the keywords separated by ", " (comma + space)""")
summary = st.text_area("Summary")
st.write("")

# User information
st.write("*The fields below are private and will not be displayed in the library.*")
col3, col4 = st.columns(2)
with col3:
    status = st.segmented_control("Reading status", ["Not Started", "In Progress", "Read"], key="status")
with col4:
    priority = st.select_slider("Priority level", options=["Low", "Medium", "High"], key="priority")



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
        ([Title], [Authors], [Journal], [Date], [DOI], [Document Type], [Article type], [Application Field], [Category], [Sub Category], [Specific to Nitrosamines], [Keywords], [Summary])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            title, authors, journal, date, doi,
            document_type, article_type, application_field,
            category, sub_category, specific_to_nitrosamines,
            keywords, summary
        )

        cursor.execute(query, params)
        conn.commit()

        # Insert into the ReadingList table
        query = f"SELECT ResourceID FROM Resources WHERE Title = '{title}' AND [Date] = {date}"
        resource_id = cursor.execute(query).fetchone()[0]

        dict_status = {"Not Started": 1, "In Progress": 2, "Read": 0}
        dict_priority = {"Low": 3, "Medium": 2, "High": 1}

        if dict_status[status] == 0:
            query = "INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded, DateRead) VALUES (?, ?, ?, ?, ?, ?)"
            params = (resource_id, st.session_state.userID, dict_status[status], 0, datetime.now(), datetime.now())

        else:
            query = f"""INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded) VALUES (?, ?, ?, ?, ?)"""
            params = (resource_id, st.session_state.userID, dict_status[status], dict_priority[priority], datetime.now())

        cursor.execute(query, params)
        conn.commit()

        # Update the number of contributions in the Users table
        query = f"UPDATE Users SET UserContributions = UserContributions + 1 WHERE UserLogin = '{st.session_state.userLogin}'"
        cursor.execute(query)
        conn.commit()

        try:
            # Insert into list of contributions
            query = "INSERT INTO Contributions (ResourceID, ContributionType, UserLogin, ContributionDate) VALUES (?, ?, ?, ?)"
            params = (resource_id, "New Resource", st.session_state.userLogin, datetime.now())
            cursor.execute(query, params)

            conn.commit()
            conn.close()

            # Success message
            st.sidebar.success("Resource added successfully.")
        
        except Exception as e:
            st.sidebar.error(f"An error occurred when adding the collaboration:\n {e}")
    
    except Exception as e:
        st.sidebar.error(f"An error occurred when adding the resource to the database:\n {e}")