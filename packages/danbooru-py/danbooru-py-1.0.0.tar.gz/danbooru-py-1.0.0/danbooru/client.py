from danbooru.http import DanbooruRequest
from bs4 import BeautifulSoup
from typing import List, Dict

class Danbooru(DanbooruRequest):

  def soup(self, data):
    bs = BeautifulSoup(data, "lxml")
    posts = bs.find("div", id="posts")
    article = posts.find_all("article")
    lists = []
    for i in article:
      result = {}
      result['id'] = i.find("a")['href'].replace("/posts/", "").split("?")[0]
      result['link'] = self.base_url + i.find("a")['href']
      result['picture'] = i.find("img")['src']
      lists.append(result)
    return lists

  def get_posts(self, page : int = 1) -> List[Dict['str', 'str']]:
    """최근에 업데이트 된 사진정보를 반환합니다."""
    data = self.reqeust(f"/posts?page={page}")
    return self.soup(data)

  def get_image(self, id : str) -> str:
    """작품의 아이디를 이용해 작품의 사진을 가져옵니다."""
    data = self.reqeust(f"/posts/{id}")
    bs = BeautifulSoup(data, "lxml")

    picture = bs.find("img", id="image")['src']
    return picture

  def get_hot(self, page : int = 1) -> List[Dict['str', 'str']]:
    """인기작품을 가져옵니다."""
    data = self.reqeust(f"/posts?d=1&page=2&tags=order%3Arank")
    data = self.reqeust("/posts")
    return self.soup(data)

  def search_tag(self, tag : str, page : int = 1) -> List[Dict['str', 'str']]:
    """태그를 이용하여 작품을 검색합니다."""
    data = self.reqeust(f'/posts?page={page}&tags={tag.replace(" ", "_")}')
    return self.soup(data)