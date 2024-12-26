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
    **LitExplorer** is your go-to application for exploring, organizing, and incteracting 
    with scientific literature on nitrosamines. Designed with researchers, industry professionals 
    and students in mind, this platfrom fosters collaboration and simplifies access 
    to information on nitrosamines.

    Throuhg intuitives features like advanced searches, user reviews, and resource 
    management, **LitExplorer** empowers you to stay up-to-date with the latest 
    insights on nitrosamines.
    """
)

st.markdown("---")

st.markdown(
    """
    ### How to get started :rocket:

    1. **Install the application**: Follow the instructions in our Installation Guide.
    2. **Configure the database**: Head over to the **Database Configuration** page to link your local 
    or cloud-hosted Access file.
    3. **Dive into your library**: Explore the database, interact with resources, and contribute 
    to the knowledge base.
    """
)

st.markdown("---")

st.markdown(
    """
    ### About LitExplorer :books:

    LitExplorer was developed by students from **ECPM Strasbourg** in collaboration with **Novartis**, 
    adressing a critical challenge in the pharmaceutical industry. This tool supports 
    dynamic literature review processes, emphasizing both ease of access and 
    community-driven insights.
    """
)    

st.markdown("---")

st.markdown(
    """
    ### Tutorials :movie_camera:
    
    Below, you'll find video tutorials to guide you through essentiel steps:
    * Installing LitExplorer
    * Configuring the database
    * Your First Use

    *(Tutorial videos coming soon)*
    """
)

st.markdown("---")

st.markdown(
    """
    ### Contact Us :mailbox:
    
    Have questions, suggestions, or feedback? Feel free to reach out!
    
    * **Team Project** : Axel Delente, Sara Sanchez, Florentin Creme supervised by **[ECPM Strasbourg](https://ecpm.unistra.fr)** and **Novartis**
    * **Developer** : Florentin Creme
        * **Email**: creme.florentin@gmail.com
        * **GitHub**: [f-creme](https://github.com/f-creme)"""
)