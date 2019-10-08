# This script generates Font Awesome icon mapping file pywaffle/fontawesome_mapping.py
# To run it:
# python3 scripts/get_fontawesome.py

# The font files in folder font need to be updated manually when updating FontAwesome

import json
import requests

INDENT = " " * 4
VERSION = "5.5.0"
URI = "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/advanced-options/metadata/icons.json"


def main():
    icons = json.loads(requests.get(URI).text)

    # Group icons by style
    mapping = {}
    for k, v in icons.items():
        for style in v["styles"]:
            style_name = style.upper()
            if style_name not in mapping.keys():
                mapping[style_name] = {}
            mapping[style_name][k] = chr(int(v["unicode"], 16))

    with open("pywaffle/fontawesome_mapping.py", "w") as file:
        file.write("# This file belongs to Font Awesome, see license https://fontawesome.com/license/\n")
        file.write("# Font Awesome version: {0}\n".format(VERSION))
        file.write("\n")
        file.write("icons = ")
        file.write(json.dumps(mapping, indent=4))
        file.write("\n")


if __name__ == "__main__":
    main()
