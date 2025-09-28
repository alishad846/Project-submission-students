import streamlit as st
from github import Github
import os
import datetime
import tempfile

# ===========================
# Configuration
# ===========================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "alishad846/Project-submission-students"
FOLDER_NAME = "submissions"
MAX_FILE_SIZE_MB = 50  # Maximum size per file

st.set_page_config(page_title="Shad's Project Submission", layout="centered")
st.title("Shad's Student Project Submission")

# ===========================
# Input fields
# ===========================
student_name = st.text_input("Enter your full name")
uploaded_files = st.file_uploader(
    "Upload your project files (images, videos, PDFs, ZIPs)",
    type=["png","jpg","jpeg","mp4","pdf","zip"],
    accept_multiple_files=True
)

# ===========================
# GitHub Repo Access
# ===========================
if not GITHUB_TOKEN:
    st.error("GitHub token not configured! Please set GITHUB_TOKEN in secrets or .env")
else:
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
    except Exception as e:
        st.error(f"Error accessing repository: {e}")

# ===========================
# Submit Button
# ===========================
if st.button("Submit"):
    if not student_name:
        st.error("Please enter your name.")
    elif not uploaded_files:
        st.error("Please select at least one file.")
    else:
        uploaded_file_names = []
        for uploaded_file in uploaded_files:
            try:
                # Check file size
                uploaded_file.seek(0, os.SEEK_END)
                file_size_mb = uploaded_file.tell() / (1024 * 1024)
                uploaded_file.seek(0)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    st.warning(f"{uploaded_file.name} is larger than {MAX_FILE_SIZE_MB}MB and will be skipped.")
                    continue

                # Generate unique filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"{timestamp}_{uploaded_file.name}"
                repo_path = f"{FOLDER_NAME}/{student_name}/{file_name}"

                # Use a temporary file to avoid memory issues with large files
                with tempfile.NamedTemporaryFile() as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp.flush()
                    with open(tmp.name, "rb") as f:
                        content = f.read()
                    repo.create_file(
                        path=repo_path,
                        message=f"Submission: {student_name} - {uploaded_file.name}",
                        content=content
                    )

                uploaded_file_names.append(uploaded_file.name)

            except Exception as e:
                st.error(f"Error uploading {uploaded_file.name}: {e}")

        if uploaded_file_names:
            st.success(f"Files uploaded successfully: {', '.join(uploaded_file_names)}")
