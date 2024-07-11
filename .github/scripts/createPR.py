import os
from github import Github

def create_pull_request(repo, base_branch, head_branch, github_token):
    g = Github(github_token)
    repository = g.get_repo(repo)

    pull_request = repository.create_pull(
        title="Update code based on SonarCloud issues and OpenAI suggestions",
        body="This pull request updates the code based on the issues identified by SonarCloud and suggestions provided by OpenAI.",
        head=head_branch,
        base=base_branch
    )

    print(f"Pull request created: {pull_request.html_url}")

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    base_branch = "release"
    head_branch = "master"

    if not all([github_token, repo, head_branch]):
        raise ValueError("Missing required environment variables")

    create_pull_request(repo, base_branch, head_branch, github_token)

if __name__ == "__main__":
    main()
