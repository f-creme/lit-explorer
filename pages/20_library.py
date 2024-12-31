import streamlit as st
import pandas as pd
import pyodbc
import numpy as np

from forms.detailed_view import show_resources_details
from forms.mark_as_read import mark_as_read
from forms.edit_resource import edit_resource
from forms.add_review import add_review
from forms.reading_list import add_to_reading_list

def print_stars(rating):
    if isinstance(rating, (int, float, np.floating)):
        return "⭐️" * int(rating) + "✰" * (5 - int(rating))
    else:
        return "✰✰✰✰✰"

def split_and_flatten(column):
    return set(value.strip() for sublist in column.dropna().str.split(',') for value in sublist)

def render_action_buttons(resource_id, title):
        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="center")
        with col1:
            if st.button(f":mag_right: View", key=f"details_{resource_id}", use_container_width=True, type="primary", help="View detailed information about this article"):
                st.session_state.selected_article = resource_id
                show_resources_details(resource_id)
        with col2:
            if st.button(f":heavy_check_mark: Read", key=f"reading_{resource_id}", use_container_width=True, help="Quickly mark as read"):
                st.session_state.selected_article = resource_id
                st.session_state.selected_article_title = title
                mark_as_read(resource_id, title)
        with col3:
            if st.button(f":pushpin: To list", key=f"reading_list_{resource_id}", use_container_width=True, help="Add to your reading list"):
                st.session_state.selected_article = resource_id
                add_to_reading_list(resource_id)
        with col4:
            if st.button(f":thought_balloon: Review", key=f"review_{resource_id}", use_container_width=True, help="Add a review"):
                st.session_state.selected_article = resource_id
                add_review(resource_id, st.session_state.userID)
        with col5:
            if st.button(f":lower_left_ballpoint_pen: Edit", key=f"edit_{resource_id}", use_container_width=True, help="Edit this article"):
                st.session_state.selected_article = resource_id
                edit_resource(resource_id)

# Sort options
st.sidebar.header("Sort")
sort_by = st.sidebar.selectbox("Sort by", options=["Title", "Rating", "Date"], index=0)
sort_order = st.sidebar.radio("Sort order", options=["Ascending", "Descending"], index=0)

# Attempt to connect to the Access database
if st.session_state.dbPathway:
    st.title(f"📂 Library about Nitrosamines :")
    st.markdown("---")

    try:
        # Connection string for Access database
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )

        # Load the Articles table
        articles_query = "SELECT * FROM Resources;"
        articles = pd.read_sql(articles_query, conn)
        articles['Rating'] = articles['Rating'].fillna(0)

        conn.close()

        # Sidebar filters
        st.sidebar.header("Filters")
        filter_title = st.sidebar.text_input("Filter by Title")
        filter_author = st.sidebar.text_input("Filter by Author")
        filter_year = st.sidebar.slider("Filter by Year", min_value=1960, max_value=2030, value=(1960, 2030))
        filter_rating = st.sidebar.slider("Filter by Rating", min_value=0, max_value=5, value=(0, 5))

        # Dropdown filters for unique values and split columns
        filter_journal = st.sidebar.multiselect("Filter by Journal", options=sorted(articles['Journal'].dropna().unique()), default=[])
        filter_document_type = st.sidebar.multiselect("Filter by Document Type", options=sorted(articles['Document Type'].dropna().unique()), default=[])
        filter_article_type = st.sidebar.multiselect("Filter by Article Type", options=sorted(articles['Article type'].dropna().unique()), default=[])
        
        # For columns with multiple values separated by ","
        application_field_values = split_and_flatten(articles['Application Field'])
        category_values = split_and_flatten(articles['Category'])
        sub_category_values = split_and_flatten(articles['Sub Category'])
        keywords_values = split_and_flatten(articles['Keywords'])

        filter_application_field = st.sidebar.multiselect("Filter by Application Field", options=sorted(application_field_values), default=[])
        filter_category = st.sidebar.multiselect("Filter by Category", options=sorted(category_values), default=[])
        filter_sub_category = st.sidebar.multiselect("Filter by Sub Category", options=sorted(sub_category_values), default=[])
        filter_keywords = st.sidebar.multiselect("Filter by Keywords", options=sorted(keywords_values), default=[])

        # Apply filters
        if filter_title:
            articles = articles[articles['Title'].str.contains(filter_title, case=False, na=False)]

        if filter_author:
            articles = articles[articles['Authors'].str.contains(filter_author, case=False, na=False)]

        if filter_year:
            articles = articles[articles['Date'].apply(lambda x: int(str(x)[:4]) if pd.notnull(x) else 0).between(filter_year[0], filter_year[1])]

        if filter_rating:
            articles = articles[articles['Rating'].between(filter_rating[0], filter_rating[1])]

        if filter_journal:
            articles = articles[articles['Journal'].isin(filter_journal)]

        if filter_document_type:
            articles = articles[articles['Document Type'].isin(filter_document_type)]

        if filter_article_type:
            articles = articles[articles['Article type'].isin(filter_article_type)]

        if filter_application_field:
            articles = articles[articles['Application Field'].apply(lambda x: any(val in str(x).split(',') for val in filter_application_field))]

        if filter_category:
            articles = articles[articles['Category'].apply(lambda x: any(val in str(x).split(',') for val in filter_category))]

        if filter_sub_category:
            articles = articles[articles['Sub Category'].apply(lambda x: any(val in str(x).split(',') for val in filter_sub_category))]

        if filter_keywords:
            articles = articles[articles['Keywords'].apply(lambda x: any(val in [k.strip() for k in str(x).split(',')] for val in filter_keywords))]

        st.sidebar.write(f"Number of articles: {articles.shape[0]}")

        # Apply sorting
        ascending = sort_order == "Ascending"
        if sort_by in articles.columns:
            articles = articles.sort_values(by=sort_by, ascending=ascending)

        # Display articles with a button for details
        for index, row in articles.iterrows():
            st.subheader(f"{row['Title']}")
            st.write(f"{print_stars(row['Rating'])}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Authors:** {row['Authors']}")
                st.write(f"**Journal:** {row['Journal']}")
                st.write(f"**Document Type:** {row['Document Type']}")
                st.write(f"**Category:** {row['Category']}")
                st.write(f"**Specific to Nitrosamines:** {row['Specific to Nitrosamines']}")
            with col2:
                st.write(f"**Date:** {(row['Date'])}")
                st.write(f"**DOI:** {row['DOI']}")
                st.write(f"**Application Field:** {row['Application Field']}")
                st.write(f"**Sub Category:** {row['Sub Category']}")
            st.write(f"**Keywords:** {row['Keywords']}")

            # Button to open article details
            render_action_buttons(row['ResourceID'], row['Title'])

            st.markdown("---")

    except Exception as e:
        st.error(f"Unable to connect to the database: {e}")
else:
    st.info("No database path defined for this project.")
