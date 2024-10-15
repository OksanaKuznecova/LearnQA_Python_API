from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import random
import string


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    @allure.description("This test successfully updates just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_user = self.register_new_random_user()
        email = register_user['email']
        password = register_user['password']
        user_id = register_user['user_id']

        # LOGIN
        auth_user_data = self.login_user(email, password)

        # EDIT
        new_name = "Changed name"
        edit_user_response = MyRequests.put(
            url=f"/user/{user_id}",
            headers={"x-csrf-token": auth_user_data["token"]},
            cookies={"auth_sid": auth_user_data["auth_sid"]},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(edit_user_response, 200)

        # GET
        get_user_response = MyRequests.get(
            url=f"/user/{user_id}",
            headers={"x-csrf-token": auth_user_data["token"]},
            cookies={"auth_sid": auth_user_data["auth_sid"]}
        )

        Assertions.assert_json_value_by_name(
            get_user_response,
            "firstName",
            new_name,
            f"Wrong name of the user after edit"
        )

    @allure.description("This test updates just created user without authentication")
    def test_edit_just_created_user_not_auth(self):
        # REGISTER
        register_user = self.register_new_random_user()
        user_id = register_user['user_id']

        # EDIT
        new_user_name = "Changed user name"
        edit_user_response = MyRequests.put(
            url=f"/user/{user_id}",
            data={"username": new_user_name}
        )

        Assertions.assert_code_status(edit_user_response, 400)
        Assertions.assert_json_value_by_name(
            edit_user_response,
            "error",
            "Auth token not supplied",
            f"Unexpected response content '{edit_user_response.content}'")

    @allure.description("This test updates just created user with other user's authentication data")
    def test_edit_just_created_user_with_another_user_auth(self):
        # REGISTER FIRST USER
        register_first_user = self.register_new_random_user()
        first_user_id = register_first_user['user_id']

        # REGISTER SECOND USER
        register_second_user = self.register_new_random_user()
        second_user_email = register_second_user['email']
        second_user_password = register_second_user['password']

        # LOGIN WITH SECOND USER
        auth_second_user_data = self.login_user(second_user_email, second_user_password)
        second_user_token = auth_second_user_data["token"]
        second_user_auth_sid = auth_second_user_data["auth_sid"]

        # EDIT FIRST USER
        new_last_name = "Changed last name"
        edit_user_response = MyRequests.put(
            url=f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid},
            data={"lastName": new_last_name}
        )

        Assertions.assert_code_status(edit_user_response, 400)
        Assertions.assert_json_value_by_name(
            edit_user_response,
            "error",
            "This user can only edit their own data.",
            f"Unexpected response content '{edit_user_response.content}'")

    @allure.description("This test updates just created user with email in a wrong format")
    def test_edit_just_created_user_wrong_email_format(self):
        # REGISTER
        register_user = self.register_new_random_user()
        email = register_user['email']
        password = register_user['password']
        user_id = register_user['user_id']

        # LOGIN
        auth_user_data = self.login_user(email, password)
        token = auth_user_data["token"]
        auth_sid = auth_user_data["auth_sid"]

        # EDIT
        new_email = "some_random_email.google.com"
        edit_user_response = MyRequests.put(
            url=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(edit_user_response, 400)
        Assertions.assert_json_value_by_name(
            edit_user_response,
            "error",
            "Invalid email format",
            f"Unexpected response content '{edit_user_response.content}'")

    @allure.description("This test updates just created user with first name with one symbol length")
    def test_edit_just_created_user_short_first_name(self):
        # REGISTER
        register_user = self.register_new_random_user()
        email = register_user['email']
        password = register_user['password']
        user_id = register_user['user_id']

        # LOGIN
        auth_user_data = self.login_user(email, password)
        token = auth_user_data["token"]
        auth_sid = auth_user_data["auth_sid"]

        # EDIT
        new_first_name = random.choice(string.ascii_letters)
        edit_user_response = MyRequests.put(
            url=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(edit_user_response, 400)
        Assertions.assert_json_value_by_name(
            edit_user_response,
            "error",
            "The value for field `firstName` is too short",
            f"Unexpected response content '{edit_user_response.content}'")
