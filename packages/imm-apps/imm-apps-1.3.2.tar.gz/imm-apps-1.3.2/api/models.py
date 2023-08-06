import re, sys
from pydantic import BaseModel
from typing import Optional
from system.models import get_models
from pathlib import Path
import uuid
from basemodels.wordmaker import WordMaker
from system.config import Default
from api.context import BASEDIR


class ImmBase(BaseModel):
    model: str

    def getModel(self, model_type="original"):
        # get model, and its instance
        models = get_models(
            rcic_company_id_name=Default.rciccompany, temp_num=Default.temp_num
        )
        model = models.get(self.model)
        if not model:
            raise ValueError(f"{self.model} is not a valid model name.")
        class_list = model["class_list"]
        the_class = __import__(model["path"], fromlist=class_list)
        if model_type == "original":
            the_model = getattr(the_class, class_list[0])  # original model
        elif model_type == "excel":
            the_model = getattr(the_class, class_list[1])  # excel model
        else:
            the_model = getattr(the_class, class_list[2])  # future for database model
        return the_model


class ImmMake(ImmBase):
    def make(self):
        """Make excel based on model, return the file name"""
        # create excel
        the_model = self.getModel(model_type="excel")
        name = uuid.uuid4().hex + ".xlsx"
        excel_name = BASEDIR / "tmp" / name
        the_model(output_excel_file=excel_name)
        return excel_name


class ImmCheck(ImmBase):
    data: dict

    def check(self):
        the_model = self.getModel()
        model_obj = the_model(**self.data)
        if model_obj.dict() != {}:
            return {
                "success": "The model has been checked and everything seems good..."
            }


class ImmWord(ImmBase):
    data: dict
    output_name: str
    doctype: Optional[str]
    rciccompany: str = Default.rciccompany
    tempnum: int = Default.temp_num

    def word(self):
        the_model = self.getModel()
        models = get_models(
            rcic_company_id_name=self.rciccompany, temp_num=self.tempnum
        )
        template_docx_dict = models.get(self.model).get("docx_template")
        if not template_docx_dict:
            raise ValueError(
                f"There is no template {template_docx_dict} existing in model {self.model}"
            )

        # if there  is no args.document, which means the model has only one  default  dict element
        def getOnlyOneTemplate():
            the_only_one_temp = list(template_docx_dict.keys())
            temp_number = len(the_only_one_temp)
            if temp_number == 1:
                return template_docx_dict.get(the_only_one_temp[0])
            elif temp_number > 1:
                raise ValueError(
                    "Word templates more than one in the model, but you did not input the doc type abbreviation"
                )
            else:
                return None

        # if with doc type , get the specific template, or  without args.document, get the only one
        template_docx = (
            template_docx_dict.get(self.doctype)
            if self.doctype
            else getOnlyOneTemplate()
        )
        if not template_docx:
            raise ValueError(
                f"{self.doctype} is not a valid document type, please check the manual by typing:'imm man'to see valid word template for each model"
            )
        elif not Path(template_docx).exists():
            raise FileNotFoundError(
                f"{template_docx} is not existed. Please check your template base"
            )

        model_instance = the_model(**self.data)
        context = model_instance.context(doc_type=self.doctype)
        word_name = uuid.uuid4().hex + ".docx"
        word_name = BASEDIR / "tmp" / word_name
        wm = WordMaker(template_docx, context, word_name)
        wm.make()
        return word_name


class ImmWebform(ImmBase):
    data: dict
    output_name: str
    rcic: str = Default.rcic
    tempnum: int = Default.temp_num
    uploaddir: str = Default.uploaddir
    initial: bool = Default.initial
    previous: bool = Default.previous

    def webform(self):
        json_name = uuid.uuid4().hex + ".json"
        json_name = BASEDIR / "tmp" / json_name
        key_args = {
            "output_json": json_name,
            "upload_dir": self.uploaddir,
            "rcic": self.rcic,
            "initial": self.initial,
            "previous": self.previous,
        }
        the_model = self.getModel()
        app = the_model(**self.data)
        app.make_web_form(**key_args)
        return json_name


class ImmPdfform(ImmBase):
    data: dict
    output_name: str
    rcic: str = Default.rcic

    def pdfform(self):
        json_name = uuid.uuid4().hex + ".json"
        json_name = BASEDIR / "tmp" / json_name
        key_args = {"output_json": json_name, "rcic_id_name": self.rcic}
        the_model = self.getModel()
        app = the_model(**self.data)
        app.make_pdf_form(**key_args)
        return json_name


class ImmRun(ImmBase):
    data: dict

    def run(self):
        """Run app only"""
        the_model = self.getModel()
        model_obj = the_model(**self.data)
        result = ""
        if hasattr(model_obj, "result"):
            for k, v in model_obj.result.items():
                result += (f"{k}: {v}") + "\n"
            return {"success": result}
        else:
            raise ValueError(
                f"The model {self.model} has no excution function with return result."
            )

class Word(BaseModel):
    context:dict
    
    def make(self,template_docx:str):
        word_name = uuid.uuid4().hex + ".docx"
        word_name = BASEDIR / "tmp" / word_name
        wm = WordMaker(template_docx, self.context, word_name)
        wm.make()
        return word_name