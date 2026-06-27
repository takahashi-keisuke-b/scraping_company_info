# view/streamlit_component.py
import streamlit as st
import streamlit.components.v1 as stc
from domain.Url import Url
from domain.Company import Company

class StreamlitComponent:

    @staticmethod
    def display_source_value(label: str, value: str, source: Url) -> None:
        if value == "" or source is Url.empty():
            return

        col_text, col_btn = st.columns([0.85, 0.15])

        with col_text:
            st.markdown(f"**{label}**:   [{value}]({source.value})")

        with col_btn:
            html_copy_button = f"""
            <button onclick="navigator.clipboard.writeText('{value}')">
                copy
            </button>
            """
            stc.html(html_copy_button, height=50)
        st.write("---")

    @staticmethod
    def display_company(company: Company) -> None:
        StreamlitComponent.display_source_value("企業名", company.name.value, company.name.source)
        StreamlitComponent.display_source_value("電話番号", company.phone.value, company.phone.source)
        StreamlitComponent.display_source_value("住所", company.address.value, company.address.source)
        StreamlitComponent.display_source_value("メールアドレス", company.email.value, company.email.source)
        StreamlitComponent.display_source_value("代表者", company.representative.value, company.representative.source)
        StreamlitComponent.display_source_value("資本金", company.capital.value, company.capital.source)
        StreamlitComponent.display_source_value("従業員数", company.employees.value, company.employees.source)


        




