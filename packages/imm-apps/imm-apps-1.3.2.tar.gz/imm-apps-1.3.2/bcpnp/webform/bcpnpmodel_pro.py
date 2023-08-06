from typing import List, Optional
from basemodels.address import Address
from basemodels.educationbase import EducationBase
from basemodels.phone import Phone
from basemodels.commonmodel import CommonModel, BuilderModel
from basemodels.employmentbase import EmploymentBase
from basemodels.jobofferbase import JobofferBase
from basemodels.id import ID
from basemodels.person import Person
from basemodels.language import LanguageBase
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, root_validator, validator
from basemodels.utils import normalize
from termcolor import colored
from .joboffer_reg import JobofferReg
from .login import Login
from .registrant import Registrant
from .education_reg import EducationReg
from .employment import EmploymentReg
from .language import LanguageReg
from .joboffer_reg import JobofferReg
from .submit import Submit
from .register import Register
import json


class PersonId(ID):
    pass


class Personal(Person):
    email: EmailStr
    used_last_name: Optional[str]
    used_first_name: Optional[str]
    place_of_birth: str
    country_of_birth: str
    did_eca: bool
    eca_supplier: Optional[str]
    eca_number: Optional[str]
    ita_assessed: bool
    ita_assess_number: Optional[str]

    _normalize_used_first_name = validator(
        "used_first_name", allow_reuse=True, check_fields=False
    )(normalize)
    _normalize_used_last_name = validator(
        "used_last_name", allow_reuse=True, check_fields=False
    )(normalize)

    @root_validator
    def checkECA(cls, values):
        did_eca = values.get("did_eca")
        eca_supplier = values.get("eca_supplier")
        eca_number = values.get("eca_number")

        if did_eca and not all([eca_supplier, eca_number]):
            raise ValueError(f"Did ECA,but not input ECA number and/or ECA supplier")
        return values

    @root_validator
    def checkITA(cls, values):
        ita_assessed = values.get("ita_assessed")
        ita_assess_number = values.get("ita_assess_number")

        if ita_assessed and not ita_assess_number:
            raise ValueError(
                f"You selected ITA as Yes,but not input ITA assessment number"
            )
        return values

    @property
    def user_id(self):
        dob = self.dob.strftime(("%Y-%m-%d"))
        return (
            self.last_name[0].upper()
            + self.first_name[0]
            + dob.split("-")[0]
            + dob.split("-")[1]
            + dob.split("-")[2]
        )

    @property
    def password(self):
        return "Super" + str(datetime.today().year) + "!"


class BcpnpModelPro(BaseModel, BuilderModel):
    personal: Personal
    address: List[Address]
    phone: List[Phone]
    personid: List[PersonId]

    def context(self, *args, **kwargs):
        pass

    def make_pdf_form(self, *args, **kwargs):
        pass

    def make_web_form(
        self, output_json="", initial=True, previous=False, *args, **kwargs
    ):
        actions = Register(self).fill()
        with open(output_json, "w") as f:
            json.dump(actions, f, default=str, indent=3)
        return f"{output_json} has been created."


class BcpnpModelProE(CommonModel, BcpnpModelPro):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
