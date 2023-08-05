# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desktop_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'desktop-parser',
    'version': '0.1.1',
    'description': 'Parse .desktop files',
    'long_description': '# Desktop Parser\n\nThis is a parser for the [`.desktop` file format](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html). It\'s used in [Desktop Creator](https://github.com/DesktopCreatorTeam/DesktopCreator).\n\n## Installation\n\n### From pypi\n\n```bash\npip install desktop-parser\n```\n\n### From source\n\n```bash\ngit clone https://github.com/DesktopCreatorTeam/desktop-parser\ncd desktop-parser\npoetry install\n```\n\n### From the AUR\n\n```bash\nyay -S python-desktop-parser\n```\n\n## Usage\n\n```python\nfrom desktop_parser import DesktopFile\n\n# Parse a file\ndesktop_file = DesktopFile.from_file("path/to/file.desktop")\n\ndesktop_file.data["Name"] = "New Name"\ndesktop_file.data["Exec"] = "new-exec"\n\n# Save the file\ndesktop_file.save("path/to/file.desktop")\n```\n\n## Documentation\n\nThe documentation is available [here](https://desktopcreatorteam.github.io/desktop-parser/).\n\n## License\n\nThis project is licensed under the GNU GPLv3 license - see the [LICENSE.md](LICENSE.md) file for details.\n\n## Acknowledgments\n\n* [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.\n\n## Authors and Contributors\n\n* [Desktop Creator Team](https://github.com/DesktopCreatorTeam/DesktopCreator)\n    - **[0xMRTT](https://github.com/0xMRTT)**',
    'author': '0xMRTT',
    'author_email': '0xMRTT@tuta.io',
    'maintainer': '0xMRTT',
    'maintainer_email': '0xMRTT@tuta.io',
    'url': 'https://desktopcreatorteam.github.io/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
