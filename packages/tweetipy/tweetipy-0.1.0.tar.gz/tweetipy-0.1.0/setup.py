# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweetipy', 'tweetipy.handlers', 'tweetipy.helpers', 'tweetipy.types']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'tweetipy',
    'version': '0.1.0',
    'description': 'A simple "type hinted" Python client for interacting with Twitter\'s API.',
    'long_description': '# Tweetipy\nA simple "type hinted" Python client for interacting with Twitter\'s API.\n\nTo use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).\n\nAfter that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret"). Once that\'s done, put them in an `.env` file as follows:\n\n```\nTWITTER_API_KEY=<YOUR_TWITTER_API_KEY>\nTWITTER_API_KEY_SECRET=<YOUR_TWITTER_API_KEY_SECRET>\n```\n\nAlthough it is already working, please be aware that this is still in early development and thus breaking changes might happen. In other words, don\'t rely on it for production just yet.\n\nAlso note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects\n\nIn any case, feel free to use it for your own projects. Do create issues if anything weird pops up. PR and feature requests are welcome!\n\n# Examples\n\n### Posting a tweet\n```python\nfrom dotenv import load_dotenv\nfrom os import getenv\nfrom tweetipy import Tweetipy\n\nload_dotenv()\n\nttpy = Tweetipy(\n    oauth_consumer_key=getenv(\'TWITTER_API_KEY\'),\n    oauth_consumer_secret=getenv(\'TWITTER_API_KEY_SECRET\')\n)\n\nprint(ttpy.tweets.write(text="Hi mom, I\'m using Twitter API!"))\n```\n\n### Posting a tweet with media\n```python\nfrom dotenv import load_dotenv\nfrom os import getenv\nfrom tweetipy import Tweetipy\nfrom tweetipy.types import Media\n\nload_dotenv()\n\nttpy = Tweetipy(\n    oauth_consumer_key=getenv(\'TWITTER_API_KEY\'),\n    oauth_consumer_secret=getenv(\'TWITTER_API_KEY_SECRET\')\n)\n\nwith open(\'path/to/a/very/cute/dog/pic.jpeg\', \'rb\') as pic:\n    uploaded_media = ttpy.media.upload(\n        media_bytes=pic.read(),\n        media_type="image/jpeg")\n\nprint(\n    ttpy.tweets.write(\n        text="This tweet contains some media!",\n        media=Media([uploaded_media.media_id_string]))\n)\n```\n',
    'author': 'Olga Mirete',
    'author_email': 'olgamirete@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
