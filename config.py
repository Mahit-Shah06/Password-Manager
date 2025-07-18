import json

height = 650
width = 1150

text_font = ("Consolas", 11)
button_font = ("Seoge UI", 10, "bold")
title_font = ("Segoe UI", 32, "bold")

with open("themes.json", "r") as file:
    themes = json.load(file)

selected_theme = "dark"

theme = themes[selected_theme]

bgcolor = theme["bgcolor"]
bdcolor = theme["bdcolor"]
font_color = theme["font_color"]
button_bg = theme["button_bg"]
button_fg = theme["button_fg"]
hover_bg = theme["hover_bg"]
title_color = theme["title_color"]
