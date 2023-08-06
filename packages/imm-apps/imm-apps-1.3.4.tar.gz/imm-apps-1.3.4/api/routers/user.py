from basemodels.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from system.config import Default, db
import schemas
from api.hashing import Hash
from api import oauth2
from api import schemas

user_collection = db.user
router = APIRouter(
    prefix="/user", tags=["Users"], responses={404: {"description": "Nof found"}}
)


def email_existed(email: str):
    return user_collection.find_one({"email": email})


def is_admin(current_user: User):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The operation needs admin access right",
        )
    return True


@router.get("/")
async def read_users(current_user: User = Depends(oauth2.get_current_user)):
    users = list(user_collection.find())
    users1 = schemas.users_schema(users)
    return {"status_code": status.HTTP_200_OK, "data": users1}


@router.get("/{id}")
async def retrieve(id: str, current_user: User = Depends(oauth2.get_current_user)):
    user = user_collection.find_one({"_id": ObjectId(id)})
    return {"status_code": status.HTTP_200_OK, "data": schemas.user_schema(user)}


@router.post("/")
async def create(user: User):
    if email_existed(user.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"{user.email} is existed in the system.",
        )
    user.password = Hash.hash(user.password)
    user.permission.extend(Default.user_permission)
    new_id = user_collection.insert_one(user.dict()).inserted_id
    new_user = user_collection.find_one({"_id": new_id})
    return {"status_code": status.HTTP_200_OK, "data": schemas.user_schema(new_user)}


@router.put("/{id}")
async def update(
    id: str, user: User, current_user: User = Depends(oauth2.get_current_user)
):
    if user == current_user or is_admin(current_user):
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})
        updated_one = user_collection.find_one({"_id": ObjectId(id)})
        return {
            "status_code": status.HTTP_200_OK,
            "data": schemas.user_schema(updated_one),
        }


@router.put("/password/{id}")
async def password(
    id: str, password: str, current_user: User = Depends(oauth2.get_current_user)
):
    user = user_collection.find_one({"_id": ObjectId(id)})
    user["password"] = Hash.hash(password)
    if user["email"] == current_user["sub"] or is_admin(current_user):
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": user})
        updated_one = user_collection.find_one({"_id": ObjectId(id)})
        return {
            "status_code": status.HTTP_200_OK,
            "data": schemas.user_schema(updated_one),
        }


@router.delete("/{id}")
async def delete(id: str, current_user: User = Depends(oauth2.get_current_user)):
    is_admin(current_user)
    try:
        res = user_collection.delete_one({"_id": ObjectId(id)})
        if res.deleted_count > 0:
            return {"status_code": status.HTTP_204_NO_CONTENT, "data": []}
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": "Delete unseccessfully.",
        }
    except Exception as e:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": "Delete unseccessfully.",
        }


@router.post("/permission")
async def permission(
    request: schemas.Permission,
    current_user: User = Depends(oauth2.get_current_user),
):
    # print("In permission",type(current_user),current_user)
    is_admin(current_user)
    user = user_collection.find_one({"email": request.user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request.user_email} is not in the system",
        )

    # add permissions
    permissions = user["permission"]
    for permission in request.permissions:
        if request.remove:
            if permission in permissions:
                permissions.remove(permission)
        else:
            if permission not in permissions:
                permissions.append(permission)

    # update
    user_obj = User(**user)
    await update(user["_id"], user_obj)
    return {"permission": user.get("permission")}


@router.post("/role")
async def role(
    request: schemas.Role,
    current_user: User = Depends(oauth2.get_current_user),
):
    is_admin(current_user)
    user = user_collection.find_one({"email": request.user_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request.user_email} is not in the system",
        )

    # set role
    user["role"] = request.role
    # update
    user_obj = User(**user)
    await update(user["_id"], user_obj)
    return {"role": user.get("role")}
