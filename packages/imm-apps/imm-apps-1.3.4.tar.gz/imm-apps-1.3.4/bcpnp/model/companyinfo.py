from .context import DATADIR
from pydantic import BaseModel
from .data import General
from basemodels.jobposition import PositionBase
from basemodels.wordmaker import WordMaker
import os
from basemodels.commonmodel import CommonModel,BuilderModel


class Position(PositionBase):
    pass


class CompanyInfoModel(BaseModel,BuilderModel):
    general: General
    position: Position
    
    def context(self, *args, **kwargs):
        return self.dict()

    def make_pdf_form(self, *args, **kwargs):
        return super().make_pdf_form(*args, **kwargs)
    
    def make_web_form(self, *args, **kwargs):
        return super().make_web_form(*args, **kwargs)

class CompanyInfoModel_E(CommonModel, CompanyInfoModel):
    def __init__(self, excels=None, output_excel_file=None,language:str|None=None):
        from basemodels.utils import excel_language_path
        path=excel_language_path(language)
        mother_excels = [path+"/er.xlsx"]
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
