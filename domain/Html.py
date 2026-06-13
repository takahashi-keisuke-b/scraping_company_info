# domain/Html.py
from dataclasses import dataclass
from domain.Url import Url

@dataclass(frozen=True)
class Html:
    url: Url
    value: str

    @classmethod
    def create(cls, url: Url, raw_html: str) -> "Html":
        if not raw_html or not raw_html.strip():
            raise ValueError(f"不正なHTML: {raw_html}")
        
        return cls(url=url, value=raw_html.strip())