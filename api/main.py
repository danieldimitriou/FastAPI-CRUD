import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import router

tags_metadata = [
    {
        "name": "users",
        "description": "All CRUD endpoints for the User entity."
    },
    {
        "name": "populate",
        "description": "A separate endpoint to populate the database with dummy user data."
    }
]

description = """
Daniel's Dummy API helps you do awesome stuff. 🚀

## Users

You will be able to:

* **Create users** (either individually by providing the data or by using an endpoint that uses dummy data to create the users).
* **Read users**.
* **Update users**.
* **Delete users**.
"""

app = FastAPI(
    title="Daniel's API",
    description=description,
    summary="An API for testing purposes.",
    version="0.0.1",
    contact={
        "name": "Daniel",
        "url": "https://github.com/danieldimitriou",
        "email": "danieldimitriou1@gmail.com",
    },
    openapi_tags=tags_metadata
)

app.include_router(router)
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
