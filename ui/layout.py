from shiny import ui

app_ui = ui.page_fluid(
    ui.panel_title("GitHub Repository Dashboard"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_text("user_name", "GitHub Username", value="octocat"),
            ui.input_text("repo_name", "Repository Name", value="Hello-World"),
            ui.input_action_button("fetch_data", "Fetch Data"),
        ),
        ui.panel_main(
            ui.output_ui("repo_info"),
            ui.output_plot("repo_stats"),
            ui.output_ui("user_info"),
            ui.output_plot("user_stats")
        )
    )
)
