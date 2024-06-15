import requests
import json
from collections import Counter



POSTS_URL = 'https://jsonplaceholder.typicode.com/posts'
COMMENTS_URL = 'https://jsonplaceholder.typicode.com/comments'


def get_posts(url: str, **kw):
    return requests.get(url).json()


def get_comments(url: str, **kw):
    return requests.get(url).json()


def main():
    comments = get_comments(COMMENTS_URL)
    c = Counter([x.get('postId') for x in comments])
    result = {}
    posts = get_posts(POSTS_URL)
    for post in posts:
        result[post['userId']] = result.get(post['userId'], 0) + c.get(post.get('id')) 
    posts_per_user = Counter([x.get('userId') for x in posts])
    for k, v in posts_per_user.items():
        result[k] = result.get(k) / v
    print(result)


if __name__ == '__main__':
    main()


