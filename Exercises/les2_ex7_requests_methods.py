import requests

# Here is the URL we are going to work with
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
# Here is an array of allowed methods
allowed_methods = ["GET", "POST", "PUT", "DELETE"]
not_allowed_method = "HEAD"

# Let's print the request response when no method provided in params
get_response_wo_params = requests.get(url=url)
print(
    f"GET request wo params returns {get_response_wo_params.status_code}: {get_response_wo_params.text}")

post_response_wo_params = requests.post(url=url)
print(
    f"POST request wo params returns {post_response_wo_params.status_code}: {post_response_wo_params.text}")

put_response_wo_params = requests.put(url=url)
print(
    f"PUT request wo params returns {put_response_wo_params.status_code}: {put_response_wo_params.text}")

delete_response_wo_params = requests.delete(url=url)
print(
    f"DELETE request wo params returns {delete_response_wo_params.status_code}: {delete_response_wo_params.text}")

# Let's print the request response for not supported method
head_response_wo_params = requests.head(url=url)
print(
    f"Not supported {not_allowed_method} request without sending method as a parameter returns "
    f"{head_response_wo_params.status_code}: {head_response_wo_params.text}")

payload = {"method": not_allowed_method}
head_response_wo_params = requests.head(url=url, data=payload)
print(
    f"Not supported {not_allowed_method} request with sending method as a parameter returns "
    f"{head_response_wo_params.status_code}: {head_response_wo_params.text}")

# Let's print the request response when allowed method provided with valid method in params
for method in allowed_methods:
    payload = {"method": method}
    match method:
        case "GET":
            response = requests.get(url=url, params=payload)
            print(
                f"{method} request with sending {method} method as a parameter returns "
                f"{response.status_code}: {response.text}")
        case "POST":
            response = requests.post(url=url, data=payload)
            print(
                f"{method} request with sending {method} method as a parameter returns "
                f"{response.status_code}: {response.text}")
        case "PUT":
            response = requests.put(url=url, data=payload)
            print(
                f"{method} request with sending {method} method as a parameter returns "
                f"{response.status_code}: {response.text}")
        case "DELETE":
            response = requests.delete(url=url, data=payload)
            print(
                f"{method} request with sending {method} method as a parameter returns "
                f"{response.status_code}: {response.text}")
        case _:
            print("We do not expect this method here")

# Let's print the request response for combinations of methods
for method in allowed_methods:
    payload = {"method": method}
    get_response = requests.get(url=url, params=payload)
    print(
        f"GET request with {method} method as a parameter returns {get_response.status_code}: {get_response.text}")

for method in allowed_methods:
    payload = {"method": method}
    post_response = requests.post(url=url, data=payload)
    print(
        f"POST request with {method} method as a parameter returns {post_response.status_code}: {post_response.text}")

for method in allowed_methods:
    payload = {"method": method}
    put_response = requests.put(url=url, data=payload)
    print(
        f"PUT request with {method} method as a parameter returns {put_response.status_code}: {put_response.text}")

for method in allowed_methods:
    payload = {"method": method}
    delete_response = requests.delete(url=url, data=payload)
    print(
        f"DELETE request with {method} method as a parameter returns {delete_response.status_code}: {delete_response.text}")
