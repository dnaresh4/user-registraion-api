import os
import json
import requests

def get_openai_suggestions(issue_description, api_key):
    openai_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": f"Provide a suggestion to fix the following issue:\n\n{issue_description}",
        "max_tokens": 100,
        "n": 1,
        "stop": "\n"
    }
    response = requests.post(openai_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()

def post_github_comment(issue, suggestion, repo, pr_number, github_token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    comment_body = {
        "body": f"Issue: {issue['message']}\n\nSuggestion: {suggestion}\n\nFile: {issue['component']}\nLine: {issue['line']}"
    }
    response = requests.post(url, headers=headers, json=comment_body)
    response.raise_for_status()

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('GITHUB_PULL_REQUEST_NUMBER')

    if not all([openai_api_key, github_token, repo, pr_number]):
        raise ValueError("Missing required environment variables")

    with open('sonarcloud_issues.json', 'r') as f:
        issues = json.load(f)

    for issue in issues:
        suggestion = get_openai_suggestions(issue['message'], openai_api_key)
        post_github_comment(issue, suggestion, repo, pr_number, github_token)
        print(f"Posted suggestion for issue: {issue['message']}")

if __name__ == "__main__":
    main()
