# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffusions',
 'diffusions.losses',
 'diffusions.lr_schedulers',
 'diffusions.models',
 'diffusions.models.imagen',
 'diffusions.pipelines',
 'diffusions.schedulers',
 'diffusions.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'einops>=0.4.1,<0.5.0',
 'numpy>=1.21.0',
 'torch>=1.12.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'diffusions',
    'version': '0.1.12',
    'description': 'Diffusion models',
    'long_description': '# diffusions\nDiffusion models\n\n# TODO\n\n- [x] Memory Efficient Attention\n  - [Paper](https://arxiv.org/abs/2112.05682)\n- [x] Focal Frequency Loss\n  - [Code](https://github.com/EndlessSora/focal-frequency-loss)\n  - [Paper](https://arxiv.org/abs/2012.12821)\n  - [Homepage](https://www.mmlab-ntu.com/project/ffl/index.html)',
    'author': 'yuta0306',
    'author_email': 'yuta20010306@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yuta0306/diffusions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
