import streamlit as st
import json
from github import Github, InputGitTreeElement
import base64
import os

# GitHub credentials
GITHUB_TOKEN = "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"
REPO_NAME = "format81/files-streamlit-to-github"
FILE_PATH = "navigator"

def upload_to_github(json_content, commit_message):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Convert JSON to string
    json_str = json.dumps(json_content, indent=4)

    try:
        # Get the file contents from GitHub
        contents = repo.get_contents(FILE_PATH)
        sha = contents.sha
        # Update the file
        repo.update_file(contents.path, commit_message, json_str, sha)
        st.success("File updated successfully.")
    except:
        # If file does not exist, create it
        repo.create_file(FILE_PATH, commit_message, json_str)
        st.success("File created successfully.")

st.title("JSON to GitHub")

json_input = st.text_area("Enter JSON here")

commit_message = st.text_input("Commit Message")

if st.button("Upload to GitHub"):
    try:
        json_content = json.loads(json_input)
        upload_to_github(json_content, commit_message)
    except json.JSONDecodeError:
        st.error("Invalid JSON. Please correct it and try again.")
