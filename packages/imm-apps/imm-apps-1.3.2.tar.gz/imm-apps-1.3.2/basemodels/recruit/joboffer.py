from .context import DATADIR
from typing import List
from basemodels.commonmodel import CommonModel, BuilderModel
from basemodels.recruit.jobofferdata import JobOffer, General, ErAddress, ErAddresses
from basemodels.address import Address, Addresses
from basemodels.person import Person
from basemodels.wordmaker import WordMaker
import os
from pydantic import BaseModel


class Personal(Person):
    def __str__(self):
        return self.full_name


class JobofferModel(BaseModel, BuilderModel):
    general: General
    joboffer: JobOffer
    eraddress: List[ErAddress]
    personal: Personal
    address: List[Address]

    def context(self, *args, **kwargs):
        context = {
            **self.dict(),
            "offer_date": self.joboffer.offer_date.strftime("%b %d, %Y"),
            "term": self.joboffer.term,
            "has_benefits": self.joboffer.has_benefits,
            "benefits": self.joboffer.benefits.lower(),
            "full_part_time": self.joboffer.full_part_time,
            "workingaddress": ErAddresses(self.eraddress).working,
            "address_line1": Addresses(self.address).residential.line1,
            "address_line2": Addresses(self.address).residential.line2,
            "work_start_date": self.joboffer.work_start_date.strftime("%b %d, %Y")
            if self.joboffer.work_start_date
            else None,
            "vacation_pay_percentage": self.joboffer.vacation_pay_percent,
        }
        return context

    def make_pdf_form(self, *args, **kwargs):
        pass

    def make_web_form(self, *args, **kwargs):
        pass


class JobofferModelE(CommonModel, JobofferModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/pa.xlsx", "excel/er.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())


class JobofferModelDocxAdapater:
    """This is an adapater to bridging job ad model data and docx data"""

    def __init__(self, joboffer_obj: JobofferModel):
        # get original obj, which will be used to generate some value based on it's object methods.
        # 此处用来处理list里面的一些内容。
        self.joboffer_obj = joboffer_obj
        eraddresses = ErAddresses(self.joboffer_obj.eraddress)
        self.joboffer_obj.eraddress = eraddresses.working

        addresses = Addresses(self.joboffer_obj.address)
        self.joboffer_obj.address = addresses.residential

    def make(self, output_docx, template_no=None):
        file_name = "word/joboffer" + str(template_no) + ".docx"
        template_path = os.path.abspath(os.path.join(DATADIR, file_name))
        wm = WordMaker(template_path, self.joboffer_obj, output_docx)
        wm.make()
