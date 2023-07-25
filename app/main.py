from typing import List, Dict, Annotated
from uuid import UUID
from faker import Faker
from fastapi import FastAPI, APIRouter, Query, Path, HTTPException
from utils import Role
from database import init_db
from models import UserInDB
from schemas import UserCreate, UserOut, UserUpdate
from fastapi.middleware.cors import CORSMiddleware


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


@router.delete("/users/{user_id}")
async def delete_user(user_id: Annotated[UUID, Path(title="The ID of the user that will be deleted.")]):
    user = await UserInDB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = await user.delete()
    if deleted:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete user")


# # GET USERS BY EMAIL
# @router.get("/users/{user_email}")
# async def update_user(user_email: Annotated[str, Path(title="The email of the user to fetch.")]):
#     # get a list of users that satisfy the condition(userindb.email == user_email)
#     users = await UserInDB.find(UserInDB.email == user_email).to_list()
#     # iterate through the list and create a UserOut object for each entry
#     users_out = [UserOut(**user.__dict__) for user in users]
#     return users_out


@router.get("/users/{doc_id}", response_model=UserOut)
async def get_user_by_id(
        doc_id: Annotated[str, Path(title="The ID of the document to retrieve.")]
):
    """Get user by ID."""
    # get a user that satisfies the condition(userInDB.id == user_id)
    user = await UserInDB.get(doc_id)
    print(user)
    user_out = UserOut(**user.dict())
    # iterate through the list and create a UserOut object for each entry
    return user_out


@router.get("/populate")
async def populate_db(
        count: Annotated[int, Query(title="Count represents the number of entries the DB will be populated with.")]
):
    """Populate the database with dummy data. Through Query parameters the user can decide the amount
     of users to populate the db with."""
    faker = Faker()
    users_out = []
    for _ in range(count):
        email = faker.email()
        first_name = faker.first_name()
        last_name = faker.last_name()
        password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        role = faker.random_element(elements=(Role.user, Role.admin))
        gender = faker.random_element(elements=("male", "female"))
        date_of_birth = faker.date_of_birth(minimum_age=18, maximum_age=70)
        user = UserCreate(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            gender=gender,
            date_of_birth=date_of_birth,
        )
        db_user = await UserInDB(**user.dict()).insert()
        user_out_data = db_user.dict(exclude={'id'})
        user_out = UserOut(id=str(db_user.id), **user_out_data)
        users_out.append(user_out)
    return users_out


@router.patch("/users/{doc_id}", response_model=UserOut)
async def update_user(doc_id: UUID, user_update: UserUpdate):
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
