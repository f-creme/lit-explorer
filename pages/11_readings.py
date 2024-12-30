import streamlit as st
import pandas as pd
import pyodbc
import numpy as np

from forms.detailed_view import show_resources_details
from forms.add_review import add_review
from forms.edit_resource import edit_resource
from forms.reading_list import modify_reading_list

dict_status = {"Not Started": 1, "In Progress": 2, "Read": 3}
dict_priority = {"Low": 1, "Medium": 2, "High": 3}

st.title('My Readings')
st.write("Here is the list of resources you have added to your reading list.")
st.write("---")

filter_status = st.sidebar.selectbox("Filter by status", ["All", "Not Started", "In Progress", "Read"])
filter_priority = st.sidebar.selectbox("Filter by priority", ["All", "Low", "Medium", "High"])
sort_field = st.sidebar.selectbox("Sort by", ["Priority", "Status", "Date Added"])

st.sidebar.markdown(f"""
                    <p style="margin: 0px; font-size: 17px; font-weight: bold; text-indent: 12px;">Legend</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> 🟢: Low priority</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> 🟡: Medium priority</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> 🟠: High priority</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> 💤: Not started</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> ⌛: In progress</p>
                    <p style="margin: 0px; font-size: 14px; text-indent: 22px;"> ✔️: Read</p>
                    """, unsafe_allow_html=True)

# Connect to the database
try:
    conn=pyodbc.connect(
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
    )

    query = f"""SELECT 
            ReadingList.ResourceID, ReadingList.Status, ReadingList.Priority, ReadingList.DateAdded, ReadingList.DateRead, 
            Resources.Title, Resources.Authors, Resources.Date 
            FROM ReadingList LEFT JOIN Resources ON ReadingList.ResourceID = Resources.ResourceID 
            WHERE ReadingList.UserID = {st.session_state.userID};
            """
    readings = pd.read_sql(query, conn)

    readings['LiteralStatus'] = readings['Status'].map({v: k for k, v in dict_status.items()})
    readings['EmojisStatus'] = readings['Status'].map({1: "&#128164;", 2: "&#8987;", 3: "✔️"})
    readings['Priority'] = readings['Priority'].fillna(0)
    readings['DateRead'] = readings['DateRead'].fillna(0)
    readings['LiteralPriority'] = readings['Priority'].map({v: k for k, v in dict_priority.items()})
    readings['EmojisPriority'] = readings['Priority'].map({1: "🟢", 2: "🟡", 3: "🟠", 0: ""})
    readings = readings.sort_values(by=['Priority', 'Status', 'DateAdded'], ascending=[False, True, True])

    if filter_status != "All":
        readings = readings[readings['LiteralStatus'] == filter_status]
    if filter_priority != "All":
        readings = readings[readings['LiteralPriority'] == filter_priority]
    if sort_field == "Priority":
        readings = readings.sort_values(by=['Priority', 'Status', 'DateAdded'], ascending=[False, True, True])
    elif sort_field == "Status":
        readings = readings.sort_values(by=['Status', 'Priority', 'DateAdded'], ascending=[True, False, True])
    elif sort_field == "Date Added":
        readings = readings.sort_values(by=['DateAdded', 'Priority', 'Status'], ascending=[True, False, False])
    

    for _, elem in readings.iterrows():
        col1, col2, col3, col4 = st.columns([2, 8, 1, 1], vertical_alignment='center', gap="small")
        with col1:
            if elem['DateRead'] == 0:
                date_to_display = elem['DateAdded']
            else:
                date_to_display = elem['DateRead']

            st.markdown(f"""
                        <p style="margin: 0px; text-align: center; font-size: 20px;">
                        {elem['EmojisPriority']}&nbsp;&nbsp;&nbsp;{elem['EmojisStatus']}
                        </p>
                        <p style="margin: 0px; text-align: center; color: #808080;">
                        {date_to_display.strftime("%d %b %Y")}
                        </p>
                        """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                        <p style="margin: 0px; font-weight: bold; color: #000000;">{elem['Title']}</p>
                        <p style="margin: 0px; color: #808080;"><i>{elem['Authors']}</i> ({elem['Date']})</p>
                        """, unsafe_allow_html=True)
            
        with col3:
            if st.button(":mag_right:", key=f"view_{elem['ResourceID']}", help="View the details of this resource."):
                st.session_state.selected_article = elem['ResourceID']
                show_resources_details(st.session_state.selected_article)
            if st.button(":lower_left_fountain_pen:", key=f"edit_{elem['ResourceID']}", help="Edit the details of this resource."):
                st.session_state.selected_article = elem['ResourceID']
                edit_resource(st.session_state.selected_article)

        with col4:
            if st.button(":thought_balloon:", key=f"review_{elem['ResourceID']}", help="Add a review to this resource."):
                st.session_state.selected_article = elem['ResourceID']
                add_review(elem['ResourceID'], st.session_state.userLogin)
            if st.button(":writing_hand:", key=f"edit_status_{elem['ResourceID']}", help="Edit the status and priority of this resource."):
                st.session_state.selected_article = elem['ResourceID']
                st.session_state.selected_status = elem['Status']
                st.session_state.selected_priority = elem['Priority']
                modify_reading_list(st.session_state.selected_article, st.session_state.selected_priority, st.session_state.selected_status)

        st.write("---")
except Exception as e:
    st.error(f":x: An error as occured :\n{e}")
    st.stop()