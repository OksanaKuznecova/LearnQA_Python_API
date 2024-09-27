import requests

url = "https://playground.learnqa.ru/api/long_redirect"
# I added these headers because without them the redirect is failing with 403 code when redirecting to
# https://learnqa.ru/
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/129.0.0.0 Safari/537.36"}

response = requests.get(url, allow_redirects=True, headers=headers)

# Getting the response history
response_history = response.history
# Getting the response history length to identify the number of redirects
response_history_length = len(response.history)
print(f"The number of redirects is {response_history_length}")
if response_history_length == 0:
    print(f"looks like this endpoint does not have any redirects")
else:
    h = 0
    while h < response_history_length:
        # Checking each redirect
        redirect_response = response_history[h]
        # Printing each redirect URL and status code
        print(redirect_response.url)
        print(redirect_response.status_code)
        h += 1
    # the final URL and status code
    print(f"The final URL is {response.url}")
    print(f"The final Status Code is {response.status_code}")
