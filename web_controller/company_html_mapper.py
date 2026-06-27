import re

from domain.Company import Company
from domain.Url import Url
from domain.SourceValue import SourceValue
from web_controller.base_html_mapper import BaseHtmlMapper
from config.Key import COMPANY_KEYWORDS, COMPANY_FIELD_KEYWORDS
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
    
    def _clean_label(self, label: str) -> str:
        if not label:
            return ""
        
        text = re.sub(r"\s+", "", label)
        
        noise_chars = ["：", ":", "【", "】", "■", "◆", "▲", "▼", "●", "★", "[", "]", "(", ")", "（", "）"]
        for char in noise_chars:
            text = text.replace(char, "")
            
        return text.strip()
    
    def _matrix_to_company(self, matrix:list[list[str]]) -> Company:
        url: Url = self.html.url
        
        extracted: dict[str, str] = {}
        
        for row in matrix:
            if len(row) < 2:
                continue
            
            label = self._clean_label(row[0])
            value = " ".join(item.strip() for item in row[1:])

            for field, keywords in COMPANY_FIELD_KEYWORDS.items():
                if any(k in label for k in keywords):
                    extracted[field] = value
                    break

        result_company: Company = Company.create(
            name=SourceValue(extracted.get("name", ""), url),
            phone=SourceValue(extracted.get("phone", ""), url),
            address=SourceValue(extracted.get("address", ""), url),
            email=SourceValue(extracted.get("email", ""), url),
            representative=SourceValue(extracted.get("representative", ""), url),
            capital=SourceValue(extracted.get("capital", ""), url),
            employees=SourceValue(extracted.get("employees", ""), url)
            )
        return result_company

    def extract_company_from_table(self) -> Result[Company]:
        matrix_result = self.table_to_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()
        matrix = matrix_result.value

        company = self._matrix_to_company(matrix)
        
        # 企業名が空白なら失敗
        if company.name.value == "":
            return Result[Company].not_found()
        
        return Result[Company].success(company)
    
    
    def extract_company_from_dl(self) -> Result[Company]:
        matrix_result = self.dl_to_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()
        matrix = matrix_result.value

        company = self._matrix_to_company(matrix)
        
        # 企業名が空白なら失敗
        if company.name.value == "":
            return Result[Company].not_found()
        
        return Result[Company].success(company)
    

    def extract_company_from_flexible(self) -> Result[Company]:
        matrix_result = self.flexible_block_to_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()
        matrix = matrix_result.value

        company = self._matrix_to_company(matrix)
        
        # 企業名が空白なら失敗
        if company.name.value == "":
            return Result[Company].not_found()
        
        return Result[Company].success(company)
    
    def extract_company_from_bottom(self) -> Result[Company]:
        matrix_result = self.bottom_up_block_to_matrix()
        if not matrix_result.is_success or not matrix_result.value:
            return Result[Company].not_found()
        matrix = matrix_result.value

        company = self._matrix_to_company(matrix)
        
        # 企業名が空白なら失敗
        if company.name.value == "":
            return Result[Company].not_found()
        
        return Result[Company].success(company)


