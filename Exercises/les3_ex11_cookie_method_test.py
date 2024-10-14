import requests


class TestCookie:
    def test_cookie_value(self):
        # Defining URL to work with
        url = "https://playground.learnqa.ru/api/homework_cookie"

        # Sending the request
        response = requests.get(url=url)
        # Printing cookies to understand what we have there
        print(response.cookies)

        # Setting the expected cookie value
        expected_cookie_value = "hw_value"
        # Checking there is a cookie before checking its value
        assert "HomeWork" in response.cookies, "There is no HomeWork cookie in the response"

        # getting the actual cookie value
        actual_cookie_value = response.cookies.get("HomeWork")

        # Checking the actual cookie value is correct
        assert actual_cookie_value == expected_cookie_value, f"The cookie value is incorrect. " \
                                                             f"The expected value is {expected_cookie_value}"
