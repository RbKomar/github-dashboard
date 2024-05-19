import textwrap

import plotly.graph_objects as go


def plot_repo_stats(data):
    labels = ['Stars', 'Forks', 'Open Issues']
    values = [data['stargazers_count'], data['forks_count'], data['open_issues_count']]

    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title='Repository Statistics', xaxis_title='Metric', yaxis_title='Count')
    return fig


def plot_user_stats(data):
    labels = ['Public Repos', 'Followers', 'Following']
    values = [data['public_repos'], data['followers'], data['following']]

    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title='User Statistics', xaxis_title='Metric', yaxis_title='Count')
    return fig


def plot_user_repos(repos):
    repos_sorted = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)
    repo_names = [textwrap.shorten(repo['name'], width=30, placeholder="...") for repo in repos_sorted]
    stars = [repo['stargazers_count'] for repo in repos_sorted]

    fig = go.Figure(data=[go.Bar(y=repo_names, x=stars, orientation='h')])
    fig.update_layout(title='Repositories and Stars', xaxis_title='Stars', yaxis_title='Repositories')
    return fig
