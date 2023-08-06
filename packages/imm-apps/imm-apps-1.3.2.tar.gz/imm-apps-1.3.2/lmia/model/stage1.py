from datetime import date
from typing import Optional, List
from pydantic import BaseModel, root_validator
from basemodels.commonmodel import CommonModel
import os


class General(BaseModel):
    legal_name: str
    operating_name: Optional[str]
    website: Optional[str]
    establish_date: date
    num_pnps: int
    num_pnps_approved: int
    num_pnps_in_process: int
    has_lmia_approved: bool
    when_lmia_approved: Optional[date]
    last_revenue: float
    last_profit: float
    before_last_revenue: float
    before_last_profit: float
    retained_earning: float
    has_jobbank_account: bool
    has_bc_employer_certificate: bool


class Employee_list(BaseModel):
    employee: str
    job_title: str
    wage: float
    hours_per_week: float
    immigration_status: str
    employment_start_date: date
    remark: Optional[str]


class Lmi(BaseModel):
    laid_off_in_12: bool
    laid_off_canadians: Optional[int]
    laid_off_tfw: Optional[int]
    laid_off_reason: Optional[str]
    is_work_sharing: bool
    work_sharing_info: Optional[str]
    labour_dispute: bool
    labour_dispute_info: Optional[str]

    @root_validator
    def checkLayoff(cls, values):
        laid_off_in_12 = values.get("laid_off_in_12", None)
        laid_off_canadians = values.get("laid_off_canadians", None)
        laid_off_tfw = values.get("laid_off_tfw", None)
        laid_off_reason = values.get("laid_off_reason", None)
        if laid_off_in_12 and (
            not laid_off_canadians or not laid_off_tfw or not laid_off_reason
        ):
            raise ValueError(
                "Since there is laid of in past 12 months in info lmi sheet,but did not input how many Canadians and/or foreign workers, and/or reason of lay off."
            )
        return values

    @root_validator
    def checkWorkSharing(cls, values):
        is_work_sharing = values.get("is_work_sharing", None)
        work_sharing_info = values.get("work_sharing_info", None)
        if is_work_sharing and not work_sharing_info:
            raise ValueError(
                "Since there is work sharing in info lmi sheet,but did not input the details about it."
            )
        return values


class LmiaAssess(BaseModel):
    general: General
    employee_list: List[Employee_list]
    lmi: Lmi


class LmiaAssessE(CommonModel):
    general: General
    employee_list: List[Employee_list]
    lmi: Lmi

    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/er.xlsx", "excel/lmia.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
