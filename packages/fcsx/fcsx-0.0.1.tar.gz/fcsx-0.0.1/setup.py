# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fcs']

package_data = \
{'': ['*']}

extras_require = \
{'numpy': ['numpy>=1.22.4,<2.0.0']}

setup_kwargs = {
    'name': 'fcsx',
    'version': '0.0.1',
    'description': 'FCS for Humans',
    'long_description': "# FCSX: FCS for Humans\n\nFCSX is \n\n* a very simple but fully featured Flow Cytometry Standard (FCS) reader for Python.\n* written in Python Standard Library\n\nFCSX supports to\n\n* parse FCS 2.0, 3.0, and 3.1 versions\n* create NumPy memory-mapped array for the DATA segment via installing NumPy\n\n\n\n\n## Installation\n\n```bash\npip install fcsx\n```\n\nTo support NumPy memory mapping (usually faster), please install the extra dependencies as\n\n```bash\npip install fcsx[numpy]\n```\n\n\n\n## Quick Start\n\n```python\nimport fcs\n\nf = fcs.read('./FR-FCM-ZZPH/Samusik_all.fcs')\n```\n\n\n\n## Contributing\n\n\n\n## License\n\nFCSX has an BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/fcsx/blob/main/LICENSE) file.",
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/imyizhang/fcsx/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
