# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gh_release_install']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<2.29']

entry_points = \
{'console_scripts': ['gh-release-install = gh_release_install.cli:run']}

setup_kwargs = {
    'name': 'gh-release-install',
    'version': '0.8.0',
    'description': 'CLI helper to install Github releases on your system.',
    'long_description': '# Github release installer\n\n[![CI](https://github.com/jooola/gh-release-install/actions/workflows/ci.yml/badge.svg)](https://github.com/jooola/gh-release-install/actions/workflows/ci.yml)\n[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/gh-release-install.svg)](https://pypi.org/project/gh-release-install/)\n[![PyPI Package Version](https://img.shields.io/pypi/v/gh-release-install.svg)](https://pypi.org/project/gh-release-install/)\n\n`gh-release-install` is a CLI helper to install Github releases on your system.\nIt can be used for pretty much anything, to install a formatter in your CI, deploy\nsome binary using an orcherstration tool, or on your desktop.\n\nThis project was mainly created to...\n\n```sh\n# ...turn this mess:\nwget --quiet --output-document=- "https://github.com/koalaman/shellcheck/releases/download/v0.7.1/shellcheck-v0.7.1.linux.x86_64.tar.xz" \\\n    | tar --extract --xz --directory=/usr/local/bin --strip-components=1 --wildcards \'shellcheck*/shellcheck\' \\\n    && chmod +x /usr/local/bin/shellcheck\n\nwget --quiet --output-document=/usr/local/bin/shfmt "https://github.com/mvdan/sh/releases/download/v3.2.1/shfmt_v3.2.1_linux_amd64"\xa0\\\n    && chmod +x /usr/local/bin/shfmt\n\n# Into this:\npip3 install gh-release-install\n\ngh-release-install \\\n      "koalaman/shellcheck" \\\n      "shellcheck-{tag}.linux.x86_64.tar.xz" --extract "shellcheck-{tag}/shellcheck" \\\n      "/usr/bin/shellcheck"\n\ngh-release-install \\\n      "mvdan/sh" \\\n      "shfmt_{tag}_linux_amd64" \\\n      "/usr/bin/shfmt"\n```\n\nFeatures:\n\n- Download releases from Github.\n- Extract zip or tarball on the fly.\n- Pin to a desired version or get the `latest` version.\n- Keep track of the local tools version using a version file.\n\n## Installation\n\nInstall the package from pip:\n\n```sh\npip install gh-release-install\ngh-release-install --help\n```\n\nOr with with pipx:\n\n```sh\npipx install gh-release-install\ngh-release-install --help\n```\n\n## Usage\n\n```sh\nusage: gh-release-install [-h] [--extract <filename>] [--version <version>]\n                          [--version-file <filename>] [-v] [-q]\n                          REPOSITORY ASSET DESTINATION\n\nInstall GitHub release file on your system.\n\npositional arguments:\n  REPOSITORY            Github REPOSITORY org/repo to get the release from.\n  ASSET                 Release ASSET filename. May contain variables such as\n                        \'{version}\' or \'{tag}\'.\n  DESTINATION           Path to save the downloaded file. If DESTINATION is a\n                        directory, the asset name will be used as filename in\n                        that directory. May contain variables such as\n                        \'{version}\' or \'{tag}\'.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --extract <filename>  Extract the <filename> from the release asset archive\n                        and install the extracted file instead. May contain\n                        variables such as \'{version}\' or \'{tag}\'. (default:\n                        None)\n  --version <version>   Desired release version to install. When using \'latest\'\n                        the installer will guess the latest version from the\n                        Github API. (default: latest)\n  --version-file <filename>\n                        Track the version installed on the system using a file.\n                        May contain variables such as \'{destination}\'. (default:\n                        None)\n  -v, --verbose         Increase the verbosity. (default: 0)\n  -q, --quiet           Disable logging. (default: None)\n\ntemplate variables:\n    {tag}               Release tag name.\n    {version}           Release tag name without leading \'v\'.\n    {destination}       DESTINATION path, including the asset filename if path\n                        is a directory.\n\nexamples:\n    gh-release-install \'mvdan/sh\' \\\n        \'shfmt_{tag}_linux_amd64\' \\\n        \'/usr/local/bin/shfmt\' \\\n        --version \'v3.3.1\'\n\n    gh-release-install \'prometheus/prometheus\' \\\n        \'prometheus-{version}.linux-amd64.tar.gz\' \\\n        --extract \'prometheus-{version}.linux-amd64/prometheus\' \\\n        \'/usr/local/bin/prometheus\' \\\n        --version-file \'{destination}.version\'\n```\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
