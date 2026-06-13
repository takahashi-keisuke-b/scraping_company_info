from domain.Company import Company
from domain.Url import Url
from web_controller.base_html_mapper import BaseHtmlMapper
from config.Company_Key import COMPANY_KEYWORDS, COMPANY_FIELD_KEYWORDS
from urllib.parse import urlparse
from util.Result import Result

class CompanyHtmlMapper(BaseHtmlMapper):
    
    def score_urls_high_precision(self, base_url: Url) -> Result[list[tuple[Url, int]]]:
        links = self.collect_same_domain_url_with_text(base_url).value or []
        if not links:
            return Result[list[tuple[Url, int]]].not_found()

        url_scores_dict: dict[Url, int] = {}

        for item in links:
            text = item[0]
            url = item[1]
            
            url_lower = url.value.lower()

            n = 0
            if any(k in text.lower() for k in COMPANY_KEYWORDS):
                n = 25
            else:
                n = 5

            parsed_url = urlparse(url.value)
            path_parts = [p for p in parsed_url.path.split("/") if p]
            weight_sum = 0.0

            for index, part in enumerate(path_parts):
                layer = index + 1
                part_lower = part.lower()

                for keyword in COMPANY_KEYWORDS:
                    if keyword in part_lower:
                        weight_sum += 2 ** (1-layer)
            
            score = int(n * weight_sum)

            if url_lower.endswith((".pdf", ".jpg", ".jpeg", ".png", ".gif", ".zip")):
                score = -1

            if url not in url_scores_dict or score > url_scores_dict[url]:
                url_scores_dict[url] = score

        url_scores_list = list(url_scores_dict.items())
        return Result[list[tuple[Url, int]]].success(url_scores_list)
    
    def extract_company_from_table(self) -> Result[Company]:
        matrix_result = self.table_to_limit_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()

        matrix = matrix_result.value

        extracted: dict[str, str] = {}

        for row in matrix:
            if len(row) < 2:
                continue
            
            label = row[0].strip()
            value = row[1].strip()

            for field, keywords in COMPANY_FIELD_KEYWORDS.items():
                if any(k in label for k in keywords):
                    extracted[field] = value
                    break

        if not extracted.get("name"):
            return Result[Company].not_found()

        result_company: Company = Company.create(
            name=extracted.get("name", ""),
            phone=extracted.get("phone", ""),
            email=extracted.get("email", ""),
            address=extracted.get("address", ""),
            representative=extracted.get("representative",""),
            capital=extracted.get("capital",""),
            employees=extracted.get("employees",""),
            )

        return Result[Company].success(result_company)
    
    def extract_company_from_dl(self) -> Result[Company]:
        matrix_result = self.dl_to_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()

        matrix = matrix_result.value

        extracted: dict[str, str] = {}

        for row in matrix:
            if len(row) < 2:
                continue
            
            label = row[0].strip()
            value = row[1].strip()

            for field, keywords in COMPANY_FIELD_KEYWORDS.items():
                if any(k in label for k in keywords):
                    extracted[field] = value
                    break

        if not extracted.get("name"):
            return Result[Company].not_found()

        result_company: Company = Company.create(
            name=extracted.get("name", ""),
            phone=extracted.get("phone", ""),
            email=extracted.get("email", ""),
            address=extracted.get("address", ""),
            representative=extracted.get("representative",""),
            capital=extracted.get("capital",""),
            employees=extracted.get("employees",""),
            )

        return Result[Company].success(result_company)


