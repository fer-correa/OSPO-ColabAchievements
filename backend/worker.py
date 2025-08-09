import yaml
import os
import requests
from datetime import datetime

# This is a placeholder for the actual API client
# In a real app, this would be a more robust client class.
API_BASE_URL = "http://127.0.0.1:8000"

def get_repos_from_org(organization: str, token: str) -> list[str]:
    """Fetches all public repository names for a given organization."""
    print(f"Fetching repositories for organization: {organization}...")
    repos = []
    url = f"https://api.github.com/orgs/{organization}/repos?type=public&per_page=100"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Will raise an exception for non-200 status
        
        repos.extend([repo["full_name"] for repo in response.json()])
        
        # Handle pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
            
    print(f"Found {len(repos)} public repositories for {organization}.")
    return repos

def get_or_create_contributor(username: str, avatar_url: str):
    """Checks if a contributor exists, if not, creates it."""
    response = requests.get(f"{API_BASE_URL}/contributors/{username}/")
    if response.status_code == 404:
        print(f"Creating new contributor: {username}")
        create_response = requests.post(
            f"{API_BASE_URL}/contributors/",
            json={"github_username": username, "avatar_url": avatar_url}
        )
        create_response.raise_for_status()
        return create_response.json()
    response.raise_for_status()
    return response.json()

def create_achievement(username: str, title: str, description: str, url: str):
    """Creates a new achievement for a contributor."""
    print(f"Creating achievement '{title}' for {username}")
    response = requests.post(
        f"{API_BASE_URL}/contributors/{username}/achievements/",
        json={
            "title": title,
            "description": description,
            "source_contribution_url": url,
            "awarded_at": datetime.utcnow().isoformat()
        }
    )
    response.raise_for_status()
    return response.json()

def process_repository(repo_name: str, token: str):
    """Fetches contributions (PRs, issues, commits) from a repo and creates achievements."""
    print(f"Processing repository: {repo_name}")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # --- Fetch Pull Requests (all states) ---
    print(f"  Fetching PRs for {repo_name}...")
    pr_url = f"https://api.github.com/repos/{repo_name}/pulls?state=all&sort=updated&direction=desc&per_page=100"
    pr_response = requests.get(pr_url, headers=headers)
    pr_response.raise_for_status()
    prs = pr_response.json()
    print(f"  Found {len(prs)} PRs.")

    for pr in prs:
        if pr.get("user"):
            username = pr["user"]["login"]
            avatar_url = pr["user"]["avatar_url"]
            get_or_create_contributor(username, avatar_url)

            if pr.get("merged_at"):
                achievement_title = f"PR Merged in {repo_name}"
                achievement_desc = f"Successfully merged PR: {pr['title']}"
                create_achievement(username, achievement_title, achievement_desc, pr["html_url"])
            elif pr.get("state") == "closed":
                achievement_title = f"PR Closed (Unmerged) in {repo_name}"
                achievement_desc = f"Closed PR: {pr['title']}"
                create_achievement(username, achievement_title, achievement_desc, pr["html_url"])
            elif pr.get("state") == "open":
                achievement_title = f"PR Opened in {repo_name}"
                achievement_desc = f"Opened PR: {pr['title']}"
                create_achievement(username, achievement_title, achievement_desc, pr["html_url"])

    # --- Fetch Issues (all states, excluding PRs) ---
    print(f"  Fetching Issues for {repo_name}...")
    issues_url = f"https://api.github.com/repos/{repo_name}/issues?state=all&sort=updated&direction=desc&per_page=100"
    issues_response = requests.get(issues_url, headers=headers)
    issues_response.raise_for_status()
    issues = issues_response.json()
    print(f"  Found {len(issues)} issues.")

    for issue in issues:
        # GitHub API returns PRs as issues, so we filter them out
        if "pull_request" not in issue and issue.get("user"):
            username = issue["user"]["login"]
            avatar_url = issue["user"]["avatar_url"]
            get_or_create_contributor(username, avatar_url)

            if issue.get("state") == "closed":
                achievement_title = f"Issue Closed in {repo_name}"
                achievement_desc = f"Closed Issue: {issue['title']}"
                create_achievement(username, achievement_title, achievement_desc, issue["html_url"])
            elif issue.get("state") == "open":
                achievement_title = f"Issue Opened in {repo_name}"
                achievement_desc = f"Opened Issue: {issue['title']}"
                create_achievement(username, achievement_title, achievement_desc, issue["html_url"])

    # --- Fetch Commits (direct commits to default branch) ---
    print(f"  Fetching Commits for {repo_name} (limited to default branch, not PRs)...")
    # Get default branch name
    repo_info_url = f"https://api.github.com/repos/{repo_name}"
    repo_info_response = requests.get(repo_info_url, headers=headers)
    repo_info_response.raise_for_status()
    default_branch = repo_info_response.json().get("default_branch", "main")

    commits_url = f"https://api.github.com/repos/{repo_name}/commits?sha={default_branch}&per_page=100"
    commits_response = requests.get(commits_url, headers=headers)
    commits_response.raise_for_status()
    commits = commits_response.json()
    print(f"  Found {len(commits)} commits on default branch.")

    for commit in commits:
        if commit.get("author") and commit["author"].get("login"):
            username = commit["author"]["login"]
            avatar_url = commit["author"]["avatar_url"]
            get_or_create_contributor(username, avatar_url)

            achievement_title = f"Direct Commit to {repo_name}"
            achievement_desc = f"Committed: {commit['commit']['message'].splitlines()[0]}"
            create_achievement(username, achievement_title, achievement_desc, commit["html_url"])

    print(f"Finished processing {repo_name}.")

def main():
    """Main worker function."""
    print("Starting OSPO-ColabAchievements worker...")
    with open("ospo_config.yml", "r") as f:
        config = yaml.safe_load(f)
    
    token = os.getenv("GH_TOKEN")
    if not token:
        raise ValueError("GitHub token not found. Please set the GH_TOKEN environment variable.")

    # Start with the explicit list of repositories
    repos_to_process = config.get("repositories") or []
    
    # Add repositories from organizations
    organizations_to_process = config.get("organizations") or []
    if organizations_to_process:
        print(f"Processing {len(organizations_to_process)} organization(s)...")
        for org in organizations_to_process:
            try:
                org_repos = get_repos_from_org(org, token)
                repos_to_process.extend(org_repos)
            except Exception as e:
                print(f"Failed to fetch repos for organization {org}: {e}")

    # Remove duplicates
    repos_to_process = sorted(list(set(repos_to_process)))

    print(f"\nFound a total of {len(repos_to_process)} repositories to process.")
    for repo in repos_to_process:
        try:
            process_repository(repo, token)
        except Exception as e:
            print(f"Failed to process repository {repo}: {e}")

    print("Worker run finished.")

if __name__ == "__main__":
    main()
