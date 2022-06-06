# This script generates Font Awesome icon mapping file pywaffle/fontawesome_mapping.py
# To run it:
# python3 scripts/fontawesome_mapping_generator.py

# The font files in folder font need to be updated manually when updating FontAwesome

import inspect
import json
import pathlib
import subprocess
import sys
from collections import defaultdict

import fontawesomefree

INDENT = " " * 4


def main():
    # Check installed Font Awesome version with pip
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "fontawesomefree"],
        stdout=subprocess.PIPE,
        text=True,
    )
    pip_show = result.stdout
    fa_pip_version = pip_show.split("\n")[1].lstrip("Version: ")

    # Check Font Awesome version in requirements.txt
    # When upgrading FA, change the version number in requirements.txt, requirements_dev.txt, and setup.py
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("fontawesomefree"):
                break
    fa_req_version = line.strip("\n").split("==")[1]

    # Upgrade FA in pip first before generating the mapping
    if fa_req_version != fa_pip_version:
        raise ValueError(
            f"Font Awesome version conflict. In pip: v{fa_pip_version}, in requirements: v{fa_req_version}."
        )

    # Get font meta data from the package
    package_path = pathlib.Path(inspect.getsourcefile(fontawesomefree))
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

    with open("pywaffle/fontawesome_mapping.py", "w") as file:
        file.write("# For Font Awesome version: {0}\n".format(fa_req_version))
        file.write("\n")
        file.write("icons = ")
        file.write(json.dumps(mapping, indent=4))
        file.write("\n")


if __name__ == "__main__":
    main()
