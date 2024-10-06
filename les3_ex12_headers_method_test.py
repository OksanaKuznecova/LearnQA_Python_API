import requests


class TestHeader:
    def test_header_value(self):
        # Defining URL to work with
        url = "https://playground.learnqa.ru/api/homework_header"

        # Sending the request
        response = requests.get(url=url)
        # Printing headers to understand what we have there
        print(response.headers)
        
        # Setting the expected header value
        expected_header_value = "Some secret value"
        # Checking there is a header before checking its value
        assert "x-secret-homework-header" in response.headers, "There is no x-secret-homework-header header " \
                                                               "in the response"

        # getting the actual header's value
        actual_header_value = response.headers.get("x-secret-homework-header")

        # Checking the actual header's value is correct
        assert actual_header_value == expected_header_value, f"The header value is incorrect. " \
                                                             f"The expected value is {expected_header_value}"
