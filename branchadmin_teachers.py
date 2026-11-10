import streamlit as st
from database import load_data, create_connection

def branchadmin_teachers(branch_name):
    st.header("Manage Teachers")
     # Add Teacher Form
    with st.form("add_teacher_form_branch"):
        teacher_name = st.text_input("Teacher Name")
        school_name = st.text_input("School Name")
        subject = st.text_input("Subject")
        submitted = st.form_submit_button("Add Teacher")

        if submitted and teacher_name and school_name and subject:
            conn = create_connection("school.db")
            try:
                with conn:
                    conn.execute("""
                        INSERT INTO Teachers (teacher_name, school_name, branch_name, subject)
                        VALUES (?, ?, ?, ?)
                    """, (teacher_name, school_name, branch_name, subject))
                    st.success(f"Teacher '{teacher_name}' added successfully!")
            except Exception as e:
                st.error(f"Error adding teacher: {e}")

    # Delete Teacher by Name
    with st.form("delete_teacher_form_branch"):
        teacher_name_to_delete = st.text_input("Teacher Name to Delete")
        delete_teacher_submitted = st.form_submit_button("Delete Teacher")

        if delete_teacher_submitted and teacher_name_to_delete:
            conn = create_connection("school.db")
            try:
                with conn:
                    conn.execute("DELETE FROM Teachers WHERE teacher_name = ? AND branch_name = ?", (teacher_name_to_delete,branch_name))
                    st.success(f"Teacher '{teacher_name_to_delete}' deleted successfully!")
            except Exception as e:
                st.error(f"Error deleting teacher: {e}")

    teachers_df = load_data(f"SELECT * FROM Teachers WHERE branch_name = '{branch_name}'")
    if not teachers_df.empty:
        st.subheader("Existing Teachers")
        st.dataframe(teachers_df)
    else:
        st.warning("No teachers available. Please add teachers.")