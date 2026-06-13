from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class Url:
    
    value: str
    scheme: str # http or https
    netloc: str # example.com
    path: str   # /company/about

    @classmethod
    def create(cls, raw_url: str) -> "Url":
        clean_url = raw_url.strip()
        parsed = urlparse(clean_url)
        
        if parsed.scheme not in ["http", "https"] or not parsed.netloc:
            raise ValueError(f"不正なURL形式です: {raw_url}")
            
        return cls(
            value=clean_url,
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            path=parsed.path
        )

    @classmethod
    def empty(cls) -> "Url":
        return cls(value="", scheme="", netloc="", path="")

    def is_same_domain(self, other: "Url") -> bool:
        return self.netloc == other.netloc