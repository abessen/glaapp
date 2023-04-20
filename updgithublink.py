from github import Github
import base64
import os

GITHUB_ACCESS_TOKEN = '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'

def update_excel_file_in_github(repo_name, file_path, file_content, commit_message):
    g = Github(GITHUB_ACCESS_TOKEN, per_page=30)  # Increase the timeout duration to 30 seconds
    repo = g.get_repo(repo_name)
    
    # Get the existing file
    contents = repo.get_contents(file_path)
    
    # Update the file
    repo.update_file(contents.path, commit_message, file_content, contents.sha)

#local_excel_file_path = r'C:\glaapp\requirements.txt'
local_excel_file_path = r'C:\glaapp\GLADisplay1.py'

with open(local_excel_file_path, 'rb') as f:
    file_content = f.read()

repo_name = 'abessen/glaapp'
#file_path = 'requirements.txt'
file_path = 'GLADisplay1.py'
commit_message = 'Update requirements with new data'
update_excel_file_in_github(repo_name, file_path, file_content, commit_message)
