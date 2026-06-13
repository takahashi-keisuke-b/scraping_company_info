import requests
from domain.Url import Url
from domain.Html import Html
from util.Result import Result
import time
import re

class HttpClient:
    def __init__(self, base_url: Url):

        self.base_url = base_url

        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
            "Referer": "https://www.google.com/"
        }

    def fetch_html(self) -> Result[Html]:
        try:
            time.sleep(5)
            print(f"request url:{self.base_url}")
            response = self.session.get(url=self.base_url.value, headers=self.headers)

            response.raise_for_status()

            response.encoding = response.apparent_encoding
            return Result[Html].success(Html.create(url=self.base_url, raw_html= response.text))
        
        except Exception as e:
            return Result[Html].fail(f"{e}")
        
    def fetch_cleaned_html(self) -> Result[Html]:
        try:
            time.sleep(5)
            print(f"request url:{self.base_url}")
            response = self.session.get(url=self.base_url.value, headers=self.headers)

            response.raise_for_status()

            response.encoding = response.apparent_encoding

            raw_html_text = response.text
            
            cleaned_text = re.sub(r'<script.*?>.*?</script>', '', raw_html_text, flags=re.DOTALL)
            cleaned_text = re.sub(r'<style.*?>.*?</style>', '', cleaned_text, flags=re.DOTALL)

            return Result[Html].success(Html.create(url=self.base_url, raw_html= cleaned_text))
        
        except Exception as e:
            return Result[Html].fail(f"{e}")