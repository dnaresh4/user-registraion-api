import os
import json
import openai
from github import Github
import subprocess

def get_openai_suggestions(issue_description, api_key):
    openai.api_key = api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Provide a suggestion to fix the following issue:\n\n{issue_description}"}
            ],
            temperature=0.7,
            max_tokens=64,
            top_p=1
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        # Mock response for testing purposes
        return "Mock suggestion: Consider refactoring the code to improve readability and maintainability."

def update_code_with_suggestion(file_path, line, suggestion):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # This is a simplified way to replace the line with the suggestion
    # You might want to improve how the suggestion is applied
    lines[line - 1] = suggestion + "\n"

    with open(file_path, 'w') as file:
        file.writelines(lines)

def run_git_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e.stderr}")
        raise

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')

    if not all([openai_api_key, github_token, repo_name]):
        raise ValueError("Missing required environment variables")

    with open('sonarcloud_issues.json', 'r') as f:
        issues = json.load(f)

    g = Github(github_token)
    repo = g.get_repo(repo_name)

    updated_files = []

    for issue in issues:
        suggestion = get_openai_suggestions(issue['message'], openai_api_key)
        file_path = issue['component'].replace('AvinashNagella1999_user-registraion-api:', '')
        line = issue.get('line', 1)
        update_code_with_suggestion(file_path, line, suggestion)
        updated_files.append(file_path)
        print(f"Updated {file_path} at line {line} with suggestion: {suggestion}")
    
    if not updated_files:
        print("No files updated.")
        return
    
    # Commit the changes
    commit_message = "Update code based on SonarCloud issues and OpenAI suggestions"
    head_branch = os.getenv('GITHUB_HEAD_REF')

    run_git_command(["git", "config", "--global", "user.name", "github-actions[bot]"])
    run_git_command(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])


    # Add and commit the changes
    try:
        run_git_command(["git", "add"] + updated_files)
        run_git_command(["git", "commit", "-m", commit_message])
    except subprocess.CalledProcessError as e:
        print("No changes to commit.")
        return

    # Push the new branch to the remote repository
    run_git_command(["git", "push", "--set-upstream", "origin", "master"])

    print(f"Code updated and committed to branch {head_branch}.")

if __name__ == "__main__":
    main()
