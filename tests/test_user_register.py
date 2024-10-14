import pytest
import random
import string
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    exclude_user_fields = [
        ("username"),
        ("password"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.description("This test successfully registers new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test doesn't allow registering a new user with existing user's email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("This test doesn't allow registering a new user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = "some.random.user.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.description("This test checks registering a new user with missing params")
    @pytest.mark.parametrize("user_field", exclude_user_fields)
    def test_create_user_with_missing_param(self, user_field):
        data = self.prepare_registration_data()
        data.pop(user_field)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {user_field}", \
            f"Unexpected response content '{response.content}'"

    @allure.description("This test checks registering user with a short one symbol length username")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        username = random.choice(string.ascii_letters)
        data.update({"username": username})
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content '{response.content}'"

    @allure.description("This test checks registering user with a long username > 250 symbols")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        username = ''.join(random.choice(string.ascii_letters) for x in range(251))
        data.update({"username": username})
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"Unexpected response content '{response.content}'"
