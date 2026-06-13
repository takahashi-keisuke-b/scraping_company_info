from dataclasses import dataclass
from .Url import Url

@dataclass(frozen=True)
class Company:
    name: str = ""
    phone: str = ""
    address: str = ""
    email: str = ""
    top_url: Url = Url.empty()
    form_url: Url = Url.empty()
    representative: str = ""
    capital: str = ""
    employees: str = ""

    @classmethod
    def create(
        cls,
        name: str = "",
        phone: str = "",
        address: str = "",
        email: str = "",
        top_url: Url = Url.empty(),
        form_url: Url = Url.empty(),
        representative: str = "",
        capital: str = "",
        employees: str = "",
    ) -> "Company":
        return cls(
            name=name,
            phone=phone,
            address=address,
            email=email,
            top_url=top_url,
            form_url=form_url,
            representative=representative,
            capital=capital,
            employees=employees
        )