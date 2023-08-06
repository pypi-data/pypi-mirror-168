from .context import DATADIR
from typing import List
from basemodels.commonmodel import CommonModel, BuilderModel
from .data import Bcpnp, General, JobOffer, ErAddress
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
from basemodels.address import Addresses
from basemodels.wordmaker import WordMaker
import os
from pydantic import BaseModel


class Personal(Person):
    def __str__(self):
        return self.full_name


class Position(PositionBase):
    pass


class EmployerTrainingModel(BaseModel, BuilderModel):
    eraddress: List[ErAddress]
    general: General
    position: Position
    personal: Personal
    joboffer: JobOffer
    personalassess: PersonalAssess
    bcpnp: Bcpnp
    rcic: Rcic
    advertisement: List[Advertisement]
    interviewrecord: List[InterviewRecord]
    recruitmentsummary: RecruitmentSummary

    @property
    def work_location(self):
        addresses = Addresses(self.eraddress)
        return addresses.working

    @property
    def selected_contact(self):
        contacts = Contacts(self.contact)
        return contacts.preferredContact

    @property
    def summary(self):
        return InterviewRecords(self.interviewrecord)

    @property
    def advertisements(self):
        return Advertisements(self.advertisement)

    @property
    def person(self):
        return {
            "full_name": self.personal.full_name,
            "attributive": self.personal.attributive,
            "object": self.personal.object,
            "subject": self.personal.subject,
            "short_name": self.personal.short_name,
        }

    def context(self, *args, **kwargs):
        context = {
            **self.dict(),
            "resume_num": self.summary.resume_num,
            "canadian_num": self.summary.canadian_num,
            "unknown_num": self.summary.unknown_num,
            "foreigner_num": self.summary.foreigner_num,
            "total_canadian": self.summary.total_canadian,
            "total_interviewed_canadians": self.summary.total_interviewed_canadians,
            "canadian_records": self.summary.canadian_records,
            "advertisement": self.advertisements,
            "personal": self.person,
            "date_of_offer": self.joboffer.date_of_offer,
            "work_start_date": self.joboffer.start_date_say,
            "joboffer_date": self.joboffer.date_of_offer,
            "work_location": self.work_location,
        }
        return context

    def make_pdf_form(self, *args, **kwargs):
        pass

    def make_web_form(self, *args, **kwargs):
        pass


class EmployerTrainingModelE(CommonModel, EmployerTrainingModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = [
            "excel/er.xlsx",
            "excel/pa.xlsx",
            "excel/recruitment.xlsx",
            "excel/bcpnp.xlsx",
            "excel/rep.xlsx",
        ]
        super().__init__(excels, output_excel_file, mother_excels, globals())
