import pytest
from fastapi.testclient import TestClient

from app.schemas import Role
from app.utils import generate_users

# from app.main import app
# from app.utils import generate_users

# from fastapi import HTTPException
# from app.main import delete_user

pytestmark = [pytest.mark.str]


# class TestEndpoints():
#     def test_get_all_users_pass(self):
#         with pytest.raises(HTTPException):
#             assert delete_user(2)

@pytest.mark.xfail(reason="known issue ------------------")
def test_1():
    assert 1 / 0


@pytest.mark.parametrize('parameter', [0, 1, 2, 3, 4, 0, 5, 6, 0])
@pytest.mark.test
def test_g2(parameter):
    with pytest.raises(Exception):
        assert 1 / parameter


@pytest.mark.test
def test_3():
    with pytest.raises(Exception):
        assert 1 / 0


@pytest.mark.str
def test_str1():
    assert 5 + 5 == 10


@pytest.mark.str
def test_str2():
    assert 1 + 5 == 6


@pytest.mark.str
def test_str3():
    assert 5 + 5 == 10


# def cent_to_far(cent=0):
#     const = 9/5
#     fah = (cent * const) + 32
#     return fah
#
# #by decorating the test function with @pytest.mark.name, I can later use that name in the cmd to execute all tests marked with that decorator.
# @pytest.mark.sanity
# def test_cent_to_far():
#     assert cent_to_far(40) == 104.0


@pytest.fixture(scope="module")
def test_client():
    # Use TestClient to make requests to your FastAPI application
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_database():
    # Set up your test database here (e.g., using an in-memory database or a temporary database)
    # Initialize the test database
    yield


@pytest.mark.api
def test_get_all_users(test_client):
    print(str(test_client.scope))
    response = test_client.get("/users")
    assert response.status_code == 200


# @pytest.mark.parametrize('users',[{
#         "email": "test1@example.com",
#         "first_name": "John",
#         "last_name": "Doe",
#         "password": "testpassword",
#         "role": "user",
#         "gender": "male",
#         "date_of_birth": "1990-01-01",
#     },
#     {
#         "email": "test2@example.com",
#         "first_name": "John",
#         "last_name": "Doe",
#         "password": "testpassword",
#         "role": "user",
#         "gender": "male",
#         "date_of_birth": "1990-01-01",
#     }
# ,
#     {
#         "email": "test3@example.com",
#         "first_name": "John",
#         "last_name": "Doe",
#         "password": "testpassword",
#         "role": "user",
#         "gender": "male",
#         "date_of_birth": "1990-01-01",
#     }
# ])

# @pytest.mark.parametrize('parameter', [0, 1, 2, 3, 4, 0, 5, 6, 0])
# @pytest.mark.generate_users
# def test_generate_users(parameter):
#     users = generate_users(parameter)
#     print(users.__len__())
#     # print(users)
#     assert users.__len__() == parameter


@pytest.mark.parametrize('parameter', [1, 2, 3, 4, 5, 6])
@pytest.mark.generate_users
def test_generate_users(parameter):
    users = generate_users(parameter)
    print(users.__len__())
    # print(users)
    for user in range(users.__len__()):
        print(f'loop: {user}')
        assert users.__len__() == parameter
        assert users[user].email is not None
        assert users[user].first_name is not None
        assert users[user].last_name is not None
        assert users[user].date_of_birth is not None
        assert users[user].role is not None
        assert isinstance(users[user].role, Role)
        assert users[user].password is not None


@pytest.mark.parametrize('parameter', [-1, -2, -3, -4, -5, -6])
@pytest.mark.xfail(reason="Negative numbers provided.")
@pytest.mark.generate_users
def test_generate_users_fail(parameter):
    users = generate_users(parameter)
    # print(users.__len__())
    # print(users)
    assert users.__len__() == parameter


@pytest.mark.parametrize('parameter', [-1, -2, -3, -4, -5, -6])
@pytest.mark.xfail(reason="Negative numbers provided, assertion exception checked.")
@pytest.mark.generate_users
def test_generate_users_pass(parameter):
    with pytest.raises(AssertionError):
        users = generate_users(parameter)
        # print(users.__len__())
        # print(users)
        assert users.__len__() == parameter
