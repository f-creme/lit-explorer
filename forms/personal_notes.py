import streamlit as st
import pyodbc
import warnings

warnings.filterwarnings("ignore")

def validate_input(notes):
    """Validate the length of the user's input notes."""
    if len(notes) > 1000:
        raise ValueError("Your notes exceed the maximum length of 1000 characters.")
    return notes

@st.dialog("Edit Personal Notes", width="small")
def edit_notes(resource_id):
    """
    Display and allow editing of personal notes for a specific resource.

    Parameters:
        resource_id (int): The unique ID of the resource whose notes are being edited.

    Steps:
        1. Connect to the database to fetch the resource title and current notes.
        2. Display the title and existing notes.
        3. Allow the user to edit and save their notes with validation.
    """

    try:
        # Establish database connection
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state.dbPathway};"
        )
        
        # Retrieve data for the given resource ID
        with conn.cursor() as cursor:
            query = (
                "SELECT Resources.Title, ReadingList.PersonalNotes "
                "FROM ReadingList "
                "LEFT JOIN Resources ON ReadingList.ResourceID = Resources.ResourceID "
                "WHERE ReadingList.ResourceID = ?;"
            )
            cursor.execute(query, resource_id)
            data = cursor.fetchone()

        if not data:
            st.error("The resource could not be found.")
            return

        title, current_notes = data

        st.header(title)
        st.write("Your current notes:")
        st.write(current_notes if current_notes else "No notes available.")

        # Input field for editing notes
        notes = st.text_area(
            "Edit your notes",
            value=current_notes or "",
            help=(
                "You can use Markdown to format your notes. "
                "[Click here to learn more about Markdown](https://www.markdownguide.org/cheat-sheet/).\n\n"
                "**Examples of Markdown formatting:**\n"
                "- *Italic text*: `*italic*`\n"
                "- **Bold text**: `**bold**`\n"
                "- [Link](https://example.com): `[Link](https://example.com)`"
            ),
        )

        if st.button("Save your notes", type="primary", use_container_width=True):
            try:
                # Validate input
                validated_notes = validate_input(notes)

                # Update notes in the database
                with conn.cursor() as cursor:
                    update_query = "UPDATE ReadingList SET PersonalNotes = ? WHERE ResourceID = ?"
                    cursor.execute(update_query, (validated_notes, resource_id))
                conn.commit()

                st.success("Your notes have been saved successfully.\nClick anywhere outside the dialog to close it.")

            except ValueError as ve:
                st.error(f"Validation error: {ve}")

            except Exception as e:
                st.error(f"An error occurred while saving your notes: {e}")

    except pyodbc.Error as db_error:
        st.error(f"Database connection error: {db_error}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()
