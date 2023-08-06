from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from system.config import db
from api.hashing import Hash
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import Union

user_collection = db.user

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
    responses={404: {"description": "Nof found"}},
)


@router.post("/")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": request.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{request.username} is not registered in the system.",
        )
    if not Hash.verify(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Password is incorrect"
        )

    access_token = create_access_token(
        data={
            "sub": user["email"],
            "role": user.get("role"),
            "permission": user.get("permission"),
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
