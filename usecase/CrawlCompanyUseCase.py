from util.Result import Result
from domain.Url import Url
from domain.Html import Html
from domain.Company import Company
from web_controller.http_client import HttpClient
from web_controller.company_html_mapper import CompanyHtmlMapper

class CrawlCompanyUseCase:
    log_tag: str = "CrawlCompanyUseCase"

    def __init__(self, max_limit: int = 20):
        self.max_limit: int = max_limit
        self.visited_urls: set[Url] = set()
        self.queue: list[tuple[Url, int]] = []

    def execute(self, start_url: Url) -> Result[Company]:
        print(f"{self.log_tag}| crawl start")

        self.queue.append((start_url,0))

        access_count: int = 0
        while self.queue and access_count < self.max_limit:
            access_count += 1
            print(f"{self.log_tag}| crawl count{access_count}")

            self.queue.sort(key=lambda item: item[1])

            current_url = self.queue.pop()[0]
            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            try:
                client: HttpClient = HttpClient(current_url)

                print(f"{self.log_tag}| fetch_html")
                res_html: Result[Html] = client.fetch_cleaned_html()
                if not res_html.is_success or res_html.value is None:
                    continue

                mapper: CompanyHtmlMapper = CompanyHtmlMapper(res_html.value)

                print(f"{self.log_tag}| extract_company_from_table")
                result_company: Result[Company] = mapper.extract_company_from_table()

                if not result_company.is_success:
                    print(f"{self.log_tag}| extract_company_from_dl")
                    result_company = mapper.extract_company_from_dl()

                if not result_company.is_success:
                    print(f"{self.log_tag}| extract_company_from_flexible")
                    result_company = mapper.extract_company_from_flexible()

                if not result_company.is_success:
                    print(f"{self.log_tag}| extract_company_from_bottom")
                    result_company = mapper.extract_company_from_bottom()

                if result_company.is_success and not result_company.value is None and not result_company.value.name.value == "":
                    return result_company
                
                print(f"{self.log_tag}| score_urls_high_precision")
                res_url_scores: Result[list[tuple[Url, int]]] = mapper.score_urls_high_precision(current_url)
                if not res_url_scores.is_success or res_url_scores.value is None:
                    continue

                print(f"{self.log_tag}| reserch url_scores")
                url_scores: list[tuple[Url,int]] = res_url_scores.value
                for url, score in url_scores:
                    if url not in self.visited_urls:
                        self.queue.append((url, score))
            
            except Exception as e:
                print(f"Error: {e}")
                continue
        return Result[Company].not_found()


