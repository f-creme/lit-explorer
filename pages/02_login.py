"""
Login and Registration Page for LitExplorer

This page allows users to log in or register to access LitExplorer. 
It supports user authentication and stores session information in a configuration file.

Features:
- User login with validation and session management.
- New user registration with dynamic username generation.
- Persistent user data stored in a TOML configuration file.
- Secure connection to a Microsoft Access database with query parameterization.

Dependencies:
- Streamlit for user interface.
- pandas and pyodbc for database interaction.
- toml for configuration management.
"""

from datetime import datetime
import streamlit as st
import pandas as pd
import pyodbc
import toml

# Generate the login based on the user's name
def generate_login(name, existing_users):
    """
    This function generates a unique login for a new user based on their name.
    It appends a number if the login already exists in the database.

    Parameters:
    - name (str): The name of the user.
    - existing_users (list): The DataFrame containing existing users.

    Returns:
    - login (str): The generated login.
    """
    
    parts = name.strip().split()
    if len(parts) >= 2:
        first_name, last_name = parts[0], parts[-1]
        login = f"{first_name[0].lower()}{last_name.lower()}"
    else:
        login = parts[0].lower()
    
    count = 1
    base_login = login
    while login in existing_users and count < 100:
        login = f"{base_login}{count}"
        count += 1
    
    return login

# Load the configuration file
with open ("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.userLogin = data["user"]["userLogin"]
    st.session_state.userName = data["user"]["userName"]

# Dialog for registration success
@st.dialog("Registration Success")
def success_dialog(login, username):
    st.success(f"✅ User '{username}' registered successfully.")
    st.write("Please note your login details:")
    st.write("**Username**: ", username)
    st.write("**Login**: ", login)

# Dialog for debug information
@st.dialog("Debug Information")
def debug_dialog(message):
    st.write("Debug information:")
    st.write(message)

# Login Section
st.header("Login Page")
st.write("If you are already a user, please login here with your login.")

col1, col2 = st.columns(2)

with col1:
    user_login = st.text_input("Login", value=st.session_state.userLogin, label_visibility="collapsed", help="Enter your login", placeholder="Enter your login")
with col2:
    user_name = st.text_input("Username", value=st.session_state.userName, label_visibility="collapsed", help="Enter your username", placeholder="Enter your username")

log_button = st.button("Login", use_container_width=True, type="primary", help="Click to login")

if log_button:
    
    if not user_login.strip():
        st.error("❌ Login cannot be empty.")
    else:
        try:
            # Connection string for the database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )
            query = "SELECT UserID, Username, UserRole, UserMail FROM Users WHERE UserLogin = ?;"
            user_data = pd.read_sql(query, conn, params=[user_login])

            if not user_data.empty:
                user = user_data.iloc[0]
                st.session_state.update({
                    "userLogin": user_login,
                    "userName": user["Username"],
                    "userRole": user["UserRole"],
                    "userMail": user["UserMail"],
                    "userID": int(user["UserID"])
                })

                
                # Save to config file
                with open("config.toml", "w") as f:
                    for item in data["user"]:
                        data["user"][item] = st.session_state[item]                    
                    toml.dump(data, f)

                st.success("✅ Login successful!")

            else:
                st.error("❌ User not found. Please register as a new user.")

        except Exception as e:
            st.error(f"❌ Error during login:\n{e}")

st.markdown("---")

# Registration
st.header("New User")
st.write("If you're new, register below.")

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
    if not name.strip() or not role.strip() or not mail.strip():
        st.error("❌ All mandatory fields must be filled.")
    
    else:  
        try:
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )

            # Verify if the user already exists
            query = "SELECT UserLogin, UserMail FROM Users;"
            users = pd.read_sql(query, conn)

            if mail in users["UserMail"].values:
                st.error("❌ User with this email already exists.")
                st.stop()
                

            else:
                # Generate a login
                login = generate_login(name, users["UserLogin"].tolist())
                
                # Default picture if not provided
                if not picture:
                    picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

                cursor = conn.cursor()
                cursor.execute(f"""
                        INSERT INTO Users (Username, UserLogin, UserRole, UserMail, UserDesc, UserRegDate, UserPicURL) 
                        VALUES (?, ?, ?, ?, ?, ?, ?);""", 
                        (name, login, role, mail, description, datetime.now(), picture))
                conn.commit()

                cursor.execute(f"SELECT UserID FROM Users WHERE UserLogin = '{login}';")
                user_id = cursor.fetchall()[0][0]

                # Update session state
                st.session_state.update({
                    "userLogin": login,
                    "userName": name,
                    "userRole": role,
                    "userMail": mail,
                    "userID": user_id
                })

                # Save to config file
                with open("config.toml", "w") as f:
                    for item in data["user"]:
                        data["user"][item] = st.session_state[item]                    
                    toml.dump(data, f)

                success_dialog(login, name)

        except Exception as e:
            st.error(f"❌ Error registering user: {e}")
            st.stop()

        finally:
            if 'conn' in locals() and conn:
                conn.close()