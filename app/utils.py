from typing import List
from faker import Faker
# from schemas import UserOut, UserCreate, Role
from app.schemas import UserOut, UserCreate, Role


def generate_users(count: int) -> List[UserCreate]:
    faker = Faker()
    users_create = []
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
        users_create.append(user)
    return users_create
