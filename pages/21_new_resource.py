import streamlit as st
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Page title
st.title("Add a new resource")
st.header(f"📂 Library about  Nitrosamines :")
st.markdown("---")

# Input fields
## Resource information
st.subheader("**Resource information:**")
st.write("*The fields below are public and will be displayed in the library.*")

title = st.text_area("Title *", help="Enter the title of the resource")
authors = st.text_input("Authors *", help="Enter the authors of the resource")
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.write("**Publication details:**")
    date = st.number_input("Year of publication *", 
                           min_value=1900, max_value=2200, 
                           help="Enter the year of publication")
    document_type = st.selectbox("Document Type", 
                                 ["Journal Article", 
                                  "Patent", 
                                  "Report", 
                                  "Presentation", 
                                  "Bachelor-Thesis", 
                                  "Technical Instruction", 
                                  "Book", 
                                  "Conference Paper", 
                                  "Review", 
                                  "Other"], 
                                  help="Select the document type")
    journal = st.text_input("Name of the Journal or Publisher", 
                            help="Enter the name of the journal or publisher")
    doi = st.text_input("DOI", 
                        help="Enter the DOI of the resource, if available")
    article_type = st.selectbox("Article Type", 
                                ["Not applicable", 
                                 "Primary Research",
                                 "Review", 
                                 ], 
                                 help="If applicable, select the article type")
    
    
with col2:
    st.write("**Categorization:**")
    application_field = st.text_input("Application Field", 
                                      help=("Enter the main domain of application of the resource.\n\n"
                                            "For example: `Pharmaceuticals, Food Industry, etc.`\n\n"
                                            "If the resource belongs to multiple categories, separate them by «, » (comma + space)"))
    category = st.text_input("Category",
                             help=("Enter the main category of the resource.\n\n"
                                "For example: `Nitrosamines Formation, Mitigation, etc.`\n\n"
                                "If the resource belongs to multiple categories, separate them by «, » (comma + space)"))
    sub_category = st.text_input("Sub Category", 
                                help=("Enter the main category of the resource.\n\n"
                                "For example: `Transitrosation, NOx Mitigation, etc.`\n\n"
                                "If the resource belongs to multiple categories, separate them by «, » (comma + space)"))

    specific_to_nitrosamines = st.selectbox("Is the resource specific to nitrosamines ?", 
                                            ["Yes", "No"], 
                                            help="Precise if the resource is specific to nitrosamines")

keywords = st.text_area("Keywords", help="""Enter the keywords separated by ", " (comma + space)""")
summary = st.text_area("Summary", help="Enter a brief summary of the resource")
st.write("")

# User information
st.subheader("**User information:**")
st.write("*The fields below are private and will not be displayed in the library.*")

col3, col4 = st.columns(2)
with col3:
    status = st.segmented_control("Reading status*", ["Not Started", "In Progress", "Read"], key="status",
                                  help="Select the reading status of the resource")
with col4:
    priority = st.select_slider("Priority level", options=["Low", "Medium", "High"], key="priority",
                                help="Select the priority level of the resource")


# Submit button
submit = st.button("Save Resource", type="primary", use_container_width=True)

# Function to check for duplicate resources
def check_dupplicates(cursor, title, date):
    """
    Checks if a resource with the same title and date already exists in the database.
    
    Args:
        cursor (pyodbc.Cursor): Database cursor for executing queries.
        title (str): Title of the resource.
        date (int): Year of publication of the resource.
        
    Returns:
        bool: True if a duplicate resource is found, False otherwise.
    """
    query = "SELECT COUNT(*) FROM Resources WHERE Title = ? AND Date = ?"
    cursor.execute(query, (title, date))
    return cursor.fetchone()[0] > 0

# If the user clicks the "Save Resource" button
if submit:
    try:
        # Validate mandatory fields : Title, Authors, Year of publication, Reading status
        if not title.strip() or not authors.strip() or not date or not status:
            st.sidebar.error("Title, Authors, Year of publication, and Reading status are mandatory fields.")
            st.stop()

        # Connection string for Access database
        conn = pyodbc.connect(f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};")
        cursor = conn.cursor()

        # Check for duplicate entries
        if check_dupplicates(cursor, title, date):
            st.sidebar.error("This resource already exists in the database.")
            st.stop()

        # Insert into the Resources table using parameters
        query = """
        INSERT INTO Resources
        ([Title], [Authors], [Journal], [Date], [DOI], [Document Type], 
        [Article type], [Application Field], [Category], [Sub Category], 
        [Specific to Nitrosamines], [Keywords], [Summary])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            title, authors, journal, date, doi,
            document_type, article_type, application_field,
            category, sub_category, specific_to_nitrosamines,
            keywords, summary
        )

        cursor.execute(query, params)
        conn.commit()

        # Get the resource ID of the newly added resource
        resource_id_query = f"SELECT ResourceID FROM Resources WHERE Title = ? AND [Date] = ?"
        cursor.execute(resource_id_query, (title, date))
        resource_id = cursor.fetchone()[0]

        # Map status and priority to numeric values
        dict_status = {"Not Started": 1, "In Progress": 2, "Read": 3}
        dict_priority = {"Low": 1, "Medium": 2, "High": 3}

        # Insert into the ReadingList table
        if dict_status[status] == dict_status["Read"]:
            query = "INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded, DateRead) VALUES (?, ?, ?, ?, ?, ?)"
            params = (resource_id, st.session_state.userID, dict_status[status], 0, datetime.now(), datetime.now())
        else:
            query = f"""INSERT INTO ReadingList (ResourceID, UserID, Status, Priority, DateAdded) VALUES (?, ?, ?, ?, ?)"""
            params = (resource_id, st.session_state.userID, dict_status[status], dict_priority[priority], datetime.now())

        cursor.execute(query, params)
        conn.commit()

        # Update the number of contributions in the Users table
        update_contribution_query = f"UPDATE Users SET UserContributions = UserContributions + 1 WHERE UserID = ?"
        cursor.execute(update_contribution_query, (st.session_state.userID,))
        conn.commit()

        # Insert into list of contributions
        contributions_query = "INSERT INTO Contributions (ResourceID, ContributionType, UserID, ContributionDate) VALUES (?, ?, ?, ?)"
        contributions_params = (resource_id, "New Resource", st.session_state.userID, datetime.now())
        cursor.execute(contributions_query, contributions_params)

        conn.commit()
        conn.close()

        # Success message
        st.sidebar.success("Resource added successfully.")
        
    
    except Exception as e:
        st.sidebar.error(f"An error occurred when adding the resource:\n {e}")