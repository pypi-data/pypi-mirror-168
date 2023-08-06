from termcolor import colored
from pydantic import BaseModel, EmailStr, root_validator
from functools import reduce
from typing import List, Optional
from basemodels.address import Address
from basemodels.mixins import DatePeriod
from basemodels.phone import Phone
from basemodels.commonmodel import CommonModel
from basemodels.educationbase import EducationBase
from basemodels.utils import checkRow
from utils.utils import checkContinuity
from datetime import date
from utils.utils import PydanticException


class Family(BaseModel):
    relationship: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    native_last_name: Optional[str]
    native_first_name: Optional[str]
    date_of_birth: Optional[date]
    date_of_death: Optional[date]
    place_of_birth: Optional[str]
    birth_country: Optional[str]
    marital_status: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]

    @root_validator
    def checkCompletion(cls, values):
        all_fields = [
            "relationship",
            "last_name",
            "first_name",
            "native_last_name",
            "native_first_name",
            "date_of_birth",
            "date_of_death",
            "place_of_birth",
            "birth_country",
            "marital_status",
            "email",
            "address",
        ]
        required_fields = [
            "relationship",
            "last_name",
            "first_name",
            "native_last_name",
            "native_first_name",
            "date_of_birth",
            "place_of_birth",
            "birth_country",
            "marital_status",
            "address",
        ]
        checkRow(values, all_fields, required_fields)
        return values


class Personal(BaseModel):
    last_name: str
    first_name: str
    native_last_name: str
    native_first_name: str
    dob: date


class PRBackground(BaseModel):
    q1: bool
    q2: bool
    q3: bool
    q4: bool
    q5: bool
    q6: bool
    q7: bool
    q8: bool
    q9: bool
    q10: bool
    q11: bool
    details: Optional[str]


class Education(EducationBase):
    city: Optional[str]
    country: Optional[str]


class History(DatePeriod):
    activity: str
    city_and_country: str
    status: str
    name_of_company_or_school: str

    @property
    def __str__(self) -> str:
        return "table-history"


class Member(DatePeriod):
    organization_name: str
    organization_type: str
    position: str
    city: str
    country: str


class Government(DatePeriod):
    country: str
    department: str
    position: str


class Military(DatePeriod):
    country: str
    service_detail: str
    rank: str
    combat_detail: Optional[str]
    reason_for_end: Optional[str]


class AddressHistory(DatePeriod):
    street_and_number: str
    city: str
    province: str
    country: str
    post_code: str

    @property
    def __str__(self) -> str:
        return "table-addresshistory"


class M5669Model(BaseModel):
    personal: Personal
    family: List[Family]
    prbackground: PRBackground
    education: List[Education]
    history: List[History]
    member: List[Member]
    government: List[Government]
    military: List[Military]
    addresshistory: List[AddressHistory]

    def check(self, items: List[object]):
        results = []
        # construct list suitable for checkContinuity
        for item in items:
            results.append(list(item.__dict__.values()))

        # check
        continued, sorted_list, msg = checkContinuity(results)

        if not continued:
            msg1 = [f"There are {len(msg)} error(s) in sheet {items[0].__str__}"]
            msg2 = [f"{index},'\t', {m}" for index, m in enumerate(msg)]
            msg = "\n".join(msg1 + msg2)
            raise PydanticException(msg)


class M5669ModelE(CommonModel, M5669Model):
    def __init__(self, excels=None, output_excel_file=None, check=False):
        mother_excels = ["excel/pr.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
        if check:
            [self.check(item) for item in [self.history, self.addresshistory]]

    def check(self, items: List[object]):
        results = []
        # construct list suitable for checkContinuity
        for item in items:
            results.append(list(item.__dict__.values()))

        # check
        continued, sorted_list, msg = checkContinuity(results)

        if not continued:
            msg1 = [f"There are {len(msg)} error(s) in sheet {items[0].__str__}"]
            msg2 = [f"{index}, '\t', {m}" for index, m in enumerate(msg)]
            msg = "\n".join(msg1 + msg2)
            raise PydanticException(msg)
