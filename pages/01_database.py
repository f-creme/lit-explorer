"""
Database Configuration Page for LitExplorer

This page allows users to configure and connect the LitExplorer application to a Microsoft Access database.
The database can be stored locally, on a network server, or synchronized via SharePoint for collaboration.

Features:
- Clear instructions for downloading and setting up the database.
- Input field for specifying the database pathway.
- Validation of the connection to ensure accessibility.
- Dynamic feedback on the success or failure of the connection.

Dependencies:
- Streamlit for the user interface.
- pandas and pyodbc for database interaction.
- toml for reading and writing configuration files.
"""

import streamlit as st
import pandas as pd
import pyodbc
import toml

# Load database configuration
with open("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.dbPathway = data["project"]["dbPathway"]

st.title("Database Configuration :file_cabinet:")

st.write(
    "To get started with LitExplorer, you need to link the application to an Access database. "
    "Follow the steps below based on your storage preference:"
)

st.markdown("---")

# Step 1: Download the database
st.markdown(
    """
    #### Step 1: Download the Database

    :inbox_tray:[Download the Access database template]() to get a pre-configured file with all the required tables and fields. 
    Alternatively, create your own database by replicating the provided structure.
    """
)

# Step 2: Save the database
st.markdown(
    """
    #### Step 2: Save Your Database

    Depending on your needs, you can store the database:

    - :floppy_disk: **Locally**: Save the file to a directory on your computer.
    - :card_file_box: **On a Local Server**: Store the file in a shared folder on a network server.
    - :globe_with_meridians: **On SharePoint**: 
        1. Create a Microsoft Teams group if one doesn’t exist.
        2. Add the database file to the Files tab under a folder of your choice.
        3. Synchronize the folder using OneDrive for easy access in your file explorer.
        4. *(See detailed video tutorial)*.
    """
)

# Step 3: Connect to the database
st.markdown(
    """
    #### Step 3: Connect to the Database

    Paste the full file path (right-click your database file and select *Copy as Path*) and 
    click **Save** to establish the connection.

    :warning: Make sure there are no quotes around the path.
    """
)

# Input field for the database pathway
st.session_state.dbPathway = st.text_input(
    "Database Pathway", 
    value=st.session_state.dbPathway, 
    help="Enter the full file path to the database (e.g., C:\\Users\\YourName\\Documents\\Database.accdb)",
    placeholder="Enter the pathway to the database"
)

# Save button
save_button = st.button(
    "Save", 
    type="primary", 
    help="Click to save the database configuration", 
    use_container_width=True
)

if save_button:
    with open("config.toml", "w") as f:
        data["project"]["dbPathway"] = st.session_state.dbPathway
        toml.dump(data, f)
    st.success("✅ Database configuration saved successfully.") 

    # Attempt to connect to the database
    try:
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        test_query = "SELECT TOP 1 Title FROM Resources;"
        test = pd.read_sql(test_query, conn)
        st.success("✅ Connection to the database successful.")
    except Exception as e:
        st.error(f"❌ Error connecting to the database: {e}")
        st.stop()
