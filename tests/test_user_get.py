from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User get cases")
class TestUserGet(BaseCase):
    @allure.description("This test gets details returned for the non-authorized user")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test successfully gets details of the authorized user")
    def test_get_user_details_auth_as_same_user(self):
        auth_user_data = self.login_user()
        response2 = MyRequests.get(
            f"/user/{auth_user_data['user_id']}",
            headers={"x-csrf-token": auth_user_data["token"]},
            cookies={"auth_sid": auth_user_data["auth_sid"]}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test gets details for some user with another user's authorization info")
    def test_get_user_details_auth_as_another_user(self):
        # Login with some known user
        auth_user_data = self.login_user()
        token = auth_user_data["token"]
        auth_sid = auth_user_data["auth_sid"]

        # Register another user
        register_user = self.register_new_random_user()
        new_user_id = register_user['user_id']

        # Getting data for just created user using auth info of another user
        response2 = MyRequests.get(
            f"/user/{new_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_user_auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")