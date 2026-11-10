import streamlit as st
from database import load_data, create_connection, add_student

def branchadmin_students(branch_name):
    st.header("Manage Students")
     # Form for adding students
    with st.form("add_student_form_branch"):
        student_name = st.text_input("Student Name")
        classes_df = load_data(f"SELECT id, class, section FROM Classes WHERE branch_id = (SELECT id from Schools WHERE branch_name = '{branch_name}')")
        if not classes_df.empty:
            class_id = st.selectbox("Select Class", options=classes_df['id'].tolist(),format_func=lambda x: f"Class {classes_df[classes_df['id'] == x]['class'].iloc[0]}-{classes_df[classes_df['id'] == x]['section'].iloc[0]}")
            submitted = st.form_submit_button("Add Student")
            if submitted and student_name and class_id:
                if add_student(class_id, student_name):
                    st.success(f"Student '{student_name}' added to the class successfully!")
                else:
                    st.error("Error adding Student, Please check the details")
        else:
            st.warning(f"No classes available in {branch_name}")

    students_df = load_data(f"SELECT s.id, s.student_name, c.class, c.section FROM Students s JOIN Classes c ON s.class_id = c.id  WHERE c.branch_id = (SELECT id from Schools WHERE branch_name = '{branch_name}')")
    # Form for deleting a student
    with st.form("delete_student_form_branch"):
        if not students_df.empty:
            student_to_delete = st.selectbox("Select Student to Delete", options=students_df['student_name'].tolist())
            delete_student_submitted = st.form_submit_button("Delete Student")
            if delete_student_submitted and student_to_delete:
                conn = create_connection("school.db")
                try:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM Students WHERE student_name = ? AND class_id IN (SELECT id FROM Classes WHERE branch_id = (SELECT id from Schools WHERE branch_name = ?))", (student_to_delete, branch_name))
                        conn.commit()
                        st.success(f"Student '{student_to_delete}' deleted successfully!")
                except Exception as e:
                    st.error(f"Error deleting student: {e}")
        else:
             st.warning("No Students available")

    # Display Existing Students
    if not students_df.empty:
        st.subheader("Existing Students")
        st.dataframe(students_df)
    else:
         st.warning("No students available.")