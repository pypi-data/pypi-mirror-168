from src.icon_writer import write_icon

# write_icon("TEAMS", bgcolor=(95, 91, 204), fontcolor='white')
# write_icon("EDGE", bgcolor=(45, 248, 141), fontcolor=(2, 66, 162))
image = write_icon("VSCODE", bgcolor=(0, 102, 185), fontcolor="white")
image.save("icon.png")
