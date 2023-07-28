import uuid
from fastapi import FastAPI, APIRouter, Query, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Annotated
from uuid import UUID

from database import init_db
from models import UserInDB
from schemas import UserCreate, UserOut, UserUpdate, Role
from utils import generate_users

app = FastAPI()
router = APIRouter()
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.on_event("startup")
async def start_db():
    """Initiate the database connection."""
    await init_db()


@router.get("/users", response_model=List[UserOut], status_code=200)
async def get_all_users() -> List[UserOut]:
    """Get all users. Returns a List with User objects or an empty list if no data is available."""
    try:
        users_cursor = UserInDB.find()
        users = await users_cursor.to_list(length=None)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occured while fetching users from the database. Please try again.{e}")

    users_out_list = []
    for user in users:
        print(user.id)
        users_out_list.append(UserOut(**user.dict()))
    return users_out_list


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate) -> UserOut:
    """ Create a user. Returns the user data from the database after saving said user, including the newly
    created ID."""

    try:
        user_in_db = UserInDB(**user.dict())
        db_user = await user_in_db.insert()
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occured while persisting the user to the database. Please try again.")
    user_out_data = db_user.dict(exclude={'id'})
    user_out = UserOut(id=str(db_user.id), **user_out_data)
    if user_out:
        return user_out
    else:
        raise HTTPException(status_code=500, detail="Could not create user. Please try again.")


@router.delete("/users/{doc_id}", status_code=200)
async def delete_user(doc_id: Annotated[UUID, Path(title="The ID of the user that will be deleted.")]):
    user = await UserInDB.get(doc_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = await user.delete()
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    return {"message": "User deleted successfully"}


@router.delete("/users", status_code=200)
async def delete_all_users():
    all_users = await UserInDB.find_all().to_list()

    # Delete each user one by one (optional)
    for user in all_users:
        await user.delete()

    # Alternatively, you can delete all users in a single operation (recommended)
    # await UserInDB.delete_many({})

    return {"message": "All users have been deleted."}


# GET USERS BY EMAIL
@router.get("/user", response_model=UserOut, status_code=200)
async def get_by_email(email: Annotated[str, Query(title="The email of the user to fetch.")]) -> UserOut:
    # get a list of users that satisfy the condition(userindb.email == user_email)
    try:
        user = await UserInDB.find_one(UserInDB.email == email)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occured while fetching the data from the database. Please try again.")
    if not user:
        raise HTTPException(status_code=404, detail=f"user with email: {email} not found.")
    # iterate through the list and create a UserOut object for each entry
    user_out = UserOut(**user.__dict__)
    return user_out


@router.get("/users/{doc_id}", response_model=UserOut, status_code=200)
async def get_user_by_id(
        doc_id: Annotated[UUID, Path(title="The ID of the document to retrieve.")]
) -> UserOut:
    """Get user by ID."""
    # get a user that satisfies the condition(userInDB.id == user_id)
    print(type(doc_id))
    print(isinstance(doc_id, uuid.UUID))
    if not isinstance(doc_id, uuid.UUID):
        raise HTTPException(status_code=404, detail="Please provide a correct UUID for the user.")
    try:
        user = await UserInDB.get(doc_id)
        user_out = UserOut(**user.dict())
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occured while fetching the data from the database. Please try again.")
    return user_out


@router.get("/populate", response_model=List[UserOut], status_code=201)
async def populate_db(
        count: Annotated[int, Query(title="Count represents the number of entries the DB will be populated with.")]
) -> List[UserOut]:
    """Populate the database with dummy data. Through Query parameters the user can decide the amount
     of users to populate the db with."""
    users_create = generate_users(count)
    users_out = []
    for user in users_create:
        db_user = await UserInDB(**user.dict()).insert()
        user_out_data = db_user.dict(exclude={'id'})
        user_out = UserOut(id=str(db_user.id), **user_out_data)
        print(user_out.id)
        users_out.append(user_out)
    return users_out


@router.patch("/users/{doc_id}", response_model=UserOut, status_code=200)
async def update_user(doc_id: UUID, user_update: UserUpdate) -> UserOut:
    print(user_update)
    """Update a user entry by ID."""
    user = await UserInDB.get(doc_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict(exclude_unset=True).items():
        print(field, value)
        setattr(user, field, value)

    await user.save()
    return UserOut(id=str(user.id), **user.dict(exclude={'id'}))


app.include_router(router)
