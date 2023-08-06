from datetime import date
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date
from basemodels.commonmodel import CommonModel, BuilderModel
from basemodels.rcic import RcicList
from basemodels.contact import ContactBase
from ..pdfform.fbrep import FormBuilderBcRep
import json
from termcolor import colored
from basemodels.employerbase import EmployerBase
from ..webform.rep import Representative


class General(EmployerBase):
    pass


class Contact(ContactBase):
    pass


class Personal(BaseModel):
    last_name: str
    first_name: str
    sex: str
    dob: date
    uci: Optional[str]


class MRepModel(BaseModel, BuilderModel):
    rciclist: List[RcicList]
    personal: Personal
    general: General
    contact: List[Contact]

    def make_pdf_form(self, output_json, rcic_id_name, *args, **kwargs):
        pf = FormBuilderBcRep(self, rcic_id_name)
        form = pf.get_form()
        with open(output_json, "w") as output:
            json.dump(form.actions, output, indent=3, default=str)
        return f"{output_json} has been created."

    def make_web_form(self, output_json, upload_dir, rcic_id_name, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")

    def context(self, *args, **kwargs):
        raise ValueError("This model doesn't have webform...")


class MRepModelE(CommonModel, MRepModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx", "excel/rep.xlsx", "excel/er.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
