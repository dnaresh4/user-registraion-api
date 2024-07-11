import os
import requests
import json

def get_sonarcloud_issues(sonar_token, project_key, pullRequest, organization):
    url = f"https://sonarcloud.io/api/issues/search"
    params = {
        "componentKeys": project_key,
        "pullRequest": pullRequest,
        "organization": organization,
        "resolved": "false"
    }
    headers = {
        "Authorization": f"Bearer {sonar_token}"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def extract_issues(report):
    issues = report.get('issues', [])
    return [issue for issue in issues]

def save_issues_to_json(issues, output_file):
    with open(output_file, 'w') as f:
        json.dump(issues, f, indent=2)

def main():
    sonar_token = os.getenv('SONAR_TOKEN')
    project_key = os.getenv('SONAR_PROJECT_KEY')
    pullRequest = os.getenv('GITHUB_PULL_REQUEST_NUMBER')
    organization = os.getenv('SONAR_ORGANIZATION')

    if not all([sonar_token, project_key, pullRequest, organization]):
        raise ValueError("Missing required environment variables")

    report = get_sonarcloud_issues(sonar_token, project_key, pullRequest, organization)
    issues = extract_issues(report)
    save_issues_to_json(issues, 'sonarqube-report.json')

    print(f"Extracted {len(issues)} issues and saved to sonarqube-report.json")

if __name__ == "__main__":
    main()
