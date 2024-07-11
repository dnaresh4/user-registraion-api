import os
import requests
import json

def get_sonarcloud_issues(sonar_token, project_key, pull_request, organization):
    url = "https://sonarcloud.io/api/issues/search"
    params = {
        "componentKeys": project_key,
        "pullRequest": pull_request,
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
    if 'issues' not in report:
        raise ValueError("Expected 'issues' key in the report")
    return report['issues']

def save_issues_to_json(issues, output_file):
    with open(output_file, 'w') as f:
        json.dump(issues, f, indent=2)

def main():
    sonar_token = os.getenv('SONAR_TOKEN')
    project_key = os.getenv('SONAR_PROJECT_KEY')
    pull_request = os.getenv('GITHUB_PULL_REQUEST_NUMBER')
    organization = os.getenv('SONAR_ORGANIZATION')

    if not all([sonar_token, project_key, pull_request, organization]):
        raise ValueError("Missing required environment variables")

    report = get_sonarcloud_issues(sonar_token, project_key, pull_request, organization)
    issues = extract_issues(report)
    save_issues_to_json(issues, 'sonarqube-report.json')

    print(f"Extracted {len(issues)} issues and saved to sonarqube-report.json")

if __name__ == "__main__":
    main()
