import requests
from danbooru.error import HTTPException

class DanbooruRequest:
  base_url = "https://danbooru.donmai.us"

  def reqeust(self, endpoint : str):
    url = self.base_url + endpoint
    re = requests.get(url)
    if re.status_code == 200:
      return re.text
    else:
      raise HTTPException("검색결과가 없습니다")