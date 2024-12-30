import streamlit as st
import pandas as pd
import pyodbc

st.title('My Readings')
dict_status = {"Not Started": 1, "In Progress": 2, "Read": 3}
dict_priority = {"Low": 1, "Medium": 2, "High": 3}

# Connect to the database
try:
    conn=pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )

    query = f"""SELECT 
            ReadingList.ResourceID, ReadingList.Status, ReadingList.Priority 
            FROM ReadingList 
            WHERE UserID = {st.session_state.userID};
            """
    readings = pd.read_sql(query, conn)

    readings['LiteralStatus'] = readings['Status'].map({v: k for k, v in dict_status.items()})
    readings['LiteralPriority'] = readings['Priority'].map({v: k for k, v in dict_priority.items()})
    st.write(readings)

except Exception as e:
    st.error(f":x: An error as occured :\n{e}")
    st.stop()