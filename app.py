import streamlit as st
import toml

with open("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.dbPathway = data["project"]["dbPathway"]
    st.session_state.userName = data["user"]["userName"]
    st.session_state.userLogin = data["user"]["userLogin"]
    st.session_state.userRole = data["user"]["userRole"]
    st.session_state.userMail = data["user"]["userMail"]
    st.session_state.userID = data["user"]["userID"]

# General Section : Home Page and Login Page
homepage_page = st.Page(
    page="pages/00_homepage.py",
    title="Home Page",
    icon=":material/house:",
    default=True
)

database_page = st.Page(
    page="pages/01_database.py",
    title="Database Configuration",
    icon=":material/database:",
)

login_page = st.Page(
    page="pages/02_login.py",
    title="Login",
    icon=":material/login:",
)

# Profile Section : Profile Page
profile_page = st.Page(
    page="pages/10_profile.py",
    title="Profile",
    icon=":material/account_circle:",
)

last_interaction_page = st.Page(
    page="pages/23_last_interaction.py",
    title="Last Reviews",
    icon=":material/chat:",
)


library_page = st.Page(
    page="pages/20_library.py",
    title="Library",
    icon=":material/book_5:",
)

new_resource_page = st.Page(
    page="pages/21_new_resource.py",
    title="New Resource",
    icon=":material/note_add:",
)

last_contributions_page = st.Page(
    page="pages/24_last_contributions.py",
    title="Last Contributions",
    icon=":material/work_history:",
)

contributors_page = st.Page(
    page="pages/25_contributors.py",
    title="Contributors",
    icon=":material/people:",
)

readings_page = st.Page(
    page="pages/11_readings.py",
    title="My Readings",
    icon=":material/menu_book:",
)

# test = st.Page(
#     page="pages/test.py",
#     title="Test",
#     icon=":material/bug_report:",
# )

pg = st.navigation(
    {   
        "": [homepage_page, database_page, login_page],
        "Profile": [profile_page, readings_page, contributors_page], 
        "Project": [library_page, new_resource_page, last_contributions_page]
    }
)

pg.run()
