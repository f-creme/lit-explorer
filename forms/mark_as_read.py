import streamlit as st
import pandas as pd
import pyodbc

@st.dialog("Mark as Read", width="large")
def mark_as_read(resource_id, resource_title):
    with st.form("mark_as_read"):
        
        try:
        # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
            
            query = f"SELECT Reader FROM Resources WHERE ResourceID = {resource_id};"
            reader = str(pd.read_sql(query, conn).iloc[0, 0])

            if st.session_state.userLogin in reader:
                st.warning(f"Resource '{resource_title}' has already been marked as read by {st.session_state.userName} ({st.session_state.userLogin}).")

            else:
                if reader == None:
                    new_reader = st.session_state.userLogin
                
                else:
                    new_reader = reader + ", " + st.session_state.userLogin

                cursor = conn.cursor()

                # Update the Reader column in the Resources table
                st.write(new_reader)
                update_query = f"""
                UPDATE Resources
                SET Reader = '{new_reader}'
                WHERE ResourceID = {resource_id};
                """
                st.write(update_query)
                cursor.execute(update_query)
                conn.commit()
                st.success(f"Resource '{resource_title}' marked as read by {st.session_state.userName}.")

        except Exception as e:
            st.error(f"Error: {e}")

        st.form_submit_button("Close")