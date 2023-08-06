from .context import DATADIR
from typing import List
from basemodels.commonmodel import CommonModel, BuilderModel
from .data import Contact, General, JobOffer, PersonalAssess, Bcpnp
from basemodels.jobposition import PositionBase
from basemodels.person import Person
from basemodels.advertisement import (
    Advertisement,
    Advertisements,
    InterviewRecord,
    RecruitmentSummary,
    InterviewRecords,
)
from basemodels.contact import Contacts
from basemodels.wordmaker import WordMaker
import os
from pydantic import BaseModel


class Personal(Person):
    def __str__(self):
        return self.full_name


class Position(PositionBase):
    pass


class RecommendationLetterModel(BaseModel, BuilderModel):
    bcpnp: Bcpnp
    general: General
    contact: List[Contact]
    position: Position
    personal: Personal
    joboffer: JobOffer
    personalassess: PersonalAssess
    advertisement: List[Advertisement]
    interviewrecord: List[InterviewRecord]
    recruitmentsummary: RecruitmentSummary

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
        return {
            **self.dict(),
            "resume_num": self.summary.resume_num,
            "canadian_num": self.summary.canadian_num,
            "unknown_num": self.summary.unknown_num,
            "foreigner_num": self.summary.foreigner_num,
            "total_canadian": self.summary.total_canadian,
            "total_interviewed_canadians": self.summary.total_interviewed_canadians,
            "canadian_records": self.summary.canadian_records,
            "contact": self.selected_contact,
            "advertisement": self.advertisements,
            "personal": self.person,
            "work_start_date": self.joboffer.start_date_say,
            "joboffer_date": self.joboffer.date_of_offer,
        }

    def make_pdf_form(self, *args, **kwargs):
        pass

    def make_web_form(self, *args, **kwargs):
        pass


class RecommendationLetterModelE(CommonModel, RecommendationLetterModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = [
            "excel/er.xlsx",
            "excel/pa.xlsx",
            "excel/recruitment.xlsx",
            "excel/bcpnp.xlsx",
            "excel/rep.xlsx",
        ]
        super().__init__(excels, output_excel_file, mother_excels, globals())
