import requests
import csv

# Authenticate the user and create a session token/key
auth_url = "https://api.example.com/auth/login"
auth_data = {
    "username": "username",
    "password": "password"
}

response = requests.post(auth_url, data=auth_data)

if response.status_code == 200:
    session_token = response.json()["session_token"]
else:
    raise Exception("Authentication failed")

# Send an HTTP GET request
get_url = "https://api.example.com/users"
headers = {
    "Authorization": "Bearer " + session_token
}

response = requests.get(get_url, headers=headers)

if response.status_code == 200:
    users = response.json()
else:
    raise Exception("GET request failed")

# Store the response in a CSV formatted file
with open("users.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["username", "email"])
    for user in users:
        writer.writerow([user["username"], user["email"]])

# Close the connection
response.close()
