import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

def edit_global_rating(resourceID):
    try:
        # Connection string for Access database
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        cursor = conn.cursor()

        # Load the Reviews table
        query = f"SELECT Rating FROM Reviews WHERE ResourceID = {resourceID};"
        individual_rating = pd.read_sql(query, conn)

        # Calculate the global rating
        if individual_rating.empty:
            global_rating = None
        else:
            global_rating = individual_rating['Rating'].mean()

        # Update the Resources table using parameters
        update_query = "UPDATE Resources SET [Rating] = ? WHERE ResourceID = ?;"
        params = (global_rating, resourceID)
        cursor.execute(update_query, params)
        conn.commit()

    except Exception as e:
        st.error(f"An error as occured when updating the rating: {e}")

def add_contribution(resourceID, userID, contributionType, conn):
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Contributions (ResourceID, UserID, ContributionType, ContributionDate) VALUES (?, ?, ?, ?);"
        params = (resourceID, userID, contributionType, datetime.now())
        cursor.execute(query, params)
        conn.commit()

        query = f"SELECT TOP 1 ContributionID FROM Contributions WHERE ResourceID = {resourceID} AND UserID = {userID} AND ContributionType = '{contributionType}' ORDER BY ContributionDate DESC;"
        contributionID = cursor.execute(query).fetchone()[0]

    except Exception as e:
        st.error(f"An error as occured when saving the contribution: {e}")
    
    return contributionID

@st.dialog("Add a Review", width="small")
def add_review(resourceID, userID):
    with st.form("Add a Review"):
        try:
            # Connection string for Access database
            conn = pyodbc.connect(f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};")
            cursor = conn.cursor()

            # Load the Resources table
            error_message = "An error as occured when loading the data."

            query = f"SELECT Reviews.*, Users.Username FROM Reviews LEFT JOIN Users ON Reviews.UserID = Users.UserID WHERE ResourceID = {resourceID} AND Reviews.UserID = {userID};"
            old_review = pd.read_sql(query, conn)

            if old_review.empty:

                # Form template
                rating = st.slider("Rating", min_value=0, max_value=5, value=0)
                review = st.text_area("Review",help=(
                                            "You can use Markdown to format your notes. "
                                            "[Click here to learn more about Markdown](https://www.markdownguide.org/cheat-sheet/).\n\n"
                                            "**Examples of Markdown formatting:**\n"
                                            "- *Italic text*: `*italic*`\n"
                                            "- **Bold text**: `**bold**`\n"
                                            "- [Link](https://example.com): `[Link](https://example.com)`"),)
                username = st.text_input("User", value=st.session_state.userName)

                submit = st.form_submit_button("Save Review", use_container_width=True, type="primary")

                if submit:
                    # Add the contribution to the Contributions table
                    contributionID = add_contribution(resourceID, userID, "Add Review", conn)
                    
                    # Update the Reviews table using parameters
                    update_query = """
                    INSERT INTO Reviews (ResourceID, Rating, Review, UserID, ReviewDate, ContributionID)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
                    params = (resourceID, int(rating), review, userID, datetime.now(), contributionID)

                    error_message = "An error as occured when saving the review."
                    cursor.execute(update_query, params)
                    conn.commit()

                    # Update the number of contributions in the Users table
                    query = f"UPDATE Users SET UserContributions = UserContributions + 1 WHERE UserID = {userID}"
                    cursor.execute(query)
                    conn.commit()

                    st.success("Review added successfully.")

                edit_global_rating(resourceID)

            else:
                st.info("You have already reviewed this resource.\n\nBy submitting this form, you will update your review.")
                
                old_review = old_review.iloc[0]
 
                rating = st.slider("Rating", min_value=0, max_value=5, value=old_review['Rating'])
                review = st.text_area("Review", value=old_review['Review'])
                username = st.text_input("User", value=st.session_state.userName)

                submit = st.form_submit_button("Update Review", use_container_width=True, type="primary", help="By submitting this form, you will update your review.")

                if submit:
                    # Delete the previous contribution about this resource
                    query = f"DELETE FROM Contributions WHERE ContributionID IN (SELECT ContributionID FROM Contributions WHERE UserID = {userID} AND ResourceID = {resourceID} AND ContributionType LIKE '%Review%');"
                    cursor.execute(query)
                    conn.commit()

                    # Add the contribution to the Contributions table
                    contributionID = add_contribution(resourceID, userID, "Edit Review", conn)

                    # Update the Reviews table using parameters
                    update_query = f"UPDATE Reviews SET [ReviewDate] = ?, [Rating] = ?, [Review] = ?, [UserID] = ?, [ContributionID] = ? WHERE ReviewID = ?;"
                    params = (datetime.now(), int(rating), review, userID, contributionID, int(old_review['ReviewID']))
                    error_message = "An error as occured when updating the review."
                    
                    cursor.execute(update_query, params)
                    conn.commit()

                    st.success("Review updated successfully.")

                    edit_global_rating(resourceID)


        except Exception as e:
            st.error(f"{error_message}: {e}")

        finally:
            conn.close()

        st.form_submit_button(" ", type="tertiary")