from datetime import date
import streamlit as st
import pandas as pd
import pyodbc
import toml

# Load the configuration file
with open ("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.user = data["user"]

# Success of the Registration
@st.dialog("Registration Success")
def success_dialog(login, username):
    st.write("User registered successfully. Please note your login details:")
    st.write("**Username**: ", username)
    st.write("**Login**: ", login)

# Login Section
st.header("Login Page")
st.write("If you are already a user, please login here with your login.")

col1, col2 = st.columns(2)
with col1:
    st.session_state.userLogin = st.text_input("Login", value=st.session_state.user["userLogin"], label_visibility="collapsed", help="Enter your login", placeholder="Enter your login")
with col2:
    st.session_state.userName = st.text_input("Username", value=st.session_state.user["userName"], label_visibility="collapsed", help="Enter your username", placeholder="Enter your username")
log_button = st.button("Login", use_container_width=True, type="primary", help="Click to login")

if log_button:
    try:
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )

        query = "SELECT UserLogin, Username, UserRole, UserMail FROM Users;"
        users = pd.read_sql(query, conn)
        query = f"SELECT UserID FROM Users WHERE UserLogin = '{st.session_state.userLogin}';"
        cursor = conn.cursor()
        cursor.execute(query)
        user_id = cursor.fetchall()[0][0]

        if st.session_state.userLogin in users["UserLogin"].values:
            user = users[users["UserLogin"] == st.session_state.userLogin].iloc[0]
            st.session_state.userName = user["Username"]
            st.session_state.userRole = user["UserRole"]
            st.session_state.userMail = user["UserMail"]
            st.session_state.userID = user_id

            with open("config.toml", "w") as f:
                data["user"]["userName"] = st.session_state.userName
                data["user"]["userLogin"] = st.session_state.userLogin
                data["user"]["userRole"] = st.session_state.userRole
                data["user"]["userMail"] = st.session_state.userMail
                data["user"]["userID"] = st.session_state.userID

                toml.dump(data, f)

            st.success("✅ User logged in successfully")
        else:
            st.error("❌ User not found. Please register as a new user.")

        conn.close()
    except Exception as e:
        st.error(f"❌ Error logging in: {e}")
        st.stop()

st.markdown("---")

# New User section
st.header("New User")
st.write("If you are a new user, please register here.")

col3, col4 = st.columns(2)
with col3:
    name = st.text_input("Name*", help="Enter your name", placeholder="Enter your name")
with col4:
    role = st.text_input("Role*", help="Describe your role shortly", placeholder="Enter your role")
mail = st.text_input("Email*", help="Enter your email", placeholder="Enter your email")
description = st.text_area("Description", help="Describe yourself")
picture = st.text_input("Picture URL", help="Enter the URL of your picture")
st.write("*Fields marked with an asterisk are mandatory*")

register_button = st.button("Register", use_container_width=True, type="primary", help="Click to register")

if register_button:
    registration_date = date.today().strftime("%Y-%m-%d")
    if picture == "":
        picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        
    try:
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )

        query = "SELECT UserLogin FROM Users;"
        users = pd.read_sql(query, conn)

        parts = name.strip().split()
        if len(parts) >= 2:
            first_name, last_name = parts[0], parts[-1]
            login = f"{first_name[0].lower()}{last_name.lower()}"
        else:
            login = parts[0].lower()

        number = 1
        base_login = login
        while login in users["UserLogin"].values and number < 100:
            login = f"{base_login}{number}"
            number += 1

        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO Users (Username, UserLogin, UserRole, UserMail, UserDesc, UserRegDate, UserPicURL) VALUES ('{name}', '{login}', '{role}', '{mail}', '{description}', '{registration_date}', '{picture}');"
        )
        conn.commit()

        query = f"SELECT UserID FROM Users WHERE UserLogin = '{login}';"
        cursor.execute(query)
        user_id = cursor.fetchall()[0][0]

        with open("config.toml", "w") as f:
            data["user"]["userName"] = name
            data["user"]["userLogin"] = login
            data["user"]["userRole"] = role
            data["user"]["userMail"] = mail
            data["user"]["userID"] = user_id

            st.session_state.userName = data["user"]["userName"]
            st.session_state.userLogin = data["user"]["userLogin"]
            st.session_state.userRole = data["user"]["userRole"]
            st.session_state.userMail = data["user"]["userMail"]
            st.session_state.userID = data["user"]["userID"]

            toml.dump(data, f)

        conn.close()
        success_dialog(login, name)

    except Exception as e:
        st.error(f"❌ Error registering user: {e}")
        st.stop()
    