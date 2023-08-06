import requests
from http.client import HTTPException
from pydwanimes.domain import Player


class Fireload(Player):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
            }

    def process_url(self, url: str) -> str:
        url.replace("%2F", "/")
        url.replace("%3F", "?")
        url.replace("%3D", "=")
        return f"https://{url}"

    def download(self, video_id: str, filename: str):
        """ video_id -> video_url with dw_token """
        video_dir = self.compose_video_dir(filename)
        url = self.process_url(video_id)

        res = requests.get(url, stream=True,headers=self.headers)
        print(f"REQUEST VIDEO STATUS -> {res.status_code}")
        if res.status_code == 404:
            raise HTTPException({
                "code": res.status_code,
                "message": "Cannot found video"
            })
        self.process_file(res, video_dir)
