import streamlit as st
from util.Result import Result
from domain.Url import Url
from domain.Company import Company
from usecase.CrawlCompanyUseCase import CrawlCompanyUseCase
from view.streamlit_component import StreamlitComponent

def main() -> None:
    st.title("会社概要クローラー")
    st.text("企業サイトのURLを入力してください")

    raw_url: str = st.text_input(
        label="URL",
        placeholder="https://example.com",
        key="start_url_input"
    )

    if st.button("開始"):
        if not raw_url:
            st.warning("URLを入力してください")

        try:
            with st.spinner("巡回・解析中..."):
                start_url: Url = Url.create(raw_url)
                crawl_usecase: CrawlCompanyUseCase = CrawlCompanyUseCase()
                result_company: Result[Company] = crawl_usecase.execute(start_url)

            if result_company.is_success and result_company.value:
                company: Company = result_company.value
                print(f"Success| company: {company}")

                st.success("会社概要の取得に成功しました")

                ui = StreamlitComponent
                ui.display_company(company)

            else:
                print(f"Fail: not found")
                st.error("会社概要の取得に失敗、または対象のページが見つかりませんでした")
        
        except ValueError as e:
            print(f"Error: {e}")
            st.error(f"入力されたURLに不備があります")

if __name__ == "__main__":
    main()