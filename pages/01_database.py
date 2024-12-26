import streamlit as st
import pandas as pd
import pyodbc
import toml

with open("config.toml", "r") as f:
    data = toml.load(f)
    st.session_state.dbPathway = data["project"]["dbPathway"]

st.title("Database Configuration :file_cabinet:")
st.write("To get started with LitExplorer, you need to link the application to an Access database. Follow the steps below based on your storage preference:")

st.markdown("---")

st.markdown(
    """
    #### Step 1: Download the Database

    :inbox_tray:[Download the Access database template]() to get a pre-configured file with all the required tables and fields. Alternatively, create your own database by replicating the provided structure.
    """
)

st.markdown(
    """
    #### Step 2: Save Your Database
Depending on your needs, you can store the database:

* :floppy_disk: **Locally**: Ideal for individual projects, save the file to a directory on your computer.

* :card_file_box: **On a Local Server**: Perfect for teamwork in a fixed office, store the file in a shared folder on a network server.

* :globe_with_meridians: **On SharePoint**: For remote collaboration:
    * Create a Microsoft Teams group if one doesn’t exist.
    * Add the database file to the Files tab under a folder of your choice.
    * Synchronize the folder using OneDrive for easy access in your file explorer.
    * (See detailed video tutorial)
    """
)

st.markdown(
    """
    #### Step 3: Connect to the Database
Paste the full file path (right-click your database file and select *Copy as Path*) and 
click **Save** to establish the connection. 

:warning: Make sure there are no quotes around the path.
    """
)

st.session_state.dbPathway = st.text_input("Database Pathway", value=st.session_state.dbPathway, help="Enter the pathway to the database", placeholder="Enter the pathway to the database")

save_button = st.button("Save", type="primary", help="Click to save the database configuration", use_container_width=True)

if save_button:
    with open("config.toml", "w") as f:
        data["project"]["dbPathway"] = st.session_state.dbPathway
        toml.dump(data, f)
    st.success("✅ Database configuration saved successfully") 

    try:
        conn=pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        test_query = "SELECT TOP 1 Title FROM Resources;"
        test = pd.read_sql(test_query, conn)
        st.success("✅ Connection to the database successful.")
    except Exception as e:
        st.error(f"❌ Error connecting to the database: {e}")
        st.stop()
