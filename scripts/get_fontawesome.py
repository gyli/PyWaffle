# This script generates a .py file with a dictionary of Font Awesome icon mapping, like '500px': '\uf26e'
# Run:
# python generate_fontawesome_mapping.py > fontawesome_mapping.py


import yaml
import requests
import sys


INDENT = ' ' * 4

URI = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/src/icons.yml'

CONFIG_URI = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/_config.yml'


def main(uri, config_uri):
    icons_list = yaml.load(requests.get(uri).text)['icons']

    version = yaml.load(requests.get(config_uri).text)['fontawesome']['version']

    out = sys.stdout
    out.write("# The content is licensed under the SIL OFL 1.1: http://scripts.sil.org/OFL\n")
    out.write('# Fontawesome version {0}\n'.format(version))
    out.write('\n')
    out.write('icons = {\n')
    list(map(lambda x: out.write("{0}'{1}': '\\u{2}',\n".format(INDENT, x['id'], x['unicode'])), icons_list))
    out.write('}\n')


if __name__ == '__main__':
    main(URI, CONFIG_URI)
