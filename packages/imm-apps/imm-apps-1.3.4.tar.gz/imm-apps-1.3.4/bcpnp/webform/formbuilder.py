from .register import Register
from .bcpnpmodel_reg import BcpnpModelReg, BcpnpEEModelReg
from .bcpnpmodel_app import BcpnpEEModelApp, BcpnpModelApp
from .login import Login
from .registrant import Registrant
from .education_reg import EducationReg
from .employment import EmploymentReg
from .joboffer_reg import JobofferReg
from .language import LanguageReg
from .rep import Representative
from .submit import Submit
from pathlib import Path
from abc import ABC, abstractmethod
from .applicant import Applicant
from .education_app import EducationApp
from .workexperience import WorkExperience
from .family import FamilyApp
from .joboffer_app import JobofferApp
from .rep import Representative
from ..model.mrep import RcicList
from ..model.mrep import MRepModel


class Builder(ABC):
    def __init__(self, excels) -> None:
        if len(excels) > 0 and not Path(excels[0]).exists():
            raise FileExistsError(f"{excels[0]} is not existed")

    @abstractmethod
    def make_web_form(self, *args, **kwargs):
        raise NotImplementedError("This class must be implemented. ")


class ProfileBuilder(Builder):
    def __init__(self, excels, model: object):
        super().__init__(excels)
        self.applicant = model(excels=excels)

    def make_web_form(self):
        # signing in, pick skill immigration, select stream and confirm
        actions = Login(self.applicant).login()
        # Registrant
        actions += Registrant(self.applicant).fill()
        return actions


class RegBuilder(Builder):
    action_blocks = [
        Registrant,
        EducationReg,
        EmploymentReg,
        JobofferReg,
        LanguageReg,
        Submit,
    ]

    def __init__(self, excels, is_ee: bool = False):
        super().__init__(excels)
        self.applicant = (
            BcpnpEEModelReg(excels=excels) if is_ee else BcpnpModelReg(excels=excels)
        )

    def make_web_form(self, initial=True, previous=False):
        actions = Login(self.applicant).login(initial=initial, previous=previous)
        for block in RegBuilder.action_blocks:
            actions += block(self.applicant).fill()

        return actions


class AppBuilder(Builder):
    action_blocks = [
        Applicant,
        EducationApp,
        WorkExperience,
        FamilyApp,
        JobofferApp,
        Submit,
    ]

    def __init__(self, excels, is_ee: bool = False):
        super().__init__(excels)
        self.applicant = (
            BcpnpEEModelApp(excels=excels) if is_ee else BcpnpModelApp(excels=excels)
        )

    def make_web_form(self, initial=True, previous=False):
        actions = Login(self.applicant).login(initial=initial, previous=previous)
        for block in AppBuilder.action_blocks:
            actions += block(self.applicant).fill()

        return actions
