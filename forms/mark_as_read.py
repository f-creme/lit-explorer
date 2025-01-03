import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

@st.dialog("Mark as Read", width="large")
def mark_as_read(resource_id, resource_title):

    dict_status = {"Not Started": 1, "In Progress": 2, "Read": 3}
    dict_priority = {"Low": 1, "Medium": 2, "High": 3}

    with st.form("mark_as_read"):
        try:
        # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
            
            # Verify if the resource is already marked as read
            query = f"SELECT Status FROM ReadingList WHERE ResourceID = {resource_id} AND UserID = {st.session_state.userID};"
            status = pd.read_sql(query, conn)

            if status.empty:
                query = f"INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded, DateRead) VALUES (?, ?, ?, ?, ?, ?);"
                param = (resource_id, st.session_state.userID, dict_status["Read"], 0, datetime.now(), datetime.now())
                cursor = conn.cursor()
                cursor.execute(query, param)
                conn.commit()
                conn.close()
                st.success(f"{resource_title} has been marked as read.")

            else:
                if status['Status'][0] == dict_status["Read"]:
                    st.info(f"{resource_title} is already marked as read.")
                else:
                    query = f"UPDATE ReadingList SET Status = ?, Priority = ?, DateRead = ? WHERE ResourceID = {resource_id} AND UserID = {st.session_state.userID};"
                    param = (dict_status['Read'], 0, datetime.now())
                    cursor = conn.cursor()
                    cursor.execute(query, param)
                    conn.commit()
                    conn.close()
                    st.success(f"{resource_title} has been marked as read.")
            

        except Exception as e:
            st.error(f"Error: {e}")

        st.form_submit_button("Close")