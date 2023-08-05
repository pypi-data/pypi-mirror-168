# Danbooru
단보루 크롤링 라이브러리

## Installation
```
$ pip install danbooru-py
```

## How to use
### 최신작품
```py
from danbooru import client

client = client.Danbooru()

print(client.get_posts())
```
### 인기작품
```py
from danbooru import client

client = client.Danbooru()

print(client.get_hot())
```
### 태그검색
```py
from danbooru import client

client = client.Danbooru()

print(client.search_tag("genshin_impact"))
```
### 이미지검색(ID)
```py
from danbooru import client

client = client.Danbooru()

print(client.get_image("5681761"))
```