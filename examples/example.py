from dirtree_chart import diagram
from dirtree_chart import config

# Add files or folders to ignore list
ignore_list = config.ignore_list.copy()
ignore_list.extend([".secrets", "ect.f", "vendor", "libs", "Vendor", "Editor"])

# Create diagram
diagram.DirStrucTree(ignore = ignore_list)


