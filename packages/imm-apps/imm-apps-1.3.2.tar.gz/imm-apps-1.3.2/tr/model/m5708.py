from pydantic import BaseModel
from termcolor import colored
from functools import reduce
from typing import List, Optional
from basemodels.address import Address
from basemodels.phone import Phone
from basemodels.trperson import (
    COR,
    PersonId,
    Personal,
    Marriage,
    Education,
    Employment,
)
from basemodels.tr import TrCaseIn, TrBackground, VrInCanada
from basemodels.commonmodel import CommonModel, BuilderModel
from tr.pdfform.fb5708 import FormBuilder5708
from datetime import date
import json


class M5708Model(BaseModel, BuilderModel):
    personal: Personal
    marriage: Marriage
    personid: List[PersonId]
    address: List[Address]
    education: List[Education]
    employment: List[Employment]
    phone: List[Phone]
    cor: List[COR]
    trcasein: TrCaseIn
    vrincanada: VrInCanada
    trbackground: TrBackground

    # TODO: python-docx-template cannot use function returned value
    @property
    def visit_description(self):
        last_visit = self.trcasein.most_recent_entry_date
        original_visit = self.trcasein.original_entry_date
        last_place = self.trcasein.most_recent_entry_place
        original_place = self.trcasein.original_entry_place

        # if last visit existed, calculate the days
        visit_date = last_visit or original_visit
        visit_place = last_place or original_place
        days = (date.today() - visit_date).days

        apply_for = "restoration" if days > 180 else "extension"
        return f"I am applying for {apply_for}"

    @property
    def getAllDict(self):
        return {
            **self.dict(),
            "visit_description": self.visit_description,
            "subject": self.personal.subject,
            "object": self.personal.object,
            "attributive": self.personal.attributive,
            "salutation": self.personal.salutation,
            "short_name": self.personal.short_name,
        }

    def make_pdf_form(self, output_json, *args, **kwargs):
        pf = FormBuilder5708(self)
        form = pf.get_form()
        with open(output_json, "w") as output:
            json.dump(form.actions, output, indent=3, default=str)
        raise Exception(f"{output_json} has been created. ")

    def make_web_form(self, output_json, upload_dir, rcic, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")

    def context(self, *args, **kwargs):
        return self.getAllDict


class M5708ModelE(CommonModel, M5708Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/tr.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
