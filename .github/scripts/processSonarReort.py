import os
import json
import openai
from github import Github

# Load environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('GITHUB_REF').split('/')[-1]

# Read SonarQube report
with open('sonarqube-report.json', 'r') as f:
    report = json.load(f)

# Initialize GitHub client
g = Github(github_token)
repo = g.get_repo(repo_name)
pull_request = repo.get_pull(int(pr_number))

def get_openai_suggestion(issue_description):
    response = openai.Completion.create(
        model="text-davinci-codex",
        prompt=f"Provide a suggestion to fix the following issue in a Java Spring Boot project: {issue_description}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Iterate through issues and add review comments
for issue in report.get('issues', []):
    file_path = issue['component'].replace('java:', '')
    line = issue['line']
    message = issue['message']
    
    suggestion = get_openai_suggestion(message)
    comment_body = f"Issue: {message}\n\nSuggestion: {suggestion}"
    
    pull_request.create_review_comment(body=comment_body, commit_id=pull_request.head.sha, path=file_path, position=line)

print("Review comments added based on SonarQube report and OpenAI suggestions.")
