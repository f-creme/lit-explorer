import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime

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

        if individual_rating.empty:
            global_rating = None
        else:
            global_rating = individual_rating['Rating'].mean()

        # Update the Resources table using parameters
        update_query = """
        UPDATE Resources
        SET [Rating] = ?
        WHERE ResourceID = ?;
        """
        params = (
            global_rating, resourceID
        )
        cursor.execute(update_query, params)
        conn.commit()

    except Exception as e:
        st.error(f"An error as occured when updating the rating: {e}")

def add_contribution(resourceID, userLogin, contributionType, conn):
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Contributions (ResourceID, UserLogin, ContributionType, ContributionDate) VALUES (?, ?, ?, ?);"
        params = (resourceID, userLogin, contributionType, datetime.now())
        cursor.execute(query, params)
        conn.commit()

        query = f"SELECT TOP 1 ContributionID FROM Contributions WHERE ResourceID = {resourceID} AND UserLogin = '{userLogin}' AND ContributionType = '{contributionType}' ORDER BY ContributionDate DESC;"
        contributionID = cursor.execute(query).fetchone()[0]

    except Exception as e:
        st.error(f"An error as occured when saving the contribution: {e}")
    
    return contributionID

@st.dialog("Add a Review", width="large")
def add_review(resourceID, user):
    with st.form("Add a Review"):
        try:
            # Connection string for Access database
            conn = pyodbc.connect(
                f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
            )
            cursor = conn.cursor()

            # Load the Resources table
            error_message = "An error as occured when loading the data."
            review_query = f"SELECT * FROM Reviews WHERE ResourceID = {resourceID} AND UserLogin = '{user}';"
            user_query = f"SELECT Username FROM Users WHERE UserLogin = '{user}';"
            comment = pd.read_sql(review_query, conn)
            username = pd.read_sql(user_query, conn)['Username'].values[0]

            if comment.empty:
                # Edit form
                date = st.date_input("Date")
                rating = st.slider("Rating", min_value=0, max_value=5, value=0)
                review = st.text_area("Review")
                username = st.text_input("User", value=username)
                submit = st.form_submit_button("Save Review")
                if submit:
                    # Add the contribution to the Contributions table
                    contributionID = add_contribution(resourceID, user, "Add Review", conn)
                    
                    # Update the Reviews table using parameters
                    update_query = """
                    INSERT INTO Reviews (ResourceID, Rating, Review, UserLogin, ReviewDate, ContributionID)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
                    params = (
                        resourceID, int(rating), review, user, date, contributionID
                    )
                    error_message = "An error as occured when saving the review."
                    cursor.execute(update_query, params)
                    conn.commit()

                    st.success("Review added successfully.")

                edit_global_rating(resourceID)

            else:
                st.info("You have already reviewed this resource.\n\nBy submitting this form, you will update your review.")
                
                reviewID = int(comment.loc[0, 'ReviewID'])  
                date = st.date_input("Date", value=comment.loc[0, 'ReviewDate'])
                rating = st.slider("Rating", min_value=0, max_value=5, value=comment.loc[0, 'Rating'])
                review = st.text_area("Review", value=comment.loc[0, 'Review'])
                username = st.text_input("User", value=username)

                submit = st.form_submit_button("Update Review")
                if submit:
                    # Add the contribution to the Contributions table
                    contributionID = add_contribution(resourceID, user, "Edit Review", conn)

                    # Update the Reviews table using parameters
                    update_query = """
                    UPDATE Reviews
                    SET [ReviewDate] = ?,
                        [Rating] = ?,
                        [Review] = ?,
                        [UserLogin] = ?, 
                        [ContributionID] = ? 
                    WHERE ReviewID = ?;
                    """
                    params = (
                        date, int(rating), review, user, reviewID, contributionID
                    )
                    error_message = "An error as occured when updating the review."
                    cursor.execute(update_query, params)
                    conn.commit()

                    st.success("Review updated successfully.")

                    edit_global_rating(resourceID)


        except Exception as e:
            st.error(f"{error_message}: {e}")

        finally:
            conn.close()

        st.form_submit_button("Close")