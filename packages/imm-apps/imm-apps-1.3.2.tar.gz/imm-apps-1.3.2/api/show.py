from pydantic import ValidationError
from fastapi import HTTPException
from utils.utils import print_validation_error


def show_exception(e: Exception):
    if type(e) == ValidationError:
        raise HTTPException(status_code=422, detail=print_validation_error(e))
    else:
        raise HTTPException(status_code=422, detail=e)
