"""
LitExplorer: Interactive Database for Scientific Literature

Home page of LitExplorer, a Streamlit application designed for efficient exploration, organization, 
and interaction with a database focused on nitrosamines. This platform was developed collaboratively 
by ECPM Strasbourg students and Novartis to address a critical need in the pharmaceutical industry.

Features showcased on this page:
- Welcome message introducing the application and its purpose.
- Overview of how to set up and navigate the app.
- Resources for tutorials and contact information for support.
- Highlights of recent updates, including:
  * User collaboration tools: ratings, comments, and reviews.
  * Advanced search and resource filtering.
  * Dynamic database synchronization.
"""

import streamlit as st
import toml 

st.set_page_config(page_title="Home Page")

# Initialisation
with open("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.dbPathway = data["project"]["dbPathway"]

st.title("Welcome to **LitExplorer** :wave:")

st.markdown(
    """
    **LitExplorer** is your go-to application for exploring, organizing, and interacting 
    with scientific literature on nitrosamines. Designed with researchers, industry professionals, 
    and students in mind, this platform fosters collaboration and simplifies access 
    to critical information.
    
    Through features like advanced searches, user reviews, dynamic synchronization, 
    and resource management, **LitExplorer** empowers you to stay updated and contribute 
    to the knowledge base on nitrosamines.
    """
)

st.markdown("---")

st.markdown(
    """
    ### How to Get Started :rocket:

    1. **Install the Application**: Follow the steps in the [Installation Guide](https://github.com/f-creme/lit-explorer/blob/main/readme.md).
    2. **Configure the Database**: Use the **Database Configuration** page to link your local 
    or cloud-hosted Access file.
    3. **Collaborate**: Add reviews, interact with resources, and contribute to building 
    a dynamic knowledge hub.
    """
)

st.markdown("---")

st.markdown(
    """
    ### About LitExplorer :books:

    LitExplorer was developed by students from **ECPM Strasbourg** in collaboration with **Novartis**, 
    addressing a critical challenge in the pharmaceutical industry. This tool supports 
    a dynamic literature review process, emphasizing ease of access and user-driven insights.

    **Recent Updates**:
    - Enhanced user profile management.
    - Improved review and comment system.
    - Advanced filtering and sorting options.
    """
)    

st.markdown("---")

st.markdown(
    """
    ### Tutorials :movie_camera:
    
    Below, you'll find video tutorials to guide you through essential steps:
    - Installing LitExplorer
    - Configuring the database
    - Advanced search features
    - Collaborative resource management

    *(Tutorial videos coming soon)*
    """
)

st.markdown("---")

st.markdown(
    """
    ### Contact Us :mailbox:
    
    Have questions, suggestions, or feedback? Reach out to us!
    
    - **Team Project**: Axel Delente, Sara Sanchez, Florentin Creme
    - **Developer**: Florentin Creme
        - **Email**: creme.florentin@gmail.com
        - **GitHub**: [f-creme](https://github.com/f-creme)
    """
)
