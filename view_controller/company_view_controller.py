# view_control/company_view_control.py
from typing import Optional
from domain.Company import Company
from domain.Url import Url
from usecase.CrawlCompanyUseCase import CrawlCompanyUseCase

class CompanyViewControl:
    def __init__(self, crawl_usecase: CrawlCompanyUseCase):
        self._crawl_usecase = crawl_usecase

    def handle_search(self, raw_url: str) -> Optional[Company]:
        if not raw_url.strip():
            return None
            
        start_url = Url.create(raw_url)
        
        result = self._crawl_usecase.execute(start_url)
        
        if result.is_success:
            return result.value
        else:
            return None