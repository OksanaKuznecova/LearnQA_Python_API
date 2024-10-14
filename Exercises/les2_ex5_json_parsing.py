import json

# This is a JSON to parse taken from the https://gist.github.com/KotovVitaliy/83e4eeabdd556431374dfc70d0ba9d37
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And ' \
            'this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(json_text)

key1 = "messages"
key2 = "message"

# Check that JSON contains messages
if key1 in obj:
    # Getting the list of messages
    messages_list = obj[key1]
    # Checking the length of the list of messages if we can get the second message from it
    if len(messages_list) >= 2:
        # Getting the second message from the list
        second_message = messages_list[1]
        # Checking if there is a message text
        if key2 in second_message:
            # Printing message text
            print(second_message[key2])
        else:
            # Throwing the error if second message's text cannot be found
            print(f"The key {key2} is not found. Cannot print the second message text.")
    else:
        # Throwing the error if there are less than two messages in the JSON
        print(f"Cannot find the second message.")
else:
    print(f"There are no any messages in JSON.")
