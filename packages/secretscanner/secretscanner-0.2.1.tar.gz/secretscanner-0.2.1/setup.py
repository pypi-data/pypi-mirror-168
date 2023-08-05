# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['secretscanner']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pathspec>=0.10.1,<0.11.0',
 'ppuri==0.3.1',
 'rich>=12.5.1,<13.0.0']

entry_points = \
{'console_scripts': ['secretscanner = secretscanner.__main__:run']}

setup_kwargs = {
    'name': 'secretscanner',
    'version': '0.2.1',
    'description': 'Scan for secrets within files.',
    'long_description': "# Secret Scanner\n\nA simple tool to scan directories for secrets using regular expressions.\n\n## Install\n\nInstall using either [`pip`](https://pypi.org/project/pip/), [`pipx`](https://pypi.org/project/pipx/) or your Python installer of choice\n\n```\npipx install secretscanner\n```\n\n## Usage\n\nTo scan a directory and print the files with secrets\n\n```\nsecretscanner DIRECTORY\n```\n\nTo also display info on the tokens that have been found pass the `-v`/`--verbose` flag.\n\nTo hide the output pass the `-q`/`--quiet` flag.\n\nTo output the tokens found as json pass the `-j`/`--json` flag.\n\nIf secrets are found the tool exits with exit code `1`\n\n## Output\n\nBy default files which contain secrets are either yellow when they contain secrets and dim yellow if they contain secrets but the file is ignored by git\ni.e. the only reason they're not there is because a `.gitignore` file is provided.\n\n### Default output\n\n```\nFiles with embedded secrets:\n  /secretscanner/tests/dir/github/github.txt\n  /secretscanner/tests/dir/pypi/pypi.txt\n  /secretscanner/tests/dir/digitalocean/digitalocean.txt\n```\n\n### Verbose Output\n\n```\nFiles with embedded secrets:\n  /secretscanner/tests/dir/github/github.txt\n    - Issuer: github\n      Type: pat\n      Secret: ghp_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghj\n    - Issuer: github\n      Type: oauth\n      Secret: gho_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghj\n    - Issuer: github\n      Type: user-to-server\n      Secret: ghu_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghj\n    - Issuer: github\n      Type: server-to-server\n      Secret: ghs_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghj\n    - Issuer: github\n      Type: refresh\n      Secret: ghr_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghj\n  /secretscanner/tests/dir/pypi/pypi.txt\n    - Issuer: pypi\n      Type: pat\n      Secret:\n        pypi-AgEIcHlwaS5vcmcCJGzcex4tRk1EkM_jg2KTYkrCissgG2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX\n        0AAAYgjeEtcvL8TyDUVri6iM0LTc2YzUtNDgwYy05NTA3LTlkMjBmZjY2MWY0\n  /secretscanner/tests/dir/digitalocean/digitalocean.txt\n    - Issuer: digitalocean\n      Type: pat\n      Secret:\n        dop_v1_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghjJHGHJJGJGHJGHJG76y78\n        bhjksdbahjkghj\n    - Issuer: digitalocean\n      Type: oauth\n      Secret:\n        doo_v1_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghjJHGHJJGJGHJGHJG76y78\n        bhjksdbahjkghj\n    - Issuer: digitalocean\n      Type: refresh\n      Secret:\n        dor_v1_GHJSGSJHGgjhgshjagjgasjgjhJHGHJJGJGHJGHJG76y78bhjksdbahjkghjJHGHJJGJGHJGHJG76y78\n        bhjksdbahjkghj\n```\n\n## Recognized Secrets\n\nThe tool currently recognizes the following secret types\n\n- Github access tokens\n- PyPI access tokens\n- Digital Ocean access tokens\n\n## Package Status\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/sffjunkie/secretscanner/secretscanner-test) ![PyPI - Downloads](https://img.shields.io/pypi/dm/secretscanner)\n",
    'author': 'Simon Kennedy',
    'author_email': 'sffjunkie+code@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sffjunkie/secretscanner',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
