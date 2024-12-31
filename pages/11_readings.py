import streamlit as st
import pandas as pd
import pyodbc

from forms.detailed_view import show_resources_details
from forms.add_review import add_review
from forms.personal_notes import edit_notes
from forms.reading_list import modify_reading_list

# Dictionary to map the status and priority values
dict_status = {"Not Started": 1, "In Progress": 2, "Read": 3}
dict_priority = {"Low": 1, "Medium": 2, "High": 3}

st.title('My Readings')
st.write("Here is the list of resources you have added to your reading list.")
st.write("---")

# Sidebar
filter_status = st.sidebar.selectbox("Filter by status", ["All", "Not Started", "In Progress", "Read"])
filter_priority = st.sidebar.selectbox("Filter by priority", ["All", "Low", "Medium", "High"])
sort_field = st.sidebar.selectbox("Sort by", ["Priority", "Status", "Date Added"])

st.sidebar.info(
    """
    🟢: Low priority\n
    🟡: Medium priority\n
    🟠: High priority\n
    💤: Not started\n
    ⌛: In progress\n
    ✔️: Read
    """
)

# Function to fetch data from the database
def fetch_data(query, _conn, user_id):
    """
    Fetches data from the database based on the provided query and user ID.

    Args:
        query (str): SQL query to execute.
        _conn (pyodbc.Connection): Database connection object.
        user_id (int): User ID for filtering data.

    Returns:
        pd.DataFrame: Dataframe containing the query results.
    """
    return pd.read_sql(query, conn, params=(user_id,))

# Connection to the database
try:
    conn = pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )

    query = """
        SELECT ReadingList.ResourceID, ReadingList.Status, ReadingList.Priority, ReadingList.DateAdded, ReadingList.DateRead, 
               Resources.Title, Resources.Authors, Resources.Date 
        FROM ReadingList 
        LEFT JOIN Resources ON ReadingList.ResourceID = Resources.ResourceID 
        WHERE ReadingList.UserID = ?;
    """
    readings = fetch_data(query, conn, st.session_state.userID)

    # Transformation of the data
    readings['LiteralStatus'] = readings['Status'].map({v: k for k, v in dict_status.items()})
    readings['EmojisStatus'] = readings['Status'].map({1: "💤", 2: "⌛", 3: "✔️"})
    readings['Priority'] = readings['Priority'].fillna(0)
    readings['DateRead'] = readings['DateRead'].fillna("N/A")
    readings['LiteralPriority'] = readings['Priority'].map({v: k for k, v in dict_priority.items()})
    readings['EmojisPriority'] = readings['Priority'].map({1: "🟢", 2: "🟡", 3: "🟠", 0: ""})

    # Filterings
    if filter_status != "All":
        readings = readings[readings['LiteralStatus'] == filter_status]
    if filter_priority != "All":
        readings = readings[readings['LiteralPriority'] == filter_priority]

    # Sorting
    if sort_field == "Priority":
        readings = readings.sort_values(by=['Priority', 'Status', 'DateAdded'], ascending=[False, True, True])
    elif sort_field == "Status":
        readings = readings.sort_values(by=['Status', 'Priority', 'DateAdded'], ascending=[True, False, True])
    elif sort_field == "Date Added":
        readings = readings.sort_values(by=['DateAdded', 'Priority', 'Status'], ascending=[True, False, False])

    # Function to render the action buttons
    def render_action_buttons(resource_id, status, priority):
        """
        Renders action buttons for interacting with the reading list.

        Args:
            resource_id (int): Unique ID of the resource.
            status (int): Current status of the resource.
            priority (int): Priority level of the resource.
        """
        
        col4, col5 = st.columns([1, 1], gap="small")
        with col4:
            if st.button("🔍", key=f"view_{resource_id}", help="View the details of this resource."):
                st.session_state.selected_article = resource_id
                show_resources_details(st.session_state.selected_article)
            if st.button("📒", key=f"edit_{resource_id}", help="Edit your personal notes."):
                st.session_state.selected_article = resource_id
                edit_notes(st.session_state.selected_article)

        with col5:
            if st.button("💭", key=f"review_{resource_id}", help="Add a review to this resource."):
                st.session_state.selected_article = resource_id
                add_review(resource_id, st.session_state.userID)
            if st.button("🗂️", key=f"edit_status_{resource_id}", help="Edit the status and priority of this resource."):
                st.session_state.selected_article = resource_id
                st.session_state.selected_status = status
                st.session_state.selected_priority = priority
                modify_reading_list(resource_id, priority, status)

    # Display the readings
    for _, elem in readings.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 8, 2], vertical_alignment="center")
            with col1:
                st.markdown(
                    f"""
                    <p style="margin: 0px; text-align: center; font-size: 20px;">
                    {elem['EmojisPriority']}&nbsp;&nbsp;&nbsp;{elem['EmojisStatus']}
                    </p>
                    <p style="margin: 0px; text-align: center; color: #808080;">
                    {elem['DateAdded'].strftime('%d %b %Y') if elem['DateRead'] == 'N/A' else elem['DateRead'].strftime('%d %b %Y')}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <p style="margin: 0px; font-weight: bold; color: #000000;">{elem['Title']}</p>
                    <p style="margin: 0px; color: #808080;"><i>{elem['Authors']}</i> ({elem['Date']})</p>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                render_action_buttons(elem['ResourceID'], elem['Status'], elem['Priority'])

        st.write("---")

except pyodbc.Error as db_err:
    st.error(f"Database connection failed: {db_err}")
    st.stop()

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.stop()
