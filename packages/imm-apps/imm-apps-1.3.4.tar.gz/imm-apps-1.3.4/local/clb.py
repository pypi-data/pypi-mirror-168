import context
from utils.language import CELPIP, IELTS, TEF, TCF, CLB
from datetime import date


def show(clb):
    print(
        clb.clb,
        clb.clb_r,
        clb.clb_w,
        clb.clb_s,
        clb.clb_l,
        clb.is_valid(),
        clb.test_date,
        clb.sign_date,
    )


ielts = {
    "reading": 6.5,
    "writting": 6.5,
    "speaking": 7,
    "listening": 6.5,
    "test_date": date.today(),
    "sign_date": date.today(),
    "type_of_test": "Academic",
    "report_number": "112233",
}
clb = IELTS(**ielts)

show(clb)
print(clb.type_of_test, clb.report_number)

celpip = {
    "reading": 6.5,
    "writting": 6,
    "speaking": 7,
    "listening": 6,
    "test_date": date.today(),
    "sign_date": date.today(),
    "registration_number": "123321",
    "pin_number": "112233",
}
clb = CELPIP(**celpip)
show(clb)
print(clb.registration_number, clb.pin_number)

tef = {
    "reading": 266,
    "writting": 333,
    "speaking": 288,
    "listening": 333,
    "test_date": date.today(),
    "sign_date": date.today(),
}
clb = TEF(**tef)
show(clb)

tcf = {
    "reading": 344,
    "writting": 20,
    "speaking": 20,
    "listening": 333,
    "test_date": date.today(),
    "sign_date": date.today(),
}
clb = TCF(**tcf)
show(clb)

clb = CLB(7)
print(clb.to_ielts(), clb.to_tcf())
