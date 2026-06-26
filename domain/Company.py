from dataclasses import dataclass
from .Url import Url
from .SourceValue import SourceValue

@dataclass(frozen=True)
class Company:
    name: SourceValue[str, Url] = SourceValue("", Url.empty())
    phone: SourceValue[str, Url] = SourceValue("", Url.empty())
    address: SourceValue[str, Url] = SourceValue("", Url.empty())
    email: SourceValue[str, Url] = SourceValue("", Url.empty())
    representative: SourceValue[str, Url] = SourceValue("", Url.empty())
    capital: SourceValue[str, Url] = SourceValue("", Url.empty())
    employees: SourceValue[str, Url] = SourceValue("", Url.empty())
    top_url: Url = Url.empty()
    form_url: Url = Url.empty()

    @classmethod
    def create(
        cls,
        name: SourceValue[str, Url] = SourceValue("", Url.empty()),
        phone: SourceValue[str, Url] = SourceValue("", Url.empty()),
        address: SourceValue[str, Url] = SourceValue("", Url.empty()),
        email: SourceValue[str, Url] = SourceValue("", Url.empty()),
        representative: SourceValue[str, Url] = SourceValue("", Url.empty()),
        capital: SourceValue[str, Url] = SourceValue("", Url.empty()),
        employees: SourceValue[str, Url] = SourceValue("", Url.empty()),
        top_url: Url = Url.empty(),
        form_url: Url = Url.empty()
    ) -> "Company":
        return cls(
            name=name,
            phone=phone,
            address=address,
            email=email,
            representative=representative,
            capital=capital,
            employees=employees,
            top_url=top_url,
            form_url=form_url
        )