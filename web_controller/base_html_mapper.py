from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin
from typing import cast
from util.Result import Result
from domain.Html import Html
from domain.Url import Url

class BaseHtmlMapper:
    def __init__(self, html: Html):
        self.html = html
        self.soup = BeautifulSoup(html.value, "html.parser")
    
    def collect_all_href_with_text(self) -> Result[list[tuple[str,str]]]:
        discovered_href: list[tuple[str,str]] = []

        for a_tag in self.soup.find_all("a"):
            href = a_tag.get("href")
            if not href:
                continue

            if (
                href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("#")
            ):
                continue

            link_text = a_tag.get_text(strip=True)

            if href not in discovered_href or link_text:
                discovered_href.append((link_text,href))

        return Result[list[tuple[str,str]]].success(discovered_href)
    
    def collect_all_url_with_text(self, base_url: Url) -> Result[list[tuple[str,Url]]]:
        base_domain = base_url.netloc
        discovered_urls: list[tuple[str,Url]] = []

        href_pairs = self.collect_all_href_with_text().value or []

        for item in href_pairs:
            text = item[0]
            href = item[1]

            if (
                href.startswith("http://")
                or href.startswith("https://")
            ):
                discovered_urls.append((text, Url.create(href)))
            else:
                full_url = urljoin(base_url.value, href)
                parsed_url = urlparse(full_url)

                if parsed_url.netloc == base_domain:
                    discovered_urls.append((text, Url.create(full_url)))
        return Result[list[tuple[str,Url]]].success(discovered_urls)
    
    def collect_same_domain_url_with_text(self, base_url: Url) -> Result[list[tuple[str,Url]]]:
        base_domain = base_url.netloc
        discovered_urls: list[tuple[str,Url]] = []

        href_pairs = self.collect_all_href_with_text().value or []

        for item in href_pairs:
            text = item[0]
            href = item[1]

            full_url = urljoin(base_url.value, href)
            parsed_url = urlparse(full_url)

            if parsed_url.netloc == base_domain:
                discovered_urls.append((text, Url.create(full_url)))
        return Result[list[tuple[str,Url]]].success(discovered_urls)

    def table_to_matrix(self) -> Result[list[list[str]]]:
        matrix: list[list[str]] = []

        table = self.soup.find("table")
        if not table or not isinstance(table, Tag):
            return Result[list[list[str]]].not_found()
        
        for row_element in table.find_all("tr"):
            row: Tag = cast(Tag, row_element)

            row_data: list[str] = []

            for cell_element in row.find_all(["th", "td"]):
                cell: Tag = cast(Tag, cell_element)

                row_data.append(cell.get_text(strip=True))

            if row_data:
                matrix.append(row_data)

        return Result[list[list[str]]].success(matrix)
    
    def table_to_limit_matrix(self, max_num: int = 20) -> Result[list[list[str]]]:
        matrix: list[list[str]] = []

        table = self.soup.find("table")
        if not table or not isinstance(table, Tag):
            return Result[list[list[str]]].not_found()
        
        count: int = 0
        for row_element in table.find_all("tr"):
            row: Tag = cast(Tag, row_element)
            if count > max_num:
                break
            else:
                count += 1
        

            row_data: list[str] = []

            for cell_element in row.find_all(["th", "td"]):
                cell: Tag = cast(Tag, cell_element)

                row_data.append(cell.get_text(strip=True))

            if row_data:
                matrix.append(row_data)

        return Result[list[list[str]]].success(matrix)

    def dl_to_matrix(self) -> Result[list[list[str]]]:
        matrix: list[list[str]] = []

        dl_tags = self.soup.find_all("dl")
        if not dl_tags:
            return Result[list[list[str]]].not_found()

        for dl_tag in dl_tags:
            current_label = ""
            
            for child in dl_tag.find_all(["dt", "dd"]):
                tag_name = child.name
                text_content = child.get_text(strip=True)

                if tag_name == "dt":
                    current_label = text_content
                    
                elif tag_name == "dd":
                    if current_label:
                        matrix.append([current_label, text_content])

        if not matrix:
            return Result[list[list[str]]].not_found()

        return Result[list[list[str]]].success(matrix)
    
    def flexible_block_to_matrix(self) -> Result[list[list[str]]]:
        matrix: list[list[str]] = []

        for element in self.soup.find_all(["div", "p", "li"]):
            if not isinstance(element, Tag):
                continue

            children_texts = [
                child.get_text(strip=True).replace("：", "").replace(":", "").strip()
                for child in element.children 
                if child.get_text(strip=True)
            ]

            if len(children_texts) >= 2:
                if children_texts not in matrix:
                    matrix.append(children_texts)
        
        if not matrix:
            return Result[list[list[str]]].not_found()
        
        return Result[list[list[str]]].success(matrix)


    def bottom_up_block_to_matrix(self) -> Result[list[list[str]]]:
        matrix: list[list[str]] = []
        target_tags = ["div", "li", "p"]
        
        for element in self.soup.find_all(target_tags):
            if not isinstance(element, Tag):
                continue

            has_inner_target = any(
                isinstance(child, Tag) and child.name in target_tags 
                for child in element.children
            )
            
            if has_inner_target:
                is_first_converge_point = True
                for child in element.children:
                    if isinstance(child, Tag) and child.name in target_tags:
                        child_strings = [s.strip() for s in child.stripped_strings if s.strip()]
                        if len(child_strings) >= 2:
                            is_first_converge_point = False
                            break
                
                if not is_first_converge_point:
                    continue

            strings = [
                s.replace("：", "").replace(":", "").strip() 
                for s in element.stripped_strings 
                if s.strip()
            ]

            if len(strings) >= 2:
                if strings not in matrix:
                    matrix.append(strings)

        if not matrix:
            return Result[list[list[str]]].not_found()

        return Result[list[list[str]]].success(matrix)

