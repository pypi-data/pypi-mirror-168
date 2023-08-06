from pydantic import BaseModel, EmailStr
from basemodels.commonmodel import CommonModel
import os
from typing import List
from pydantic import BaseModel
from basemodels.advertisement import (
    Advertisement,
    InterviewRecord,
    RecruitmentSummary,
)


class LmiaApplication(BaseModel):
    advertisement: List[Advertisement]
    interviewrecord: List[InterviewRecord]
    recruitmentsummary: RecruitmentSummary


class LmiaApplicationE(CommonModel, LmiaApplication):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/recruitment.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
