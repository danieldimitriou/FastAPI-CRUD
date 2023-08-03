from typing import Annotated, List

from beanie import PydanticObjectId
from fastapi import HTTPException, Path, Query, APIRouter
from pymongo.errors import DuplicateKeyError
from api.database import init_db
from api.utils import generate_users
from api.models import UserInDB
from api.schemas import UserUpdate, UserCreate

router = APIRouter()


@router.on_event("startup")
async def start_db():
    """Initiate the database connection."""
    await init_db()


@router.get("/users", response_model=list[UserInDB], status_code=200, tags=["users"])
async def get_all_users() -> list[UserInDB]:
    """Get all users. Returns a List with User objects or an empty list if no data is available."""
    try:
        users_cursor = UserInDB.find()
        users = await users_cursor.to_list(length=None)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching users from the database. Please try again. Error message: {e}"
        )

    return users


@router.post("/users", response_model=UserInDB, status_code=201, tags=["users"])
async def create_user(user: UserCreate) -> UserInDB:
    """ Create a user. Returns the user data from the database after saving said user, including the newly
    created ID."""
    try:
        user_in_db = UserInDB(**user.dict())
        db_user = await user_in_db.insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="There is already a user with this email. "
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while persisting the user to the database. Please try again."
        )

    # user_out_data = db_user.dict(exclude={'id'})
    if db_user:
        return db_user
    else:
        raise HTTPException(
            status_code=500, detail="Could not create user. Please try again."
        )


@router.delete("/users/{doc_id}", status_code=200, tags=["users"])
async def delete_user(doc_id: Annotated[PydanticObjectId, Path(title="The ID of the user that will be deleted.")]):
    user = await UserInDB.get(doc_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    deleted_user = await user.delete()
    if not deleted_user:
        raise HTTPException(status_code=500, detail="Failed to delete user. Please try again.")

    return {"message": "User deleted successfully"}


@router.delete("/users", status_code=200, tags=["users"])
async def delete_all_users():
    all_users = await UserInDB.find_all().to_list()
    # Delete each user one by one (optional)
    if all_users:
        for user in all_users:
            await user.delete()

        # Alternatively, you can delete all users in a single operation (recommended)
        # await UserInDB.delete_many({})

        return {"message": "All users have been deleted."}
    raise HTTPException(
        status_code=404,
        detail="No users were found."
    )


# GET USERS BY EMAIL
@router.get("/user", response_model=UserInDB, status_code=200, tags=["users"])
async def get_by_email(email: Annotated[str, Query(title="The email of the user to fetch.")]) -> UserInDB:
    # get a list of users that satisfy the condition(userindb.email == user_email)
    try:
        user = await UserInDB.find_one(UserInDB.email == email)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occurred while fetching the data from the database. Please try again.")
    if not user:
        raise HTTPException(status_code=404, detail=f"user with email: {email} not found.")
    # iterate through the list and create a UserOut object for each entry

    return user


@router.get("/users/{doc_id}", response_model=UserInDB, status_code=200, tags=["users"])
async def get_user_by_id(
        doc_id: Annotated[PydanticObjectId, Path(title="The ID of the document to retrieve.")]
) -> UserInDB:
    """Get user by ID."""
    # get a user that satisfies the condition(userInDB.id == user_id)
    print(type(doc_id))
    if not isinstance(doc_id, PydanticObjectId):
        raise HTTPException(status_code=404, detail="Please provide a correct ID for the user.")
    try:
        user = await UserInDB.get(doc_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occurred while fetching the data from the database. Please try again.")


@router.get("/populate", response_model=List[UserInDB], status_code=201, tags=["populate"])
async def populate_db(
        count: Annotated[int, Query(title="Count represents the number of entries the DB will be populated with.")]
) -> List[UserInDB]:
    """Populate the database with dummy data. Through Query parameters the user can decide the amount
    of users to populate the db with."""
    users_create = generate_users(count)
    users_out = []
    for user in users_create:
        db_user = await UserInDB(**user.dict()).insert()
        user_out_data = db_user.dict(exclude={'id'})
        users_out.append(db_user)
    return users_out


@router.patch("/users/{doc_id}", response_model=UserInDB, status_code=200, tags=["users"])
async def update_user(doc_id: PydanticObjectId, user_update: UserUpdate) -> UserInDB:
    print(user_update)
    """Update a user entry by ID."""
    user = await UserInDB.get(doc_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict(exclude_unset=True).items():
        print(field, value)
        setattr(user, field, value)

    await user.save()
    return user
