# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e6py', 'e6py.http', 'e6py.http.endpoints', 'e6py.models', 'e6py.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0', 'requests>=2.28.1,<3.0.0', 'sentinel>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'e6py',
    'version': '0.1.1',
    'description': 'An e621 API wrapper',
    'long_description': '# e6py\n\n`e6py` is an API wrapper for e621/e926\n\n## Requirements\n\n- Python 3.10\n- requests >= 2.26.0\n- attrs >= 21.2.0\n\n## Usage\n\n```py\nfrom e6py import E621Client\n\nclient = E621Client(login="username", api_key="API Key")\nposts = client.get_posts()\n\nfor post in posts:\n    print(f"Got post {post.id}")\n    print(f"  Rating: {post.rating}")\n    print(f"   Score: {post.score}")\n    print(f"     URL: {post.file.url}")\n```\n',
    'author': 'zevaryx',
    'author_email': 'zevaryx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
