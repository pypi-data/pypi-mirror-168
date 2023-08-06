from basemodels.commonmodel import CommonModel, BuilderModel
from datetime import date
from pydantic import BaseModel, root_validator
from typing import List
from basemodels.mixins import DatePeriod
from basemodels.utils import checkRow


class Travel(DatePeriod):
    length: int
    destination: str
    purpose: str

    @root_validator
    def checkCompletion(cls, values):
        all_fields = ["start_date", "end_date", "length", "destination", "purpose"]
        required_fields = ["start_date", "end_date", "length", "destination", "purpose"]
        checkRow(values, all_fields, required_fields)
        return values


class Personal(BaseModel):
    last_name: str
    first_name: str


class M5562Model(BaseModel):
    travel: List[Travel]
    personal: Personal


class M5562ModelE(CommonModel, M5562Model):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
