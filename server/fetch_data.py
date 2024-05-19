import requests
HEADERS = {"Authorization": f"token YOUR_PERSONAL_ACCESS_TOKEN"}

def fetch_repo_data(user, repo):
    url = f'https://api.github.com/repos/{user}/{repo}'
    response = requests.get(url, headers=HEADERS)
    repo_data = response.json()

    # Fetch recent pushes
    url_pushes = f'https://api.github.com/repos/{user}/{repo}/commits'
    response_pushes = requests.get(url_pushes, headers=HEADERS)
    try:
        repo_data['recent_pushes'] = response_pushes.json()[:5]
    except (TypeError, IndexError):
        repo_data['recent_pushes'] = []

    url_pulls = f'https://api.github.com/repos/{user}/{repo}/pulls'
    response_pulls = requests.get(url_pulls, headers=HEADERS)
    try:
        repo_data['waiting_merges'] = response_pulls.json()
    except (TypeError, IndexError):
        repo_data['waiting_merges'] = []

    return repo_data

def fetch_user_data(user):
    url = f'https://api.github.com/users/{user}'
    response = requests.get(url, headers=HEADERS)
    return response.json()

def fetch_user_repos(user):
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url, headers=HEADERS)
    return response.json()
