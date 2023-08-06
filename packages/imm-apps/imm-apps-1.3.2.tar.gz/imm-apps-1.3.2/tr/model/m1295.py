from termcolor import colored
from functools import reduce
from typing import List, Optional
from basemodels.address import Address
from basemodels.educationbase import EducationHistory
from basemodels.phone import Phone
from basemodels.trperson import (
    COR,
    PersonId,
    Personal,
    Marriage,
    Education,
    Employment,
    Travel,
    Family,
)
from basemodels.person import PersonalAssess
from basemodels.tr import TrCase, Wp, TrBackground
from basemodels.commonmodel import CommonModel, BuilderModel
from tr.pdfform.fb1295 import FormBuilder1295
from basemodels.rcic import Rcic
import json
from pydantic import BaseModel


class M1295Model(BaseModel, BuilderModel):
    personal: Personal
    personalassess: PersonalAssess
    marriage: Marriage
    personid: List[PersonId]
    address: List[Address]
    education: List[Education]
    employment: List[Employment]
    travel: List[Travel]
    family: List[Family]
    phone: List[Phone]
    cor: List[COR]
    trcase: TrCase
    wp: Wp
    trbackground: TrBackground
    rcic: Rcic

    def make_pdf_form(self, output_json, *args, **kwargs):
        pf = FormBuilder1295(self)
        form = pf.get_form()
        with open(output_json, "w") as output:
            json.dump(form.actions, output, indent=3, default=str)
        raise Exception(f"{output_json} has been created. ")

    def make_web_form(self, output_json, upload_dir, rcic, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")

    def context(self, *args, **kwargs):
        education = EducationHistory(self.education)
        educations = (
            education.post_secondary
            if len(education.post_secondary) > 0
            else education.high_school
        )
        return {
            **self.dict(),
            "birthday": self.personal.birthday,
            "respectful_full_name": self.personal.respectful_full_name,
            "short_name": self.personal.short_name,
            "educations": educations,
            "ties": [self.wp.family_tie, self.wp.economic_tie, self.wp.other_tie],
        }


class M1295ModelE(CommonModel, M1295Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/tr.xlsx", "excel/pa.xlsx", "excel/rep.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
