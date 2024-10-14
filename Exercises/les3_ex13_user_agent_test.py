import requests
import pytest


class TestUserAgent:
    user_agent_list = (
        {
            "user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "platform": "Mobile", "browser": "No", "device": "Android"},
        {
            "user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "platform": "Mobile", "browser": "Chrome", "device": "iOS"},
        {"user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         "platform": "Googlebot", "browser": "Unknown", "device": "Unknown"},
        {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "platform": "Web", "browser": "Chrome", "device": "No"},
        {
            "user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "platform": "Mobile", "browser": "No", "device": "iPhone"},
        {
            "user_agent": "Some User Agent", "platform": "Unknown", "browser": "Unknown", "device": "Unknown"},
        {
            "user_agent": "", "platform": "Unknown", "browser": "Unknown", "device": "Unknown"}
    )

    @pytest.mark.parametrize('user_agent_data', user_agent_list)
    def test_user_agent(self, user_agent_data):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        user_agent = user_agent_data["user_agent"]
        expected_platform = user_agent_data["platform"]
        expected_browser = user_agent_data["browser"]
        expected_device = user_agent_data["device"]
        headers = {"User-Agent": user_agent}

        response = requests.get(url=url, headers=headers)
        response_to_json = response.json()
        assert "user_agent" in response_to_json, "There is no user agent key in the response"
        assert "platform" in response_to_json, "There is no platform key in the response"
        assert "browser" in response_to_json, "There is no browser key in the response"
        assert "device" in response_to_json, "There is no device key in the response"

        user_agent_from_response = response_to_json["user_agent"]
        platform_from_response = response_to_json["platform"]
        browser_from_response = response_to_json["browser"]
        device_from_response = response_to_json["device"]

        assert user_agent_from_response == user_agent, f"User agent value for '{user_agent}' in the response in " \
                                                       f"incorrect and equals to '{user_agent_from_response}'"
        assert platform_from_response == expected_platform, f"Platform value for '{user_agent}' in the response in " \
                                                            f"incorrect and equals to '{platform_from_response}'"
        assert browser_from_response == expected_browser, f"Browser value for '{user_agent}' in the response in " \
                                                          f"incorrect and equals to '{browser_from_response}'"
        assert device_from_response == expected_device, f"Device value for '{user_agent}' in the response in incorrect" \
                                                        f"and equals to '{device_from_response}'"
