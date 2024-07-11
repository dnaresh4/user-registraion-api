import os
import json
import openai
import requests

def get_openai_suggestions(issue_description, api_key):
    openai.api_key = api_key
    try: 
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Provide a suggestion to fix the following issue:\n\n{issue_description}"}
            ],
            max_tokens=100,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except openai.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        # Mock response for testing purposes
        return "Mock suggestion: Consider refactoring the code to improve readability and maintainability."

def post_github_comment(issue, suggestion, repo, pr_number, github_token):
    url = f"https://github.com/repos/{repo}/issues/{pr_number}/comments"
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

    with open('sonarqube-report.json', 'r') as f:
        issues = json.load(f)

    for issue in issues:
        suggestion = get_openai_suggestions(issue['message'], openai_api_key)
        post_github_comment(issue, suggestion, repo, pr_number, github_token)
        print(f"Posted suggestion for issue: {issue['message']}")

if __name__ == "__main__":
    main()
