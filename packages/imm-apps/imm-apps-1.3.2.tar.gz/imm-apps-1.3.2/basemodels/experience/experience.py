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

    def context(self, doc_type=None):
        if doc_type == "ec":
            # Get company set
            try:
                company_set = set(
                    [
                        emp.company
                        for emp in self.employment
                        if emp.employment_certificate
                    ]
                )
            except KeyError as err:
                raise ValueError(
                    f'key error in employment sheet. Please check "company","employment","employment_certificate"'
                )
            # pick a company for employment certificate generation
            companies = list(company_set)
            [print(index, company) for index, company in enumerate(companies)]
            which_one = input("Please input the number of the employer: ")
            company = companies[int(which_one)]

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
        elif doc_type == "rs":
            for emp in self.employment:
                emp.start_date = emp.start_from
                emp.end_date = emp.end_to
            for edu in self.education:
                edu.start_date = edu.start_from
                edu.end_date = edu.end_to
            context = {
                **self.dict(),
                "phone": Phones(self.phone).PreferredPhone.international_format_full,
                "address": Addresses(self.address).PreferredAddress.full_address,
                "full_name": self.personal.full_name,
            }
        else:
            context = {}

        return context

    def make_web_form(self, output_json, upload_dir, rcic):
        pass

    def make_pdf_form(self):
        pass


class ExperienceModelE(CommonModel, ExperienceModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
