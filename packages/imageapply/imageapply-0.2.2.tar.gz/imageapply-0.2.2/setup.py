# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imageapply']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2', 'torch>=1,<2']

setup_kwargs = {
    'name': 'imageapply',
    'version': '0.2.2',
    'description': 'Simplifies the process of applying U-net style models to large images.',
    'long_description': '# Image Apply\n![test](https://github.com/PyMLTools/imageapply/actions/workflows/tests.yml/badge.svg)\n\nA package for improving the simplicity of adapting Segmentation Models to large images.\n\nThis package include a class that can be used to apply a segmentation model to large images. The class will split the image into smaller tiles, apply the model to each tile, and then stitch the tiles back together. This allows the model to be applied to images that are too large to fit in memory.\n\n## Installation\n\n```bash\npip install imageapply\n```\n\n## Usage\nThis package can be used to easily extend a segmentation model to large images. The following example is for a `model` that takes a batch of images of size (None, 256, 256, 3) as input and outputs a mask of size (None, 256, 256, 1).\n\n```python\nfrom imageapply import FlexibleModel\nmodel = FlexibleModel(model, input_size=(256, 256, 3), max_batch_size=16)\n\n# Apply the model to a batch of large images of size (20, 1024, 1024, 3)\nmasks = model(images)\n``` \n',
    'author': 'fynnsu',
    'author_email': 'fynnsu@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
