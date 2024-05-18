import matplotlib.pyplot as plt


def plot_repo_stats(data):
    labels = ['Stars', 'Forks', 'Open Issues']
    values = [data['stargazers_count'], data['forks_count'], data['open_issues_count']]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    return fig


def plot_user_stats(data):
    labels = ['Public Repos', 'Followers', 'Following']
    values = [data['public_repos'], data['followers'], data['following']]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    return fig
