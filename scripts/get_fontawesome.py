# This script generates a .py file with a dictionary of Font Awesome icon mapping, like '500px': '\uf26e'
# Run:
# python3 scripts/get_fontawesome.py > pywaffle/fontawesome_mapping.py

# The font files in folder font need to be updated manually when updating FontAwesome


import json
import requests
import sys


INDENT = ' ' * 4
VERSION = '5.5.0'
URI = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/advanced-options/metadata/icons.json'


def main(uri):

    icons = json.loads(requests.get(uri).text)

    out = sys.stdout
    out.write("# This file belongs to Font Awesome, see license http://fontawesome.io/license/\n")
    out.write('# Font Awesome version: {0}\n'.format(VERSION))
    out.write('\n')
    out.write('icons = {\n')
    list(map(lambda x: out.write("{0}'{1}': '\\u{2}',\n".format(INDENT, x[0], x[1]['unicode'])), icons.items()))
    out.write('}\n')


if __name__ == '__main__':
    main(URI)
