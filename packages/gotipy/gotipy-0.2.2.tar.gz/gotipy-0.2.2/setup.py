# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gotipy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'gotipy',
    'version': '0.2.2',
    'description': 'A simple Python wrapper for Gotify',
    'long_description': "## Gotipy\n\nA simple Python wrapper for [Gotify](https://github.com/gotify/server)\n\n## Requirements\n- [python>=3.6](https://www.python.org/downloads/)\n- [gotify/server](https://gotify.net/docs/install)\n\n\n## Installation\n\n```sh\npip install gotipy\n```\n\n## Usage\n\n```py\nfrom gotipy import Gotify\n\ng = Gotify(host_address='https://yourdomain.com')\n```\n\n### Create a new application\n\n```py\ng.create_app(admin_username='admin',\n             admin_password='admin',\n             app_name='demo',\n             desc='My first app!')\n# {\n#     'id': 1,\n#     'token': 'xxxxxxxxxx',\n#     'name': 'demo',\n#     'description': 'My first app!',\n#     'internal': False,\n#     'image': 'static/defaultapp.png'\n# }\n```\n\n### Push messages to an application\n\n```py\ng.push(title='My message',\n       message='Hello, World!',\n       priority=9,\n       token='xxxxxxxxxx')\n# {\n#     'id': 1,\n#     'appid': 1,\n#     'message': 'Hello, World!',\n#     'title': 'My message',\n#     'priority': 9,\n#     'date': '2022-05-16T05:25:29.367216435Z'\n# }\n```\n\n\n### Notes:\n\n- You can set `GOTIFY_HOST_ADDRESS` as an envionmnt variable instead of passing `host_address` to the class instance.\n- If you want to use the same app in all your `push` calls, you can omit `token` from the method, and pass `fixed_token=...` to the class instance or set `GOTIFY_APP_TOKEN` as an envionmnt variable instead.\n- If you want to set a fixed priority level for all your `push` calls, pass `fixed_priority` to the class instance.\n",
    'author': 'Mohammad Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
