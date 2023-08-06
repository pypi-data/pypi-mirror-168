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
    def __init__(self, excels=None, output_excel_file=None,language:str|None=None):
        from basemodels.utils import excel_language_path
        path=excel_language_path(language)
        mother_excels = [path+"/recruitment.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
