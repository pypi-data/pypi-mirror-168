from pydantic import BaseModel
from typing import List
from basemodels.commonmodel import CommonModel

# from context import DATADIR


class CapTFW(BaseModel):
    employee: str
    hourly_rate: float
    hours_per_week: float
    is_working: bool
    designated_position: bool
    pr_support_only_lmia: bool
    in_application: bool
    pr_in_process: bool


class General(BaseModel):
    canadian_ft_employee_num: int
    canadian_pt_employee_num: int


class LmiaCase(BaseModel):
    provincial_median_wage: float


class CapModel(BaseModel):
    general: General
    lmiacase: LmiaCase
    captfw: List[CapTFW]

    @property
    def A(self):
        ft_tfws_num = len(
            [tfw for tfw in self.captfw if tfw.hours_per_week >= 30 and tfw.is_working]
        )
        return self.general.canadian_ft_employee_num + ft_tfws_num

    @property
    def B(self):
        pt_tfws_num = len(
            [tfw for tfw in self.captfw if tfw.hours_per_week < 30 and tfw.is_working]
        )
        return self.general.canadian_pt_employee_num + pt_tfws_num

    @property
    def C(self):
        return len(
            [
                tfw
                for tfw in self.captfw
                if tfw.hourly_rate < self.lmiacase.provincial_median_wage
                and tfw.is_working
                and not tfw.in_application
            ]
        )

    @property
    def D(self):
        return len(
            [
                tfw
                for tfw in self.captfw
                if tfw.hourly_rate < self.lmiacase.provincial_median_wage
                and tfw.is_working
                and tfw.in_application
            ]
        )

    @property
    def E(self):
        return len(
            [
                tfw
                for tfw in self.captfw
                if tfw.hourly_rate < self.lmiacase.provincial_median_wage
                and not tfw.is_working
            ]
        )

    @property
    def F(self):
        return len(
            [
                tfw
                for tfw in self.captfw
                if tfw.hourly_rate < self.lmiacase.provincial_median_wage
                and tfw.pr_in_process
            ]
        )

    @property
    def G(self):
        if self.F == 0:
            return 0
        g = self.F / (self.C + self.D)
        return "{:,.2f}".format(g)

    @property
    def H(self):
        h = float(self.G) * (self.C + self.D - self.F)
        return "{:,.2f}".format(h)

    @property
    def step1(self):
        step = (self.C + self.D + self.E) - (self.F + float(self.H))
        return "{:,.2f}".format(step)

    @property
    def step2(self):
        if self.A + self.B / 2 < 10:
            return 10
        step = self.A + self.B / 2 + self.E
        return "{:,.2f}".format(step)

    @property
    def step3(self):
        if float(self.step1) == 0:
            return 0
        step = float(self.step1) / float(self.step2)
        return "{:,.2f}".format(step)

    @property
    def step4(self):
        step = float(self.step3) * 100
        return "{:,.2f}".format(step)

    @property
    def result(self):
        return {
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "D": self.D,
            "E": self.E,
            "F": self.F,
            "G": self.G,
            "H": self.H,
            "step1": self.step1,
            "step2": self.step2,
            "step3": self.step3,
            "step4": self.step4,
        }


class CapModelE(CommonModel, CapModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/er.xlsx", "excel/lmia.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
