# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_codeartifact_plugin']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.57,<2.0.0', 'poetry>=1.2.1,<2.0.0']

entry_points = \
{'poetry.plugin': ['poetry-codeartifact-plugin = '
                   'poetry_codeartifact_plugin.plugin:CodeArtifactPlugin']}

setup_kwargs = {
    'name': 'poetry-codeartifact-plugin',
    'version': '1.0.0',
    'description': 'A poetry plugin for keeping your CodeArtifact authorization token up-to-date',
    'long_description': '# poetry-codeartifact-plugin\n\nThis Poetry plugin automatically refreshes your authorization token when working with CodeArtifact repositories.\n\n## Installation\n\nRun this to install the plugin:\n`poetry self add poetry-codeartifact-plugin`\n\nAnd to remove:\n`poetry self remove poetry-codeartifact-plugin`\n\n## Usage\n\nNo configuration or workflow changes are needed. If the plugin detects a HTTP 401 or 403 from a CodeArtifact URL, it will refresh your authorization token and retry the request.\n\nThis assumes that your local AWS creds are up-to-date -- if not, your command will still fail.\n\n\n## Adding a CodeArtifact repository\n\nAdd this snippet to your project\'s `pyproject.toml`:\n\n```toml\n[[tool.poetry.source]]\nname = "codeartifact-pypi"  # arbitrary, just don\'t reuse repository names between CodeArtifact repos\nurl = "https://DOMAIN-123412341234.d.codeartifact.us-west-2.amazonaws.com/REPO/pypi/simple/"  # get this URL from your CodeArtifact dashboard or the GetRepositoryEndpoint API call\n```\n\nLearn more about Poetry repositories here: https://python-poetry.org/docs/repositories/',
    'author': 'Tom Petr',
    'author_email': 'tom@r2c.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
