import os
import requests
import openai
import json

# Get environment variables
sonar_token = os.getenv('SONAR_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
github_token = os.getenv('GITHUB_TOKEN')
repo = os.getenv('GITHUB_REPOSITORY')
pull_request_number = os.getenv('GITHUB_PULL_REQUEST_NUMBER')

# Set up OpenAI API key
openai.api_key = openai_api_key

# Function to get suggestions from OpenAI
def get_openai_suggestions(issue_text):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Suggest improvements for the following code issue:\n{issue_text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Load SonarCloud report
with open('sonarqube-report.json') as f:
    report = json.load(f)

# Process issues and create review comments
comments = []
for issue in report['issues']:
    issue_text = issue['message']
    suggestion = get_openai_suggestions(issue_text)
    comments.append({
        'path': issue['component'],
        'side': 'RIGHT',
        'body': f"Issue: {issue_text}\nSuggestion: {suggestion}",
        'start_line': issue['line'],
        'line': issue['line']
    })

# Post comments to GitHub pull request
if comments:
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    for comment in comments:
        url = f'https://api.github.com/repos/{repo}/pulls/{pull_request_number}/comments'
        response = requests.post(url, headers=headers, json=comment)
        response.raise_for_status()

print('Review comments added successfully.')
