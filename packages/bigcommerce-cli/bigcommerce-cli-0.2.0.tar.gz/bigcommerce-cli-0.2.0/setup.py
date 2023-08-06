# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigcommerce_cli',
 'bigcommerce_cli.delete',
 'bigcommerce_cli.get',
 'bigcommerce_cli.post',
 'bigcommerce_cli.put',
 'bigcommerce_cli.settings',
 'bigcommerce_cli.utils',
 'bigcommerce_cli.utils.bigcommerce',
 'bigcommerce_cli.utils.bigcommerce.resources']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'prettytable>=3.3.0,<4.0.0',
 'pygments>=2.13.0,<3.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['bcli = bigcommerce_cli.commands:bcli']}

setup_kwargs = {
    'name': 'bigcommerce-cli',
    'version': '0.2.0',
    'description': 'bcli is BigCommerce store management on the command line.',
    'long_description': "# BigCommerce CLI\n\n`bcli` is BigCommerce store management on the command line. It brings the most commonly used store management tools to\nthe terminal for quick actions and multi-storefront workflows. `bcli` was written to help tech savvy store managers save\ntime by ditching BigCommerce's browser based admin UI.\n\n```\n      :::::::::   ::::::::  :::        ::::::::::: \n     :+:    :+: :+:    :+: :+:            :+:      \n    +:+    +:+ +:+        +:+            +:+       \n   +#++:++#+  +#+        +#+            +#+        \n  +#+    +#+ +#+        +#+            +#+         \n #+#    #+# #+#    #+# #+#            #+#          \n#########   ########  ########## ###########       \n```\n\n# Installation\n\n[`bcli` is available on PyPI](https://pypi.org/project/bigcommerce-cli/). Use the command `pip install bigcommerce-cli`\nfor easy installation.\n\n# Getting Started\n\nUse the `bcli settings add-store` command to save a store for `bcli` to use later. Then, use\nthe `bcli settings active-store` command to select which saved store should be used for your management commands.\n\nOnce `bcli` has an active store, you can make DELETE, GET, POST, and PUT commands to manage resources on that store.\n\n# Supported Commands\n\nDelete a BigCommerce resource.\n\n- `bcli delete customers <customer id>`\n- `bcli delete products <product id>`\n- `bcli delete webhooks <webhook id>`\n\nGet a list of BigCommerce resources.\n\n- `bcli get customers`\n- `bcli get order-products <order id>`\n- `bcli get orders`\n- `bcli get product-variants <product id>`\n- `bcli get products`\n- `bcli get webhooks`\n\nGet details about a BigCommerce resource.\n\n- `bcli get customers <customer id>`\n- `bcli get order-products <order id> <order product id>`\n- `bcli get orders <order id>`\n- `bcli get product-variants <product id> <variant id>`\n- `bcli get products <product id>`\n- `bcli get webhooks <webhook id>`\n\nUpdate a BigCommerce resource.\n\n- `bcli put customers <customer id>`\n- `bcli put product-variants <product id> <variant id>`\n- `bcli put products <product id>`\n- `bcli put webhooks <webhook id>`\n\nCreate a BigCommerce resource.\n\n- `bcli post customers`\n- `bcli post products`\n- `bcli post webhooks`\n\nManage `bcli` settings.\n\n- `bcli settings delete-store`\n- `bcli settings list-stores`\n- `bcli settings add-store`\n- `bcli settings active-store`\n",
    'author': 'dhartle4',
    'author_email': 'dhartle4@uncc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dhartle4/bcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
