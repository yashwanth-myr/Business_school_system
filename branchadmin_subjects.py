import streamlit as st
from database import load_data, create_connection

def branchadmin_subjects(branch_name):
        st.header("Manage Subjects, Chapters and Topics")
        
        # Fetch the branch ID
        conn = create_connection("school.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Schools WHERE branch_name = ?", (branch_name,))
        branch_result = cursor.fetchone()
        if branch_result:
            branch_id = branch_result[0]
        else:
            st.error("Error fetching Branch ID")
            return
        
        # --- Subject Management ---
        st.subheader("Manage Subjects")
        with st.form("add_subject_form"):
            subject_name = st.text_input("Subject Name")
            add_subject_submitted = st.form_submit_button("Add Subject")

            if add_subject_submitted and subject_name:
                try:
                    with conn:
                        cursor = conn.cursor()
                         # Check if subject already exists for the branch
                        cursor.execute("SELECT * FROM Subjects WHERE name = ? AND branch_id = ?",
                                        (subject_name, branch_id))
                        existing_subject = cursor.fetchone()
                        if existing_subject:
                            st.error(f"Subject '{subject_name}' already exists for this branch.")
                        else:
                            cursor.execute("INSERT INTO Subjects (name, branch_id) VALUES (?, ?)", (subject_name, branch_id))
                            conn.commit()
                            st.success(f"Subject '{subject_name}' added successfully!")
                except Exception as e:
                    st.error(f"Error adding subject: {e}")
        
        # Delete Subject Form
        subjects_df = load_data(f"SELECT id, name FROM Subjects WHERE branch_id = {branch_id}")
        with st.form("delete_subject_form"):
            if not subjects_df.empty:
                subject_to_delete = st.selectbox("Select Subject to Delete", options=subjects_df['name'].tolist())
                delete_subject_submitted = st.form_submit_button("Delete Subject")

                if delete_subject_submitted and subject_to_delete:
                    try:
                        with conn:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM Subjects WHERE name = ? AND branch_id = ?", (subject_to_delete,branch_id))
                            conn.commit()
                            st.success(f"Subject '{subject_to_delete}' deleted successfully!")
                    except Exception as e:
                        st.error(f"Error deleting subject: {e}")
            else:
                 st.warning("No Subjects available. Please add subjects first.")
        
        # Display Subjects Table
        if not subjects_df.empty:
            st.subheader("Existing Subjects")
            st.dataframe(subjects_df)
        else:
            st.warning("No subjects available")
        
        
        
        # Add a new sub-page for viewing chapters and topics
        view_page = st.sidebar.selectbox("Subject Actions", ["Manage Subjects","View Chapters & Topics"], key="subjects_action_dropdown")
        if view_page == "View Chapters & Topics":
           st.subheader("View Chapters and Topics")

            # Select Subject for Chapter Management
           if not subjects_df.empty:
               selected_subject_view = st.selectbox("Select Subject to View Chapters & Topics", options=subjects_df['name'].tolist(), key = "select_subject_dropdown")
               # Get the ID of the selected subject
               cursor.execute("SELECT id FROM Subjects WHERE name = ? AND branch_id = ?", (selected_subject_view, branch_id))
               subject_result = cursor.fetchone()
               if subject_result:
                  selected_subject_id_view = subject_result[0]
               else:
                   st.error("Error fetching Subject ID")
                   return

               # Fetch Chapters and Topics
               chapters_query = f"""
                SELECT id, name FROM Chapters WHERE subject_id = {selected_subject_id_view}
               """
               chapters_df = load_data(chapters_query)
               if not chapters_df.empty:
                  for chapter_index, chapter_row in chapters_df.iterrows():
                     chapter_id = chapter_row['id']
                     chapter_name = chapter_row['name']
                     with st.expander(f"Chapter: {chapter_name}"):
                         topics_query = f"""
                         SELECT id, name FROM Topics WHERE chapter_id = {chapter_id}
                         """
                         topics_df = load_data(topics_query)
                         if not topics_df.empty:
                            st.write("Topics:")
                            for topic_index, topic_row in topics_df.iterrows():
                              topic_name = topic_row['name']
                              st.write(f"- {topic_name}")
                         else:
                           st.write("No topics for this chapter.")
               else:
                    st.warning("No chapters for this subject")
           else:
             st.warning("No subjects available. Please add subjects first.")

        else:
         # --- Chapter Management ---
            st.subheader("Manage Chapters")

             # Select Subject for Chapter Management
            if not subjects_df.empty:
                selected_subject = st.selectbox("Select Subject to Manage Chapters", options=subjects_df['name'].tolist())
                
                # Get the ID of the selected subject
                cursor.execute("SELECT id FROM Subjects WHERE name = ? AND branch_id = ?", (selected_subject, branch_id))
                subject_result = cursor.fetchone()
                if subject_result:
                   selected_subject_id = subject_result[0]
                else:
                    st.error("Error fetching Subject ID")
                    return
                # Form to add chapters
                with st.form("add_chapter_form"):
                    chapter_name = st.text_input("Chapter Name")
                    add_chapter_submitted = st.form_submit_button("Add Chapter")

                    if add_chapter_submitted and chapter_name:
                        try:
                             with conn:
                                cursor = conn.cursor()
                                # Check if chapter already exists for the subject
                                cursor.execute("SELECT * FROM Chapters WHERE name = ? AND subject_id = ?",
                                                (chapter_name, selected_subject_id))
                                existing_chapter = cursor.fetchone()
                                if existing_chapter:
                                    st.error(f"Chapter '{chapter_name}' already exists for subject '{selected_subject}'.")
                                else:
                                    cursor.execute("INSERT INTO Chapters (name, subject_id) VALUES (?, ?)", (chapter_name, selected_subject_id))
                                    conn.commit()
                                    st.success(f"Chapter '{chapter_name}' added successfully for subject '{selected_subject}'!")
                        except Exception as e:
                            st.error(f"Error adding chapter: {e}")

                # Delete Chapter form
                chapters_df = load_data(f"SELECT id, name FROM Chapters WHERE subject_id = {selected_subject_id}")
                with st.form("delete_chapter_form"):
                    if not chapters_df.empty:
                        chapter_to_delete = st.selectbox("Select Chapter to Delete", options=chapters_df['name'].tolist())
                        delete_chapter_submitted = st.form_submit_button("Delete Chapter")
                        if delete_chapter_submitted and chapter_to_delete:
                            try:
                                with conn:
                                    cursor = conn.cursor()
                                    cursor.execute("DELETE FROM Chapters WHERE name = ? AND subject_id = ?", (chapter_to_delete, selected_subject_id))
                                    conn.commit()
                                    st.success(f"Chapter '{chapter_to_delete}' deleted successfully!")
                            except Exception as e:
                                st.error(f"Error deleting chapter: {e}")
                    else:
                        st.warning("No chapters available. Please add chapters first.")

                # Display Chapters Table
                if not chapters_df.empty:
                     st.subheader(f"Existing Chapters for {selected_subject}")
                     st.dataframe(chapters_df)
                else:
                   st.warning(f"No chapters available for {selected_subject}.")
            else:
                st.warning("Please add subjects first")

            # --- Topic Management ---
            st.subheader("Manage Topics")
            if not subjects_df.empty:
                # Select a subject for topic management
               selected_subject_for_topic = st.selectbox("Select Subject for Topic Management", options=subjects_df['name'].tolist(), key="subject_topic_dropdown")
               
               # Get the ID of the selected subject
               cursor.execute("SELECT id FROM Subjects WHERE name = ? AND branch_id = ?", (selected_subject_for_topic, branch_id))
               subject_topic_result = cursor.fetchone()
               if subject_topic_result:
                   selected_subject_topic_id = subject_topic_result[0]
               else:
                   st.error("Error fetching Subject ID")
                   return

               chapters_for_topic_df = load_data(f"SELECT id, name FROM Chapters WHERE subject_id = {selected_subject_topic_id}")

               if not chapters_for_topic_df.empty:
                    # Select chapter for topic management
                    selected_chapter = st.selectbox("Select Chapter to Manage Topics", options=chapters_for_topic_df['name'].tolist())
                    
                    # Get the ID of the selected chapter
                    cursor.execute("SELECT id FROM Chapters WHERE name = ? AND subject_id = ?", (selected_chapter, selected_subject_topic_id))
                    chapter_topic_result = cursor.fetchone()
                    if chapter_topic_result:
                        selected_chapter_id = chapter_topic_result[0]
                    else:
                         st.error("Error fetching Chapter ID")
                         return
                    # Form to add topic
                    with st.form("add_topic_form"):
                        topic_name = st.text_input("Topic Name")
                        add_topic_submitted = st.form_submit_button("Add Topic")

                        if add_topic_submitted and topic_name:
                            try:
                                with conn:
                                    cursor = conn.cursor()
                                    # Check if topic already exists for chapter
                                    cursor.execute("SELECT * FROM Topics WHERE name = ? AND chapter_id = ?",
                                                (topic_name, selected_chapter_id))
                                    existing_topic = cursor.fetchone()
                                    if existing_topic:
                                        st.error(f"Topic '{topic_name}' already exists for chapter '{selected_chapter}'.")
                                    else:
                                        cursor.execute("INSERT INTO Topics (name, chapter_id) VALUES (?, ?)", (topic_name, selected_chapter_id))
                                        conn.commit()
                                        st.success(f"Topic '{topic_name}' added successfully for chapter '{selected_chapter}'!")
                            except Exception as e:
                                st.error(f"Error adding topic: {e}")
                    
                    # Delete Topic Form
                    topics_df = load_data(f"SELECT id, name FROM Topics WHERE chapter_id = {selected_chapter_id}")
                    with st.form("delete_topic_form"):
                         if not topics_df.empty:
                            topic_to_delete = st.selectbox("Select Topic to Delete", options=topics_df['name'].tolist())
                            delete_topic_submitted = st.form_submit_button("Delete Topic")
                            if delete_topic_submitted and topic_to_delete:
                                try:
                                    with conn:
                                        cursor = conn.cursor()
                                        cursor.execute("DELETE FROM Topics WHERE name = ? AND chapter_id = ?", (topic_to_delete, selected_chapter_id))
                                        conn.commit()
                                        st.success(f"Topic '{topic_to_delete}' deleted successfully!")
                                except Exception as e:
                                    st.error(f"Error deleting topic: {e}")
                         else:
                            st.warning("No topics available. Please add topics first.")
                    # Display Topics Table
                    if not topics_df.empty:
                       st.subheader(f"Existing Topics for {selected_chapter}")
                       st.dataframe(topics_df)
                    else:
                       st.warning(f"No topics available for {selected_chapter}.")
               else:
                  st.warning(f"Please add chapters first for {selected_subject_for_topic}")
            else:
                st.warning("Please add subjects first")