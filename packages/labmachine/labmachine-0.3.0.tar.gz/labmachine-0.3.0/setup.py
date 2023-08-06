# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labmachine',
 'labmachine.io',
 'labmachine.providers.cloudflare',
 'labmachine.providers.google',
 'labmachine.providers.local']

package_data = \
{'': ['*'], 'labmachine': ['files/*']}

install_requires = \
['apache-libcloud>=3.6.0,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'cryptography>=37.0.4,<38.0.0',
 'nanoid>=2.0.0,<3.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0']

extras_require = \
{'gcs': ['smart-open>=6.0.0,<7.0.0', 'google-cloud-storage>=1.31.0,<2.0.0']}

entry_points = \
{'console_scripts': ['jupctl = labmachine.cli:cli']}

setup_kwargs = {
    'name': 'labmachine',
    'version': '0.3.0',
    'description': 'A simple creator of machines with Jupyterlab',
    'long_description': '# labmachine\n\nThis is a POC with two purposes: refactoring a cluster package from [labfunctions](github.com/labfunctions/labfunctions) and allowing the creation and self registering of a jupyter instance.\n\nThis work was inpired by [Let Deep Learning VMs and Jupyter notebooks burn the midnight oil for you](https://cloud.google.com/blog/products/ai-machine-learning/let-deep-learning-vms-and-jupyter-notebooks-to-burn-the-midnight-oil-for-you-robust-and-automated-training-with-papermill)\n\nRight now only works for Google Cloud but should be easy to expand to other providers. \n\n\nFor examples, see [examples](examples/)\n\nSee `infra_[cpu|gpu].py` and `lab_[cpu|gpu].py`\n\n`infra_*` files are raw implementacion of the cluster library.\n\nLab files are abstractions built over this library for jupyter lab provisioning.\n\n## Features\n\n- VM creation (Google)\n- Jupyter on docker\n- SSL certificates (ZeroSSL & Caddy)\n- Volumes managments (Creation, Resizing, deletion, formating, etc)\n- DNS A record creation (Google, Cloudflare)\n- Automatic shutdown by inactivity (by Jupyter)\n- GPU Provisioning (nvidia-smi installation, docker configuration, etc)\n- Linux image creation (Packer)\n- Entities types for autocompletion\n\n# Documentation\n\n- [Quickstart](docs/quickstart.md)\n- [Permissions](docs/permissions.md)\n\n\n## Next work\n\nSee https://trello.com/b/F2Smw3QO/labmachine\n\n',
    'author': 'nuxion',
    'author_email': 'nuxion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nuxion/labmachine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
