# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyw90', 'pyw90.lib', 'pyw90.utility']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'matplotlib>=3.4',
 'numpy>=1.20.1',
 'pandas',
 'pymatgen',
 'scipy>=1.8']

entry_points = \
{'console_scripts': ['pyw90 = pyw90.pyw90_cli:main_cli']}

setup_kwargs = {
    'name': 'pyw90',
    'version': '1.0.4',
    'description': 'A VASP and Wannier90 interfaced tool for projection analysis and fully automated dis energy window optimization.',
    'long_description': '# pyw90\n\nA `VASP` and `Wannier90` interfaced tool for projection analysis and fully automated dis energy window optimization.\n\n## Key features\n\n1. Show distribution of eigenvalues.\n2. Pre-analysis before `Wannier90` interpolation with projection and dis energy window recommendation\n3. Auto Wannier90 Fit. Using minimize method to choose the most suitable dis energy windows. \n4. Comparison. Show difference between `VASP` bands and `Wannier90` bands via plotting and report.\n\n## Installation via `pip`\n\n`pyw90` is installed using `pip` by\n\n```bash\npip install pyw90\n# update the package\npip install pyw90 --update\n```\n\nThe `pyw90` dependencies are listed as following:\n\n- python (>= 3.8, < 3.12)\n- pymatgen\n- scipy (>= 1.8)\n- numpy (>= 1.20.1)\n- python-yaml (PyYAML)\n- pandas\n- matplotlib (>=3.4)\n\n',
    'author': 'En Wang (Cloudiiink)',
    'author_email': 'wangenzj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cloudiiink/pyw90',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
