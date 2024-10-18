from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):
    @allure.description("This test tries to delete user not allowed for deletion")
    @allure.title("Test deleting user not allowed for deletion")
    @allure.severity("critical")
    @allure.tag("Negative", "Security")
    def test_user_delete_not_allowed(self):
        # LOGIN
        auth_user_data = self.login_user()
        auth_sid = auth_user_data["auth_sid"]
        token = auth_user_data["token"]
        user_id = auth_user_data["user_id"]

        # DELETE
        delete_user_response = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(delete_user_response, 400)
        Assertions.assert_json_value_by_name(
            delete_user_response,
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Unexpected response content '{delete_user_response.content}'")

    @allure.description("This test successfully deletes just created user")
    @allure.title("Test deleting user with correct authorization data")
    @allure.severity("blocker")
    @allure.tag("Positive", "Smoke")
    def test_user_delete_successfully(self):
        # REGISTER
        register_user = self.register_new_random_user()
        email = register_user['email']
        password = register_user['password']
        user_id = register_user['user_id']

        # LOGIN
        auth_user_data = self.login_user(email, password)
        auth_sid = auth_user_data["auth_sid"]
        token = auth_user_data["token"]
        user_id = auth_user_data["user_id"]

        # DELETE
        delete_user_response = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(delete_user_response, 200)
        Assertions.assert_json_value_by_name(
            delete_user_response,
            "success",
            "!",
            f"Unexpected response content '{delete_user_response.content}'")

        # GET
        get_user_response = MyRequests.get(
            url=f"/user/{user_id}",
            headers={"x-csrf-token": auth_user_data["token"]},
            cookies={"auth_sid": auth_user_data["auth_sid"]}
        )
        Assertions.assert_code_status(get_user_response, 404)
        assert get_user_response.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {get_user_response.content}"

    @allure.description("This test deletes just created user with other user's authentication data")
    @allure.title("Test deleting user with other user's authorization data")
    @allure.severity("critical")
    @allure.tag("Negative", "Security")
    def test_user_delete_auth_as_another_user(self):
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

        # Deleting just created user using auth info of another user
        delete_user_response = MyRequests.delete(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )
        Assertions.assert_code_status(delete_user_response, 400)
        Assertions.assert_json_value_by_name(
            delete_user_response,
            "error",
            "This user can only delete their own account.",
            f"Unexpected response content '{delete_user_response.content}'")
