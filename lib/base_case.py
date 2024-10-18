from datetime import datetime
import json.decoder
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from requests import Response


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response not in JSON format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S%f")
            email = f"{base_part}{random_part}@{domain}"
        return {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email}

    def login_user(self, email="vinkotov@example.com", password="1234"):
        data = {
            "email": email,
            "password": password
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")
        return {
            "auth_sid": auth_sid,
            "token": token,
            "user_id": user_id
        }

    def register_new_random_user(self):
        register_data = self.prepare_registration_data()
        register_user_response = MyRequests.post("/user", data=register_data)
        Assertions.assert_code_status(register_user_response, 200)
        Assertions.assert_json_has_key(register_user_response, "id")
        return {
            "user_id": self.get_json_value(register_user_response, "id"),
            "email": register_data['email'],
            "password": register_data['password']
        }
