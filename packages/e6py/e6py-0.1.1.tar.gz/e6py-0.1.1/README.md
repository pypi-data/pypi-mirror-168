# e6py

`e6py` is an API wrapper for e621/e926

## Requirements

- Python 3.10
- requests >= 2.26.0
- attrs >= 21.2.0

## Usage

```py
from e6py import E621Client

client = E621Client(login="username", api_key="API Key")
posts = client.get_posts()

for post in posts:
    print(f"Got post {post.id}")
    print(f"  Rating: {post.rating}")
    print(f"   Score: {post.score}")
    print(f"     URL: {post.file.url}")
```
