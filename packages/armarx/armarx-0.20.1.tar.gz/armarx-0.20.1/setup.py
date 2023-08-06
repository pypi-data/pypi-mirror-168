# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armarx',
 'armarx.arviz',
 'armarx.arviz.elements',
 'armarx.arviz.grids',
 'armarx.arviz.volumetric',
 'armarx.ice_conv',
 'armarx.ice_conv.armarx_core',
 'armarx.ice_conv.robot_api',
 'armarx.math',
 'armarx.remote_gui',
 'armarx.remote_gui.widgets',
 'armarx.robots',
 'armarx.tools',
 'armarx_memory',
 'armarx_memory.aron',
 'armarx_memory.aron.aron_ice_types',
 'armarx_memory.aron.common',
 'armarx_memory.aron.conversion',
 'armarx_memory.client',
 'armarx_memory.client.detail',
 'armarx_memory.core',
 'armarx_memory.ice_conv',
 'armarx_memory.ice_conv.ArmarXCore',
 'armarx_memory.ice_conv.RobotAPI',
 'armarx_memory.segments',
 'armarx_memory.segments.human',
 'armarx_objects',
 'visionx']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0', 'numpy>=1.19.5', 'transforms3d>=0.4.1', 'zeroc-ice==3.7.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8']}

setup_kwargs = {
    'name': 'armarx',
    'version': '0.20.1',
    'description': 'A Python Toolbox for ArmarX',
    'long_description': "# Python ArmarX - A Python toolbox for ArmarX\n\n```\nfrom armarx import 🤖  as ❤ \n```\n\nThis package provides Python 3 bindings for ArmarX.\n\nIn addition, the package also includes some helper functions, such as\npublishing or subscribing to images.\n\n\n## Installation\n\n`pip install --upgrade --extra-index-url https://pypi.humanoids.kit.edu/ armarx`\n\n## Using the bindings\n\n### Connecting to an existing proxy\n\nFor proxies defined in a project's `Variants-*.xml` it is possible to import\nthe interface directly. \n\n```python\nfrom armarx import PlatformUnitInterfacePrx\nplatform_unit = PlatformUnitInterfacePrx.get_proxy('Armar6PlatformUnit')\nplatform_unit.moveTo(0.0, 0.0, 0.0, 50.0, 0.1)\n```\n\nSlice definitions can be loaded using the `slice_loader.load_armarx_slice`\nfunction. Default values for the proxy name will also be mapped.\n\nMore examples can be found in the `examples` folder.\n\n## Documentation\n\nSee `https://armarx.humanoids.kit.edu/python`\n",
    'author': 'Markus Grotz',
    'author_email': 'markus.grotz@kit.edu',
    'maintainer': 'Markus Grotz',
    'maintainer_email': 'markus.grotz@kit.edu',
    'url': 'http://gitlab.com/ArmarX/python3-armarx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.9,<4.0',
}


setup(**setup_kwargs)
