from shiny import ui


def create_info_panel(title, content):
    return ui.panel_well(ui.h3(title), ui.p(content))
