from .context import DATADIR
from pydantic import BaseModel
from .data import General
from basemodels.jobposition import PositionBase
from basemodels.wordmaker import WordMaker
import os
from basemodels.commonmodel import CommonModel


class Position(PositionBase):
    pass


class CompanyInfoModel(BaseModel):
    general: General
    position: Position


class CompanyInfoModel_E(CommonModel, CompanyInfoModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/er.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())


class CompanyInfoDocxAdaptor:
    def __init__(self, employer_training_obj: CompanyInfoModel):
        self.employer_training_obj = employer_training_obj

    def make(self, output_docx):
        template_path = os.path.abspath(
            os.path.join(DATADIR, "word/bcpnp_company_information.docx")
        )
        wm = WordMaker(template_path, self.employer_training_obj, output_docx)
        wm.make()
