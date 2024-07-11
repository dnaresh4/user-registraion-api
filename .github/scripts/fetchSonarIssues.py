import os
import requests
import json

def fetch_sonar_issues(sonar_token, sonar_project_key, sonar_organization):
    url = "https://sonarcloud.io/api/issues/search"
    params = {
        "componentKeys": sonar_project_key,
        "organization": sonar_organization,
        "branch": "master",
        "resolved": "false"
    }
    headers = {
        "Authorization": f"Bearer {sonar_token}"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    print(response.json())
    return response.json()

def save_issues_to_json(issues):
    with open('sonarcloud_issues.json', 'w') as f:
        json.dump(issues, f, indent=2)

def main():
    sonar_token = os.getenv('SONAR_TOKEN')
    sonar_project_key = os.getenv('SONAR_PROJECT_KEY')
    sonar_organization = os.getenv('SONAR_ORGANIZATION')

    if not all([sonar_token, sonar_project_key, sonar_organization]):
        raise ValueError("Missing required environment variables")

    issues = fetch_sonar_issues(sonar_token, sonar_project_key, sonar_organization)
    save_issues_to_json(issues['issues'])

if __name__ == "__main__":
    main()
