from pathlib import Path
from basemodels.experience.data import (
    Employment,
    Personal,
    Language,
    PersonalAssess,
    Education,
)
from basemodels.employmenthistory import EmploymentHistory
from basemodels.id import ID, IDs
from typing import List, Optional
from basemodels.commonmodel import CommonModel, BuilderModel
from basemodels.phone import Phone, Phones
from basemodels.address import Address, Addresses
from pydantic import BaseModel


class PersonId(ID):
    pass


DATADIR = Path(__file__).parents[2] / "data"


class ExperienceModel(BaseModel, BuilderModel):
    personal: Personal
    phone: List[Phone]
    personalassess: PersonalAssess
    education: List[Education]
    language: Optional[List[Language]]
    employment: Optional[List[Employment]]
    address: List[Address]
    personid: List[PersonId]
    companies: List[str] = []

    def get_companies(self):
        try:
            company_set = set(
                [emp.company for emp in self.employment if emp.employment_certificate]
            )
        except KeyError as err:
            raise ValueError(
                f'key error in employment sheet. Please check "company","employment","employment_certificate"'
            )
        # pick a company for employment certificate generation
        self.companies = list(company_set)
        return [company for index, company in enumerate(self.companies)]

    def context(self, company=""):

        # company = self.companies[int(which_one)]
        # get validated data
        m_ec = []
        is_current = False
        works = [emp for emp in self.employment if emp.company == company]

        for i, employment in enumerate(works):
            if not employment.end_date:
                is_current = True
            m_ec.append(employment)
        # get summary info
        history = EmploymentHistory(m_ec)
        start_date = history.initial_start_date
        end_date = history.final_end_date
        position_number = history.position_number_say
        ids = IDs(self.personid)

        # get company brief, and hr rep's information from the list of positions in one company. The rep info could be in any period, but only get one of them.
        def getContent(field):
            for w in m_ec:
                value = getattr(w, field)
                if value:
                    return value
            return None

        context = {
            # 'company_brief':company_brief,
            "company_brief": getContent("company_brief"),
            "hr_rep_name": getContent("fullname_of_certificate_provider"),
            "hr_rep_position": getContent("position_of_certificate_provider"),
            "hr_rep_department": getContent("department_of_certificate_provider"),
            "hr_rep_phone": getContent("phone_of_certificate_provider"),
            "hr_rep_email": getContent("email_of_certificate_provider"),
            "passport": ids.passport.number,
            "work": m_ec,
            "personal": self.personal,
            "more_than_1": len(m_ec) > 1,
            "position_number": position_number,
            "is_current": is_current,
            "start_date": start_date.strftime("%b %Y"),
            "end_date": end_date,
        }
        return context

    def make_pdf_form(self, *args, **kwargs):
        return super().make_pdf_form(*args, **kwargs)

    def make_web_form(self, *args, **kwargs):
        return super().make_web_form(*args, **kwargs)


class ExperienceModelE(CommonModel, ExperienceModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
