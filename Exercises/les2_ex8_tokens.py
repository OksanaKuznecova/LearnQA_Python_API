import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Task creation
create_task_response = requests.get(url=url)
# convert to json format
create_task_response_to_json = create_task_response.json()
# Checking the response content
if "seconds" in create_task_response_to_json:
    if "token" in create_task_response_to_json:
        # Extracting seconds to wait
        seconds_to_wait = create_task_response_to_json["seconds"]
        # Extracting token
        token = create_task_response_to_json["token"]
        payload = {"token": token}
        # Sending the request before task's completion to check status
        get_task_status_response = requests.get(url=url, params=payload)
        get_task_status_response_to_json = get_task_status_response.json()
        # Checking the response content
        if "status" in get_task_status_response_to_json:
            status = get_task_status_response_to_json["status"]
            if status == "Job is NOT ready":
                print(f"All is good. Task's status is {status}. "
                      f"Need to wait for {seconds_to_wait} second(s) for completion.")
                # Waiting for task's completion
                time.sleep(seconds_to_wait)
                # Sending the request after task's completion
                get_task_status_response = requests.get(url=url, params=payload)
                get_task_status_response_to_json = get_task_status_response.json()
                # Checking the response content
                if "status" in get_task_status_response_to_json:
                    status = get_task_status_response_to_json["status"]
                    # Checking the task's status
                    if status == "Job is ready":
                        # Getting the task's result
                        if "result" in get_task_status_response_to_json:
                            result = get_task_status_response_to_json["result"]
                            print(f"Task is ready. The result is {result}")
                        else:
                            print(f"Task is not ready. Result is missing")
                    else:
                        print(f"Task is not ready. Status is {status}")
                else:
                    print("Something is wrong. Status is missing.")
            else:
                print(f"Something is wrong. Task's status is {status}")
else:
    print("Something wrong happened during task creation.")



