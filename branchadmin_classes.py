import streamlit as st
from database import load_data, create_connection

def branchadmin_classes(branch_name):
    st.header("Manage Classes")
    # Form for adding classes
    with st.form("add_class_form_branch"):
        class_no = st.number_input("Class Number", min_value=1, max_value=12, step=1)
        section = st.text_input("Section")
        no_of_students = st.number_input("Number of Students", min_value=0, step=1)
        submitted = st.form_submit_button("Add Class")

        if submitted and class_no and section and no_of_students:
            conn = create_connection("school.db")
            try:
                with conn:
                    # Fetch the branch_id based on school_name and branch_name
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM Schools WHERE branch_name = ?",
                                    (branch_name,))
                    result = cursor.fetchone()
                    if result:
                        branch_id = result[0]
                        # Check if class already exists
                        cursor.execute("SELECT * FROM Classes WHERE branch_id = ? AND class = ? AND section = ?",
                                        (branch_id, class_no, section))
                        existing_class = cursor.fetchone()
                        if existing_class:
                            st.error(f"Class {class_no}-{section} already exists for branch.")
                        else:
                            conn.execute("""
                                INSERT INTO Classes (branch_id, class, section, no_of_students)
                                VALUES (?, ?, ?, ?)
                            """, (branch_id, class_no, section, no_of_students))
                            st.success(f"Class {class_no}-{section} added successfully!")

            except Exception as e:
                    st.error(f"Error adding class: {e}")
        # Form to update class
        classes_df = load_data(f"SELECT id, class, section, branch_id, no_of_students FROM Classes WHERE branch_id = (SELECT id from Schools WHERE branch_name = '{branch_name}')")
        with st.form("update_class_form_branch"):
            if not classes_df.empty:
                class_id = st.selectbox("Select class to update", options=classes_df['id'].tolist(),
                                        format_func=lambda x: f"Class {classes_df[classes_df['id'] == x]['class'].iloc[0]}-{classes_df[classes_df['id'] == x]['section'].iloc[0]}")
                new_class_no = st.number_input("New Class Number", min_value=1, max_value=12, step=1)
                new_section = st.text_input("New Section")
                new_no_of_students = st.number_input("Number of Students", min_value=0, step=1)
                update_submitted = st.form_submit_button("Update Class")

                if submitted and new_class_no and new_section and new_no_of_students:
                    conn = create_connection("school.db")
                    try:
                        with conn:
                            conn.execute("""
                                UPDATE Classes
                                SET class = ?, section = ?, no_of_students = ?
                                WHERE id = ?
                            """, (new_class_no, new_section, new_no_of_students, class_id))
                            st.success(f"Class updated to {new_class_no}-{new_section} successfully!")
                    except Exception as e:
                        st.error(f"Error updating class: {e}")
                else:
                    st.warning("No classes available. Please add classes first.")
            # Form to delete class
            with st.form("delete_class_form_branch"):
                if not classes_df.empty:
                    class_no_to_delete = st.number_input("Class Number to Delete", min_value=1, max_value=12, step=1)
                    section_to_delete = st.text_input("Section to Delete")
                    delete_submitted = st.form_submit_button("Delete Class")

                    if delete_submitted and class_no_to_delete and section_to_delete:
                        conn = create_connection("school.db")
                        try:
                            with conn:
                                # Delete class based on class and section
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM Classes WHERE class = ? AND section = ? AND branch_id = (SELECT id from Schools WHERE branch_name = ?)",
                                                (class_no_to_delete, section_to_delete, branch_name))
                                if cursor.rowcount > 0:
                                    st.success(f"Class {class_no_to_delete}-{section_to_delete} deleted successfully!")
                                else:
                                    st.error(f"Class {class_no_to_delete}-{section_to_delete} not found, please check the class and section")
                        except Exception as e:
                            st.error(f"Error deleting class: {e}")
                else:
                    st.warning("No classes available. Please add classes first.")
            # Display Existing Classes
            classes_df = load_data(f"SELECT c.id, s.name as school_name, s.branch_name, c.class, c.section, c.no_of_students FROM Classes c JOIN Schools s ON c.branch_id = s.id WHERE c.branch_id = (SELECT id from Schools WHERE branch_name = '{branch_name}')")
            if not classes_df.empty:
                st.subheader("Existing Classes")
                st.dataframe(classes_df)
            else:
                st.warning("No classes available. Please add classes.")