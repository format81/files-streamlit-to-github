import streamlit as st
import json
from github import Github

# GitHub credentials
GITHUB_TOKEN = "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"
REPO_NAME = "format81/files-streamlit-to-github"
FILE_PATH = "navigator/filename.json"  # Specify the full file path in the repo

def upload_to_github(json_content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    commit_message = "Updated via Streamlit app"

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

    # Return the raw URL of the uploaded JSON file
    raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/{FILE_PATH}"
    return raw_url

st.title("JSON to GitHub")

json_input = st.text_area("Enter JSON here")

if st.button("Upload to GitHub"):
    try:
        json_content = json.loads(json_input)
        raw_url = upload_to_github(json_content)
        
        # Embed the Navigator in an iframe
        navigator_iframe_url = f"https://mitre-attack.github.io/attack-navigator/#layerURL={raw_url}"
        iframe_navigator_html = f"""
        <iframe src="{navigator_iframe_url}" width="1200" height="800" frameborder="0"></iframe>
        """
        st.write("## Mitre Navigator ##")
        st.markdown(iframe_navigator_html, unsafe_allow_html=True)
    except json.JSONDecodeError:
        st.error("Invalid JSON. Please correct it and try again.")
