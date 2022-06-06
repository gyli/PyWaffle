# This script generates Font Awesome icon mapping file pywaffle/fontawesome_mapping.py
# It's called in setup.py, and it runs as post-install command

import inspect
import json
from collections import defaultdict
from pathlib import Path

import fontawesomefree

INDENT = " " * 4
FONTAWESOME_PACKAGE_NAME = "fontawesomefree"


def main():
    # Get font meta data from the package
    package_path = Path(inspect.getsourcefile(fontawesomefree))
    icons_json_path = (
        package_path.parent / "static/fontawesomefree/metadata" / "icons.json"
    )
    with open(icons_json_path, "r") as f:
        icons = json.load(f)

    # Group icons by style
    mapping = defaultdict(dict)
    for font_name, font_meta in icons.items():
        for style in font_meta["styles"]:
            mapping[style][font_name] = chr(int(font_meta["unicode"], 16))

            for alias in font_meta.get("aliases", {}).get("names", []):
                if alias in mapping[style].keys():
                    print(f"Font {alias} existed. This mapping might contain issues!")
                mapping[style][alias] = chr(int(font_meta["unicode"], 16))

    with open(
        Path(__file__).parent.parent.absolute() / "pywaffle/fontawesome_mapping.py", "w"
    ) as file:
        file.write("# For Font Awesome version: {0}\n".format(fa_req_version))
        file.write("\n")
        file.write("icons = ")
        file.write(json.dumps(mapping, indent=4))
        file.write("\n")


if __name__ == "__main__":
    main()
