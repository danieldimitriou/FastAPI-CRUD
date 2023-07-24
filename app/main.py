from typing import List, Dict
from fastapi import FastAPI, APIRouter
from database import init_db
from models import UserCreate, UserInDB, UserOut

app = FastAPI()

router = APIRouter()


@router.on_event("startup")
async def start_db():
    """Initiate the database connection."""
    await init_db()


@router.get("/users", response_model=List[UserOut])
async def get_all_users() -> List[UserOut]:
    """Get all users. Returns a List with User objects or an empty list if no data is available."""
    users_cursor = UserInDB.find()
    users = await users_cursor.to_list(length=None)
    print(users)
    users_out_list = []
    for user in users:
        users_out_list.append(UserOut(**user.dict()))
    return users_out_list



@router.post("/users")
async def create_user(user: UserCreate):
    """ Create a user. Returns the user data from the database after saving said user, including the newly
    created ID."""
    user_in_db = UserInDB(**user.dict())
    db_user = await user_in_db.insert()
    user_out_data = db_user.dict(exclude={'id'})
    user_out = UserOut(id=str(db_user.id), **user_out_data)

    return {"created_user": user_out}


# # GET USERS BY EMAIL
# @router.get("/users/{user_email}")
# async def update_user(user_email: str):
#     # get a list of users that satisfy the condition(userindb.email == user_email)
#     users = await UserInDB.find(UserInDB.email == user_email).to_list()
#     # iterate through the list and create a UserOut object for each entry
#     users_out = [UserOut(**user.__dict__) for user in users]
#     return users_out


@router.get("/users/{doc_id}", response_model=UserOut)
async def update_user(doc_id: str):
    """Get user by ID."""
    # get a user that satisfies the condition(userInDB.id == user_id)
    user = await UserInDB.get(doc_id)
    print(user)
    user_out = UserOut(**user.dict())
    # iterate through the list and create a UserOut object for each entry
    return user_out


@router.patch("/users/{doc_id}", response_model=UserOut)
async def update_user(doc_id: str):
    """Update a user entry by ID."""
    # get a user that satisfies the condition(userInDB.id == user_id)
    user = await UserInDB.get(doc_id)
    print(user)
    user_out = UserOut(**user.dict())
    # iterate through the list and create a UserOut object for each entry
    return user_out


app.include_router(router)
