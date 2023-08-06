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
    Travel,
    Family,
)
from basemodels.tr import TrCase, Visa, TrBackground
from basemodels.commonmodel import CommonModel
from pydantic import BaseModel

"""
Program model for temporary resident visa. Get and validate info for forms: imm5257, imm0104, imm5257b_1, and imm5645
"""


class M5257Model(BaseModel):
    personal: Personal
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
    visa: Visa
    trbackground: TrBackground


class M5257ModelE(CommonModel, M5257Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/tr.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
