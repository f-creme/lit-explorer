import streamlit as st
import pandas as pd
import pyodbc


@st.dialog("Modify Profile")
def modify_profile_dialog():
    with st.form("modify_profile"):

        try:
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )
            query = f"SELECT * FROM Users WHERE UserLogin='{st.session_state.userLogin}';"
            user_data = pd.read_sql(query, conn)
            conn.close()
        except Exception as e:
            st.error(f":x: Error fetching user data: {e}")
            st.stop()

        user_name = st.text_input("Username", value=user_data['Username'].values[0], help="Enter your username", placeholder="Enter your username")
        user_role = st.text_input("Role", value=user_data['UserRole'].values[0], help="Enter your role", placeholder="Enter your role")
        user_mail = st.text_input("Email", value=user_data['UserMail'].values[0], help="Enter your email", placeholder="Enter your email")
        user_desc = st.text_area("Description", value=user_data['UserDesc'].values[0], help="Enter your description", placeholder="Enter your description")       
        user_pic = st.text_input("Profile Picture URL", value=user_data['UserPicURL'].values[0], help="Enter the URL of your profile picture", placeholder="Enter the URL of your profile picture")
        submit_button = st.form_submit_button("Submit", type="primary", help="Click to submit the changes")

        if submit_button:
            try:
                conn = pyodbc.connect(
                    f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
                )
                query = f"UPDATE Users SET UserDesc='{user_desc}', UserRole='{user_role}', UserMail='{user_mail}', UserPicURL='{user_pic}' WHERE UserID={st.session_state.userID};"
                conn.execute(query)
                conn.commit()
                conn.close()
                st.success(":white_check_mark: Profile updated successfully")
            except Exception as e:
                st.error(f":x: Error updating profile: {e}")
                st.stop()