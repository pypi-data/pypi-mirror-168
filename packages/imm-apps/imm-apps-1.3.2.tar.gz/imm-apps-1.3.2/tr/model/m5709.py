from termcolor import colored
from functools import reduce
from typing import List
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
import json

from basemodels.tr import TrCaseIn, TrBackground, SpInCanada
from basemodels.commonmodel import CommonModel, BuilderModel
from tr.pdfform.fb5709 import FormBuilder5709
from pydantic import BaseModel


class M5709Model(BaseModel, BuilderModel):
    personal: Personal
    marriage: Marriage
    personid: List[PersonId]
    address: List[Address]
    education: List[Education]
    employment: List[Employment]
    phone: List[Phone]
    cor: List[COR]
    trcasein: TrCaseIn
    spincanada: SpInCanada
    trbackground: TrBackground

    def make_pdf_form(self, output_json, *args, **kwargs):
        pf = FormBuilder5709(self)
        form = pf.get_form()
        with open(output_json, "w") as output:
            json.dump(form.actions, output, indent=3, default=str)
        raise Exception(f"{output_json} has been created. ")

    def make_web_form(self, output_json, upload_dir, rcic, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")

    def context(self, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")


class M5709ModelE(CommonModel, M5709Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/tr.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
