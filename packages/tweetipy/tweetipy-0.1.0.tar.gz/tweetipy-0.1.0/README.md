# Tweetipy
A simple "type hinted" Python client for interacting with Twitter's API.

To use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).

After that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret"). Once that's done, put them in an `.env` file as follows:

```
TWITTER_API_KEY=<YOUR_TWITTER_API_KEY>
TWITTER_API_KEY_SECRET=<YOUR_TWITTER_API_KEY_SECRET>
```

Although it is already working, please be aware that this is still in early development and thus breaking changes might happen. In other words, don't rely on it for production just yet.

Also note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects

In any case, feel free to use it for your own projects. Do create issues if anything weird pops up. PR and feature requests are welcome!

# Examples

### Posting a tweet
```python
from dotenv import load_dotenv
from os import getenv
from tweetipy import Tweetipy

load_dotenv()

ttpy = Tweetipy(
    oauth_consumer_key=getenv('TWITTER_API_KEY'),
    oauth_consumer_secret=getenv('TWITTER_API_KEY_SECRET')
)

print(ttpy.tweets.write(text="Hi mom, I'm using Twitter API!"))
```

### Posting a tweet with media
```python
from dotenv import load_dotenv
from os import getenv
from tweetipy import Tweetipy
from tweetipy.types import Media

load_dotenv()

ttpy = Tweetipy(
    oauth_consumer_key=getenv('TWITTER_API_KEY'),
    oauth_consumer_secret=getenv('TWITTER_API_KEY_SECRET')
)

with open('path/to/a/very/cute/dog/pic.jpeg', 'rb') as pic:
    uploaded_media = ttpy.media.upload(
        media_bytes=pic.read(),
        media_type="image/jpeg")

print(
    ttpy.tweets.write(
        text="This tweet contains some media!",
        media=Media([uploaded_media.media_id_string]))
)
```
