from basemodels.advertisement import Advertisements, InterviewRecords
from basemodels.finance import Finance
from basemodels.advertisement import Advertisement, Advertisements
from basemodels.advertisement import (
    InterviewRecord,
    InterviewRecords,
    RecruitmentSummary,
)
from basemodels.contact import Contacts
from .common import *
from basemodels.commonmodel import CommonModel, BuilderModel
from ..webform.webformmodel import WebformModel
from pydantic import BaseModel


class M5593Model(BaseModel, BuilderModel):
    lmiacase: LmiaCase
    general: General
    lmi: Lmi
    eraddress: List[ErAddress]
    contact: List[Contact]
    finance: List[Finance]
    joboffer: Joboffer
    personal: Personal
    personalassess: PersonalAssess
    position: Position
    advertisement: List[Advertisement]
    interviewrecord: List[InterviewRecord]
    rcic: Rcic
    recruitmentsummary: RecruitmentSummary

    def context(self, *args, **kwargs):
        interview = InterviewRecords(self.interviewrecord)
        primary_contact = Contacts(self.contact).primary
        return {
            **self.dict(),
            "formatted_finance": [
                {
                    "year": f.year,
                    "formatted_revenue": f.formatted_revenue,
                    "formatted_net_income": f.formatted_net_income,
                    "formatted_retained_earning": f.formatted_retained_earning,
                }
                for f in self.finance
            ],
            "num_of_job_posts": Advertisements(self.advertisement).amount,
            "why_qualified": self.personalassess.why_qualified,
            "adv_summary": [
                {
                    "start_date": a.start_date,
                    "end_date": a.end_date,
                    "media": a.media,
                    "days": a.days,
                }
                for a in self.advertisement
            ],
            "high_wage": True
            if float(self.joboffer.hourly_rate) >= self.lmiacase.provincial_median_wage
            else False,
            "rs": {
                "resume_num": interview.resume_num,
                "canadian_num": interview.canadian_num,
                "unknown_num": interview.unknown_num,
                "foreigner_num": interview.foreigner_num,
                "total_canadian": interview.total_canadian,
                "total_interviewed_canadians": interview.total_interviewed_canadians,
                "canadian_records": interview.canadian_records,
            },
            "primary_contact": primary_contact,
            "employee_name": self.personal.full_name,
        }

    def make_web_form(self, output_json, upload_dir, rcic, *args, **kwargs):
        args = {
            "model_variable": "5593",
            "app": self,
            "output_json": output_json,
            "upload_dir": upload_dir,
            "rcic": rcic,
        }
        wf = WebformModel(**args)
        return wf.save()

    def make_pdf_form(self):
        pass


class M5593ModelE(CommonModel, M5593Model):
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = [
            "excel/recruitment.xlsx",
            "excel/pa.xlsx",
            "excel/er.xlsx",
            "excel/rep.xlsx",
            "excel/lmia.xlsx",
        ]
        # call parent class for validating
        super().__init__(excels, output_excel_file, mother_excels, globals())
