import streamlit as st
from database import load_data, create_connection

def branchadmin_overview(branch_name):
    st.header("Overview")
    st.write("This is the overview page for the branch admin")
    
    # Calculate and display total classes
    classes_count_query = f"""
        SELECT COUNT(*) AS total_classes FROM Classes WHERE branch_id = (SELECT id from Schools WHERE branch_name = '{branch_name}')
    """
    classes_count_df = load_data(classes_count_query)
    total_classes = classes_count_df['total_classes'].iloc[0] if not classes_count_df.empty else 0
    st.subheader(f"Total Classes: {total_classes}")

    # Calculate and display total teachers
    teachers_count_query = f"""
        SELECT COUNT(*) AS total_teachers FROM Teachers WHERE branch_name = '{branch_name}'
    """
    teachers_count_df = load_data(teachers_count_query)
    total_teachers = teachers_count_df['total_teachers'].iloc[0] if not teachers_count_df.empty else 0
    st.subheader(f"Total Teachers : {total_teachers}")