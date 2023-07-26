import pytest

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


@pytest.mark.parametrize('parameter', [0,1,2,3,4,0,5,6,0])
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
