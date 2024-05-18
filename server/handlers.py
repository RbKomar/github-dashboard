from shiny import render, reactive

from server.fetch_data import fetch_repo_data, fetch_user_data
from ui.components import create_info_panel
from utils.plotting import plot_repo_stats, plot_user_stats


def server(input, output, _):
    user = reactive.Value()
    repo = reactive.Value()

    @reactive.Effect
    @reactive.event(input.fetch_data)
    def _():
        user.set(input.user_name())
        repo.set(input.repo_name())

    @output
    @render.ui
    def repo_info():
        data = fetch_repo_data(user.get(), repo.get())
        return create_info_panel(f"Repository: {repo.get()}", f"""
            **Description:** {data.get('description', 'No description')}
            **Stars:** {data.get('stargazers_count', 0)}
            **Forks:** {data.get('forks_count', 0)}
            **Open Issues:** {data.get('open_issues_count', 0)}
            """)

    @output
    @render.plot
    def repo_stats():
        data = fetch_repo_data(user.get(), repo.get())
        return plot_repo_stats(data)

    @output
    @render.ui
    def user_info():
        data = fetch_user_data(user.get())
        return create_info_panel(f"User: {user.get()}", f"""
            **Name:** {data.get('name', 'No name provided')}
            **Public Repos:** {data.get('public_repos', 0)}
            **Followers:** {data.get('followers', 0)}
            **Following:** {data.get('following', 0)}
            """)

    @output
    @render.plot
    def user_stats():
        data = fetch_user_data(user.get())
        return plot_user_stats(data)
