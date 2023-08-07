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


@router.get("/users", response_model=list[UserInDB], status_code=200, operation_id="get_all_users", responses={
    500: {"description": "Internal Server Error",
          "content": {
              "application/json": {
                  "example": {
                      "detail": "An internal error occurred while fetching the data from the database. Please try again."}
              }
          },
          }
})
async def get_all_users() -> list[UserInDB]:
    """Get all users. Returns a List with User objects or an empty list if no data is available."""
    try:
        users_cursor = UserInDB.find()
        users = await users_cursor.to_list(length=None)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while fetching the data from the database. Please try again."
        )

    return users


@router.get("/users/{doc_id}", response_model=UserInDB, status_code=200, operation_id="get_user_by_id", responses={
    404: {"description": "User not found.", "content": {
        "application/json": {
            "example": {
                "detail": "The ID provided does not match any users in the database."}
        }
    }},
    500: {"description": "Internal Server Error.", "content": {
        "application/json": {
            "example": {
                "detail": "An internal error occurred while fetching the data from the database. Please try again."}
        }
    }}
})
async def get_user_by_id(
        doc_id: Annotated[
            PydanticObjectId, Path(alias="Document ID", description="The document ID of the user to fetch.")]
) -> UserInDB:
    """Get user by ID.
    Fetches a user from the database given the correct document ID.
    Returns 404 if there is no match and 500 for any other issues. """
    print(type(doc_id))
    if not isinstance(doc_id, PydanticObjectId):
        raise HTTPException(status_code=404, detail="The ID provided does not match any users in the database.")
    try:
        user = await UserInDB.get(doc_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An internal error occurred while fetching the data from the database. Please try "
                                   "again.")


# GET USERS BY EMAIL
@router.get("/user", response_model=UserInDB, status_code=200, operation_id="get_by_email", responses={
    404: {"description": "User not found", "content": {
        "application/json": {
            "example": {
                "detail": "The ID provided does not match any users in the database."}
        }
    }},
    500: {"description": "Internal Server Error", "content": {
        "application/json": {
            "example": {
                "detail": "An internal error occurred while fetching the data from the database. Please try again."}
        }
    }}
}
            )
async def get_by_email(email: Annotated[str, Query(title="The email of the user to fetch.")]) -> UserInDB:
    """Get a user by their email."""
    try:
        user = await UserInDB.find_one(UserInDB.email == email)
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occurred while fetching the data from the database. Please try again.")

    if not user:
        raise HTTPException(status_code=404, detail=f"user with email: {email} not found.")

    return user


@router.post("/users", response_model=UserInDB, status_code=201, operation_id="create_user", responses={
    500: {"description": "Internal Server Error", "content": {
        "application/json": {
            "example": {
                "detail": "An internal error occurred while fetching the data from the database. Please try again."}
        }}},
    409: {"description": "Conflict", "content": {
        "application/json": {
            "example": {
                "detail": "There is already a user with this email."}
        }
    }}
}
             )
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


@router.delete("/users/{doc_id}", status_code=200, operation_id="delete", responses={
    200: {"description": "Successful Response", "content": {
        "application/json": {
            "example": {
                "message": "User deleted successfully"}
        }
    }},
    404: {"description": "User not found", "content": {
        "application/json": {
            "example": {
                "detail": "The ID provided does not match any users in the database."}
        }
    }},
    500: {"description": "Internal Server Error", "content": {
        "application/json": {
            "example": {
                "detail": "An internal error occurred while fetching the data from the database. Please try again."}
        }
    }}
}
               )
async def delete_user(doc_id: Annotated[
    PydanticObjectId, Path(alias="Document ID", description="The document ID of the user that will be deleted.")]):
    user = await UserInDB.get(doc_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    deleted_user = await user.delete()
    if not deleted_user:
        raise HTTPException(status_code=500, detail="Failed to delete user. Please try again.")

    return {"message": "User deleted successfully"}


@router.delete("/users", status_code=200, operation_id="",
               description="Delete all users from the database.", responses={
        200: {"description": "Successful Response", "content": {
            "application/json": {
                "example": {
                    "message": "All users have been deleted successfully"}
            }
        }},
        404: {"description": "User not found", "content": {
            "application/json": {
                "example": {
                    "detail": "No users were found. The database is empty."}
            }
        }},
        500: {"description": "User not found", "content": {
            "application/json": {
                "example": {
                    "detail": "An internal error occurred while fetching the data from the database. Please try again."}
            }
        }}
    })
async def delete_all_users():
    all_users = await UserInDB.find_all().to_list()
    # Delete each user one by one (optional)
    if all_users:
        try:
            for user in all_users:
                await user.delete()

            return {"message": "All users have been deleted successfully"}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="An internal error occurred while fetching the data from the database. Please try again."
            )
    else:
        raise HTTPException(status_code=404, detail="No users were found. The database is empty.")


@router.get("/populate", response_model=List[UserInDB], status_code=201,
            description="Create users in the database with dummy data.", responses={
        200: {"description": "Successful Response", "content": {
            "application/json": {
                "example": {
                    "message": "All users have been deleted successfully"}
            }
        }},
        500: {"description": "User not found", "content": {
            "application/json": {
                "example": {
                    "detail": "An internal error occurred while fetching the data from the database. Please try again."}
            }
        }}})
async def populate_db(
        count: Annotated[int, Query(title="Count represents the number of entries the DB will be populated with.")]
) -> List[UserInDB]:
    """Populate the database with dummy data. Through Query parameters the user can decide the amount
    of users to populate the db with."""
    users_create = generate_users(count)
    users_out = []
    try:
        for user in users_create:
            db_user = await UserInDB(**user.dict()).insert()
            user_out_data = db_user.dict(exclude={'id'})
            users_out.append(db_user)
        return users_out
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,
                            detail="An internal error occurred while fetching the data from the database. Please try again.")


@router.patch("/users/{doc_id}", response_model=UserInDB, status_code=200, tags=["Users"])
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
