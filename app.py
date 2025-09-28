import streamlit as st
from github import Github
import os
import datetime

st.title("Student Project Submission")

# --- Inputs ---
student_name = st.text_input("Enter your full name")
uploaded_files = st.file_uploader(
    "Upload your project files (images, videos, PDFs, ZIPs)",
    type=["png","jpg","jpeg","mp4","pdf","zip"],
    accept_multiple_files=True
)

# --- GitHub config ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "alishad846/Project-submission-students"
FOLDER_NAME = "submissions"

# Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# --- Submission logic ---
if st.button("Submit"):
    if not student_name or not uploaded_files:
        st.error("Please enter your name and select at least one file.")
    else:
        uploaded_file_names = []
        for uploaded_file in uploaded_files:
            try:
                # Timestamp to make file names unique
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"{timestamp}_{uploaded_file.name}"
                repo_path = f"{FOLDER_NAME}/{student_name}/{file_name}"

                # Read raw bytes
                content = uploaded_file.read()

                # Create file in repo
                repo.create_file(
                    path=repo_path,
                    message=f"Submission: {student_name} - {uploaded_file.name}",
                    content=content
                )
                uploaded_file_names.append(uploaded_file.name)

            except Exception as e:
                st.error(f"Error uploading {uploaded_file.name}: {e}")

        if uploaded_file_names:
            st.success(f"Uploaded files successfully: {', '.join(uploaded_file_names)}")
