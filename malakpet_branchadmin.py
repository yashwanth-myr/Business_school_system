import streamlit as st
from database import create_connection, load_data

def malakpet_branchadmin_dashboard():
    st.title("Malakpet Branch Admin Dashboard")
    if "branch_admin_logged_in" not in st.session_state:
        st.session_state.branch_admin_logged_in = False
    
    if not st.session_state.branch_admin_logged_in:
        st.header(f"Welcome Malakpet Branch Admin")
        with st.form("branch_login_form"):
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted and password:
                # validate if the branch name and password is correct from the schools table
                branch_auth_query = f"""
                       SELECT * FROM Schools WHERE branch_name = 'Malakpet'
                """
                branch_auth_details = load_data(branch_auth_query)

                if not branch_auth_details.empty:
                     stored_password = branch_auth_details['password'].iloc[0]
                     if (password == stored_password):
                        st.session_state.branch_admin_logged_in = True
                        st.session_state.user = ("Malakpet", None, None, "BranchAdmin",None)
                        st.success(f"Logged in to branch: Malakpet")
                     else:
                        st.error("Invalid branch name or password")
                else:
                    st.error("Invalid branch name or password")
        return
    else:
         st.sidebar.title("Navigation")
         page = st.sidebar.selectbox("Choose a page", ["Overview", "Classes", "Teachers", "Subjects","Students", "Bulk Upload"])

         if page == "Overview":
            st.header("Overview")
            st.write("This is the overview page for the branch admin")
         elif page == "Classes":
            st.header("Manage Classes")
         elif page == "Teachers":
             st.header("Manage Teachers")
         elif page == "Subjects":
            st.header("Manage Subjects, Chapters and Topics")
         elif page == "Students":
             st.header("Manage Students")
         elif page == "Bulk Upload":
              st.header("Bulk Upload")