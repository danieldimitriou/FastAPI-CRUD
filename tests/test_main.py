import asyncio
import json
from typing import List
import pytest

# from beanie.exceptions import
pytestmark = [pytest.mark.endpoint]


# GET ALL USERS
@pytest.mark.endpoint
@pytest.mark.anyio
async def test_get_all_users(test_client, initialized_db):
    # First, populate the database with some test data
    # Assuming you have a /populate endpoint that can be used to insert dummy data

    await test_client.get("/populate?count=10")
    loop = asyncio.new_event_loop()
    response = await test_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    print(response.json())
    # because the data is auto-generated, perform a basic check that all the fields are not null/empty
    for user_data in response.json():
        assert user_data["email"] is not None
        assert user_data["_id"] is not None
        assert user_data["first_name"] is not None
        assert user_data["last_name"] is not None
        assert user_data["password"] is not None
        assert user_data["role"] is not None
        assert user_data["date_of_birth"] is not None


# DELETE ALL USERS
@pytest.mark.endpoint
@pytest.mark.anyio
async def test_delete_all_users(test_client, initialized_db):
    await test_generate_users_endpoint(10, test_client, initialized_db)
    response = await test_client.delete("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "All users have been deleted."}


# Check that the response is correct when trying to delete all users but the DB is empty.
@pytest.mark.endpoint
@pytest.mark.anyio
async def test_delete_all_users_404(test_client, initialized_db):
    # first delete all users, then try to delete again.
    await test_client.delete("/users")
    response = await test_client.delete("/users")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users were found."}


# XFAIL
@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.xfail
async def test_delete_all_users_xfail(test_client, initialized_db):
    # first delete all users, then try to delete again.
    await test_client.delete("/users")
    response = await test_client.delete("/users")
    assert response.status_code == 200
    assert response.json() == {"detail": "No users were found."}


# CREATE USER
@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "email": "email@gmail.com",
        "first_name": "first",
        "last_name": "last",
        "password": "strong_password",
        "role": "user",
        "gender": "male",
        "date_of_birth": "2022-12-12"
    }
])
async def test_create_user(user, test_client, initialized_db):
    created_user = await test_client.post("users", data=json.dumps(user))
    # Check that all the users attributes are returned + the generated ID, and that the status code is 201(created)
    for attr in user:
        print(user)
        print(created_user.json())
        assert user[attr] in created_user.json()[attr]
    assert "_id" in created_user.json()
    assert created_user.status_code == 201


# GENERATE USERS ENDPOINT
@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize('count', [1, 2, 3])
async def test_generate_users_endpoint(count, test_client, initialized_db):
    returned_users_data = await test_client.get(f"/populate?count={count}")
    assert len(returned_users_data.json()) == count


# DELETE USER BY ID
@pytest.mark.endpoint
@pytest.mark.anyio
async def test_delete_user_by_id(test_client, initialized_db):
    # Populate the DB and get the newly created users IDs in order to test the delete function
    returned_users_data = await test_client.get("/populate?count=10")
    list_of_ids = []
    for user in returned_users_data.json():
        list_of_ids.append(user["_id"])

    # Delete each user by their ID, and ensure that the response is as expected.
    for user_id in list_of_ids:
        rsp = await test_client.delete(f"/users/{user_id}")
        assert rsp.status_code == 200
        assert rsp.json() == {"message": "User deleted successfully"}


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "email": "email@gmail.com",
        "first_name": "first",
        "last_name": "last",
        "password": "strong_password",
        "role": "user",
        "gender": "male",
        "date_of_birth": "2022-12-12"
    }
])
async def test_get_user_by_email(user, test_client, initialized_db):
    # Populate the DB and get the newly created users IDs in order to test the delete function
    returned_user_data = await test_client.post("users", data=json.dumps(user))
    print(returned_user_data.json())
    response = await test_client.get(f'user?email={user["email"]}')
    print(response.json())
    assert response.status_code == 200
    for attr in user:
        assert user[attr] in response.json()[attr]


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "email": "email@gmail.com",
        "first_name": "first",
        "last_name": "last",
        "password": "strong_password",
        "role": "user",
        "gender": "male",
        "date_of_birth": "2022-12-12"
    }
])
async def test_get_user_by_id(user, test_client, initialized_db):
    created_user = await test_client.post("users", data=json.dumps(user))
    print(created_user.json())
    response = await test_client.get(f'users/{created_user.json()["_id"]}')
    assert response.status_code == 200
    print(user)
    print(response.json())
    for attr in user:
        assert user[attr] in response.json()[attr]


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "email": "email@gmail.com",
        "first_name": "first",
        "last_name": "last",
        "password": "strong_password",
        "role": "user",
        "gender": "male",
        "date_of_birth": "2022-12-12"
    }
])
@pytest.mark.parametrize("updated_user", [
    {
        "email": "updatedemail@gmail.com",
        "first_name": "updated_first",
        "last_name": "updated_last",
        "password": "updated_strong_password",
        "role": "admin",
        "gender": "female",
        "date_of_birth": "2023-12-12"
    }
])
async def test_update_user(user, updated_user, test_client, initialized_db):
    # Create a new user, then update the user and ensure that the updated data is returned correctly in the response.
    created_user = await test_client.post("/users", data=json.dumps(user))
    print(created_user.json())
    updated_user_data = await test_client.patch(f'/users/{created_user.json()["_id"]}', data=json.dumps(updated_user))
    print(updated_user_data.json())
    for attr in updated_user:
        assert updated_user[attr] == updated_user_data.json()[attr]

# -----------------------------------------------------------------------------------
#   Test the random user generator helper function
# @pytest.mark.parametrize('parameter', [0, 1, 2, 3, 4, 0, 5, 6, 0])
# @pytest.mark.generate_users
# def test_generate_users(parameter):
#     users = generate_users(parameter)
#     print(users.__len__())
#     # print(users)
#     assert users.__len__() == parameter

#
# @pytest.mark.parametrize('parameter', [1, 2, 3, 4, 5, 6])
# @pytest.mark.generate_users
# def test_generate_users(parameter):
#     users = generate_users(parameter)
#     print(users.__len__())
#     # print(users)
#     for user in range(users.__len__()):
#         print(f'loop: {user}')
#         assert users.__len__() == parameter
#         assert users[user].email is not None
#         assert users[user].first_name is not None
#         assert users[user].last_name is not None
#         assert users[user].date_of_birth is not None
#         assert users[user].role is not None
#         assert isinstance(users[user].role, Role)
#         assert users[user].password is not None
#
#
# @pytest.mark.parametrize('parameter', [-1, -2, -3, -4, -5, -6])
# @pytest.mark.xfail(reason="Negative numbers provided.")
# @pytest.mark.generate_users
# def test_generate_users_fail(parameter):
#     users = generate_users(parameter)
#     # print(users.__len__())
#     # print(users)
#     assert users.__len__() == parameter
#
#
# @pytest.mark.parametrize('parameter', [-1, -2, -3, -4, -5, -6])
# @pytest.mark.xfail(reason="Negative numbers provided, assertion exception checked.")
# @pytest.mark.generate_users
# def test_generate_users_pass(parameter):
#     with pytest.raises(AssertionError):
#         users = generate_users(parameter)
#         # print(users.__len__())
#         # print(users)
#         assert users.__len__() == parameter
