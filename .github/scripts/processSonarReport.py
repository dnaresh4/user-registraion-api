import os
import json
import openai
from github import Github

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

def post_github_review_comment(issue, suggestion, repo, pr_number, github_token):
    g = Github(github_token)
    repository = g.get_repo(repo)
    pull_request = repository.get_pull(pr_number)
    
    file_path = issue['component'].replace('src/main/java/', '')
    line = issue.get('line', 1)
    
    body = f"Issue: {issue['message']}\n\nSuggestion: {suggestion}"
    
    review_comment = {
        "path": file_path,
        "position": line,
        "body": body,
        "side": "RIGHT",
        "start_side": "RIGHT"
    }
    
    pull_request.create_review(body=body, event="COMMENT", comments=[review_comment])

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('GITHUB_PULL_REQUEST_NUMBER')

    if not all([openai_api_key, github_token, repo, pr_number]):
        raise ValueError("Missing required environment variables")
    
    pr_number = int(pr_number) # Convert to integer

    with open('sonarqube-report.json', 'r') as f:
        issues = json.load(f)

    for issue in issues:
        suggestion = get_openai_suggestions(issue['message'], openai_api_key)
        post_github_comment(issue, suggestion, repo, pr_number, github_token)
        print(f"Posted suggestion for issue: {issue['message']}")

if __name__ == "__main__":
    main()
