# Tweetipy
A simple "type hinted" Python client for interacting with Twitter's API.

```
pip -m install tweetipy
```

To use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).

After that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret").

Please note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects. Also, although it is already working, please be aware that this library is still in early development phase and thus breaking changes might ocurr. In other words, don't rely on it for production just yet.

In any case, feel free to use it for your own projects. Do create issues if anything weird pops up. Pull requests and feature requests are welcome!

# Examples

### Posting a tweet
```python
from tweetipy import Tweetipy

ttpy = Tweetipy(
    oauth_consumer_key='YOUR_TWITTER_API_KEY',
    oauth_consumer_secret='YOUR_TWITTER_API_KEY_SECRET'
)

print(ttpy.tweets.write(text="Look mom, I'm using Twitter API!"))
```

### Posting a tweet with media
```python
from tweetipy import Tweetipy
from tweetipy.types import Media

ttpy = Tweetipy(
    oauth_consumer_key='YOUR_TWITTER_API_KEY',
    oauth_consumer_secret='YOUR_TWITTER_API_KEY_SECRET'
)

with open('path/to/a/very/cute/dog/pic.jpeg', 'rb') as pic:
    uploaded_media = ttpy.media.upload(
        media_bytes=pic.read(),
        media_type="image/jpeg")

print(
    ttpy.tweets.write(
        text="This tweet contains some media!",
        media=Media([uploaded_media.media_id_string])))
```
