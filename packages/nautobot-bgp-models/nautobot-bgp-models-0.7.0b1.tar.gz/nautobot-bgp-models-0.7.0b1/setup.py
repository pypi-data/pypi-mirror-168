# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_bgp_models',
 'nautobot_bgp_models.api',
 'nautobot_bgp_models.migrations',
 'nautobot_bgp_models.tests']

package_data = \
{'': ['*'],
 'nautobot_bgp_models': ['templates/nautobot_bgp_models/*',
                         'templates/nautobot_bgp_models/inc/*']}

install_requires = \
['nautobot>=1.3,<2.0']

setup_kwargs = {
    'name': 'nautobot-bgp-models',
    'version': '0.7.0b1',
    'description': 'Nautobot BGP Models Plugin',
    'long_description': '# Nautobot BGP Models Plugin\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot) extending the core models with BGP-specific models.\n\nNew models enable modeling and management of BGP peerings, whether or not the peer device is present in Nautobot.\n\n> The initial development of this plugin was sponsored by Riot Games, Inc.\n\n## Data Models\n\nNavigate to [Data Models](docs/cisco_use_case.md) for detailed descriptions on additional data models provided in the plugin.\n\n## Use Cases\n\nTo make the start with the plugin easier, we provide two example use cases for common OS platforms: Cisco and Juniper.\n\n### Cisco Configuration Modeling and Rendering\n\nNavigate to [Cisco Example Use Case](docs/cisco_use_case.md) for detailed instructions how to consume BGP Models plugin on Cisco devices.\n\n### Juniper Configuration Modeling and Rendering\n\nNavigate to [Juniper Example Use Case](docs/juniper_use_case.md) for detailed instructions how to consume BGP Models plugin on Juniper devices.\n\n## Installation\n\nThe plugin is available as a Python package in PyPI and can be installed with `pip`:\n\n```shell\npip install nautobot-bgp-models\n```\n\n> The plugin is compatible with Nautobot 1.3 and higher\n\nTo ensure Nautobot BGP Models Plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-bgp-models` package:\n\n```no-highlight\n# echo nautobot-bgp-models >> local_requirements.txt\n```\n\nOnce installed, the plugin needs to be enabled in your `nautobot_config.py`\n\n```python\n# In your configuration.py\nPLUGINS = ["nautobot_bgp_models"]\n```\n\n```python\nPLUGINS_CONFIG = {\n    "nautobot_bgp_models": {\n        "default_statuses": {\n            "AutonomousSystem": ["active", "available", "planned"],\n            "Peering": ["active", "decommissioned", "deprovisioning", "offline", "planned", "provisioning"],\n        }\n    }\n}\n```\n\nIn the `default_statuses` section, you can define a list of default statuses to make available to `AutonomousSystem` and/or `Peering`. The lists must be composed of valid slugs of existing Status objects.\n\n## Screenshots\n\n![Menu](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/main-page-menu.png)\n\n![Autonomous System](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/autonomous_system_01.png)\n\n![Peering List](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/peering_list.png)\n\n![Peering](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/peering_01.png)\n\n![Peer Endpoint](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/peer_endpoint_01.png)\n\n![Peer Group](https://github.com/nautobot/nautobot-plugin-bgp-models/blob/main/docs/images/peer_group_01.png)\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nautobot/nautobot-plugin-bgp-models',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
