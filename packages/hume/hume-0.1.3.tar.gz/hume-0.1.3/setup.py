# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hume', 'hume._batch', 'hume._common', 'hume._common.config']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'hume',
    'version': '0.1.3',
    'description': 'Hume AI Python Client',
    'long_description': "# Hume AI Python SDK\n\nThe Hume AI Python SDK makes it easy to call Hume APIs from Python applications.\n\nTo get started, [sign up for a Hume account](https://beta.hume.ai/sign-up)!\n\n## Usage & Documentation\n\nFor usage examples check out the [full documentation](https://humeai.github.io/hume-python-sdk/).\n\n## Other Resources\n\n- [Hume AI Homepage](https://hume.ai)\n- [Platform Documentation](https://help.hume.ai/basics/about-hume-ai)\n- [API Reference](https://docs.hume.ai)\n\n## Support\n\nIf you've found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!\n",
    'author': 'Hume AI Dev',
    'author_email': 'dev@hume.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HumeAI/hume-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
