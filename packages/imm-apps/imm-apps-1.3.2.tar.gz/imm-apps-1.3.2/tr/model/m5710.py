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
from basemodels.tr import TrCaseIn, TrBackground, WpInCanada
from basemodels.commonmodel import CommonModel, BuilderModel
from tr.pdfform.fb5710 import FormBuilder5710
from termcolor import colored
import json
from pydantic import BaseModel


class M5710Model(BaseModel, BuilderModel):
    personal: Personal
    marriage: Marriage
    personid: List[PersonId]
    address: List[Address]
    education: List[Education]
    employment: List[Employment]
    phone: List[Phone]
    cor: List[COR]
    trcasein: TrCaseIn
    wpincanada: WpInCanada
    trbackground: TrBackground

    def make_pdf_form(self, output_json, *args, **kwargs):
        pf = FormBuilder5710(self)
        form = pf.get_form()
        with open(output_json, "w") as output:
            json.dump(form.actions, output, indent=3, default=str)
        raise Exception(f"{output_json} has been created. ")

    def make_web_form(self, output_json, upload_dir, rcic, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")

    def context(self, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")


class M5710ModelE(CommonModel, M5710Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/tr.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
