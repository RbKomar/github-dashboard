from shiny import ui


def create_info_panel(title, content):
    return ui.panel_well(ui.h3(title), ui.markdown(content))


def create_clickable_list(items, input_id):
    return ui.tags.ul(
        *[ui.tags.li(ui.a(item, href="#", onclick=f"Shiny.setInputValue('{input_id}', '{item}')")) for item in items])
