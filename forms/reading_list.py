import streamlit as st
import pyodbc
import pandas as pd
from datetime import datetime

@st.dialog("Add to Reading List", width="large")
def add_to_reading_list(resource_id):

    with st.form("add_to_reading_list"):

        st.title("Add to Reading List")
        st.write("Add this resource to your reading list.")

        dict_status = {"Not Started": 1, "In Progress": 2, "Read": 0}
        dict_priority = {"Low": 3, "Medium": 2, "High": 1}

        try:
            # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )

            # Verify if the resource is already in the reading list
            query = f"SELECT * FROM ReadingList WHERE ResourceID = {resource_id} AND UserID = {st.session_state.userID};"
            rl = pd.read_sql(query, conn)

            if rl.empty:
                
                status = st.segmented_control("Select a status", ["Not Started", "In Progress", "Read"])
                priority = st.select_slider("Select a priority", options=["Low", "Medium", "High"])

                if st.form_submit_button("Add to Reading List", use_container_width=True, type="primary"):
                    query = f"INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded) VALUES (?, ?, ?, ?, ?);"
                    param = (resource_id, st.session_state.userID, dict_status[status], dict_priority[priority], datetime.now())
                    cursor = conn.cursor()
                    cursor.execute(query, param)
                    conn.commit()
                    conn.close()
                    st.success("Resource added to your reading list.")

            elif rl['Status'][0] == dict_status["Read"]:
                st.info("This resource is already marked as read. You can't update it.")

            else:
                st.warning("This resource is already part of your reading list. Do you want to update it?")
                st.info(f"Status is currently set to {next(key for key, value in dict_status.items() if value == rl['Status'][0])}.")
                st.info(f"Priority is currently set to {next(key for key, value in dict_priority.items() if value == rl['Priority'][0])}.")

                status = st.segmented_control("Select a status", ["Not Started", "In Progress", "Read"])
                priority = st.select_slider("Select a priority", options=["Low", "Medium", "High"])

                if st.form_submit_button("Update Reading List", use_container_width=True, type="primary"):
                    query = f"UPDATE ReadingList SET Status = ?, Priority = ? WHERE ResourceID = {resource_id} AND UserID = {st.session_state.userID};"
                    param = (dict_status[status], dict_priority[priority])
                    cursor = conn.cursor()
                    cursor.execute(query, param)
                    conn.commit()
                    conn.close()
                    st.success("Resource updated in your reading list.")

            
        except Exception as e:
            st.error(f"Error: {e}")

        st.form_submit_button(" ", type="tertiary")