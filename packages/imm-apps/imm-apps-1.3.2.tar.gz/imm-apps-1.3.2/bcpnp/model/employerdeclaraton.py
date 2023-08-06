from typing import List
from basemodels.commonmodel import CommonModel, BuilderModel
from .data import Contact, General, JobOffer, ErAddress
from basemodels.jobposition import PositionBase
from basemodels.rcic import Rcic
from basemodels.advertisement import (
    Advertisement,
    Advertisements,
    InterviewRecord,
    InterviewRecords,
    RecruitmentSummary,
)
from basemodels.person import Person, PersonalAssess
from basemodels.contact import Contacts
from basemodels.address import Addresses
from basemodels.phone import Phone, Phones
from typing import Optional
from ..pdfform.fbemployerdeclaration import FormBuilderEmployerDeclaration
from pydantic import BaseModel


class Personal(Person):
    def __str__(self):
        return self.full_name


class Position(PositionBase):
    is_new: bool
    has_same_number: Optional[int]
    vacancies_number: Optional[int]
    laidoff_with12: Optional[int]
    laidoff_current: Optional[int]


class EmployerDeclaratonFormModel(BaseModel, BuilderModel):
    eraddress: List[ErAddress]
    phone: List[Phone]
    general: General
    contact: List[Contact]
    position: Position
    personal: Personal
    joboffer: JobOffer
    personalassess: PersonalAssess
    # bcpnp: Bcpnp
    rcic: Rcic
    advertisement: List[Advertisement]
    interviewrecord: List[InterviewRecord]
    recruitmentsummary: RecruitmentSummary

    @property
    def work_location(self):
        addresses = Addresses(self.eraddress)
        return addresses.working

    @property
    def phones(self):
        return Phones(self.phone)

    @property
    def selected_contact(self):
        contacts = Contacts(self.contact)
        return contacts.preferredContact

    @property
    def interviews(self):
        return InterviewRecords(self.interviewrecord)

    @property
    def advertisements(self):
        return Advertisements(self.advertisement)

    @property
    def businessaddress(self):
        eraddress = Addresses(self.eraddress)
        return eraddress.business

    @property
    def mailingaddress(self):
        eraddress = Addresses(self.eraddress)
        return eraddress.mailing

    @property
    def person(self):
        return {
            "first_name": self.personal.first_name,
            "last_name": self.personal.last_name,
            "full_name": self.personal.full_name,
            "attributive": self.personal.attributive,
            "object": self.personal.object,
            "subject": self.personal.subject,
            "short_name": self.personal.short_name,
            "why_tfw": self.personalassess.why_qualified_say,
        }

    def context(self, *args, **kwargs):
        pass

    def make_pdf_form(self, output_json, *args, **kwargs):
        pf = FormBuilderEmployerDeclaration(self)
        pf.save(output_json)

    def make_web_form(self, *args, **kwargs):
        pass


class EmployerDeclaratonFormModelE(CommonModel, EmployerDeclaratonFormModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = [
            "excel/er.xlsx",
            "excel/pa.xlsx",
            "excel/recruitment.xlsx",
            "excel/bcpnp.xlsx",
            "excel/rep.xlsx",
        ]
        super().__init__(excels, output_excel_file, mother_excels, globals())
