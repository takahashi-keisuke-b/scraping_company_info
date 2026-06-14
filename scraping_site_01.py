import streamlit as st
from util.Result import Result
from domain.Url import Url
from domain.Company import Company
from usecase.CrawlCompanyUseCase import CrawlCompanyUseCase

def main() -> None:
    st.title("企業情報クローラー")
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
            # ==============================
            # 
            # ==============================
            with st.spinner("巡回・解析中..."):
                start_url: Url = Url.create(raw_url)
                crawl_usecase: CrawlCompanyUseCase = CrawlCompanyUseCase()
                result_company: Result[tuple[Company,Url]] = crawl_usecase.execute(start_url)

            if result_company.is_success and result_company.value:
                company: Company = result_company.value[0]
                url: Url = result_company.value[1]
                print(f"Success| company: {company}, url:{url}")

                st.success("企業情報の取得に成功しました")

                st.text(f"url: {url.value}")
                st.markdown(f"会社名: {company.name if company.name else '未検出'}")
                st.markdown(f"電話番号: {company.phone if company.phone else '未検出'}")
                st.markdown(f"住所: {company.address if company.address else '未検出'}")
                st.markdown(f"メール: {company.email if company.email else '未検出'}")
                st.markdown(f"トップURL: {company.top_url.value if company.top_url else '未検出'}")
                st.markdown(f"問い合わせフォーム: {company.form_url.value if company.form_url else '未検出'}")
                st.markdown(f"代表者: {company.representative if company.representative else '未検出'}")
                st.markdown(f"資本金: {company.capital if company.capital else '未検出'}")
                st.markdown(f"従業員数: {company.employees if company.employees else '未検出'}")

            else:
                print(f"Fail: not found")
                st.error("情報取得に失敗、または対象のデータが見つかりませんでした")
        
        except ValueError as e:
            print(f"Error: {e}")
            st.error(f"入力されたURLに不備があります")

if __name__ == "__main__":
    main()