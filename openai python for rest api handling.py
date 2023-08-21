import requests
import csv
import json

# Step 1: Authenticate the user and create a session token/key
def authenticate_user():
    # Make a POST request with the user credentials to the authentication endpoint
    response = requests.post('https://10.60.17.209/api/v2/sessions', headers={'Content-Type': 'application/json'}, json={'username':'root','password':'snodgrass'}, verify=False)
    #print(f"response code: {response}")
    print(response.content)
    print(response.text)
    print("response code: %s!" %response)
    if response.status_code == 200:
        # Authentication successful
        # Extract the session token/key from the response
        # session_token = response.json().get('session_token')
        # session_token = response.json()["session_token"]
        session_token = json.loads(response.content)['session']
        print(session_token)
        return session_token
    else:
        # Authentication failed
        # Handle the error
        print("Authentication failed.")
        return None

# Step 2: Send a GET API request and validate the response
def send_get_request_lldp_nei(session_token):
    if session_token:
        print(session_token)
        # Add the session token to the request headers
        headers = {'Authorization': f'Token {session_token}'}
        print(headers)
        #headers = {'Authorization': f'Bearer {session_token}'}
        # Make a GET request to the API endpoint
        response = requests.get('https://10.60.17.209/api/v2/monitor/lldp/neighbor', headers=headers, verify=False)
        print("response code: %s!" %response.status_code)
        if response.status_code == 200:
            # Request was successful
            # Process the response content
            data = response.json()
            print(data)
            return data
        else:
            # Request was not successful
            # Handle the error
            print("GET request failed.")
    else:
        # Authentication failed, so cannot make the request
        print("Authentication failed. Cannot make the GET request.")
    return None


def send_get_request_serial_port(session_token):
    if session_token:
        #print(session_token)
        # Add the session token to the request headers
        headers = {'Authorization': f'Token {session_token}'}
        #print(headers)
        #headers = {'Authorization': f'Bearer {session_token}'}
        # Make a GET request to the API endpoint
        response = requests.get('https://10.60.17.209/api/v2/ports', headers=headers, verify=False)
        print("response code: %s!" %response.status_code)
        if response.status_code == 200:
            # Request was successful
            # Process the response content
            data = response.json()
            #print(data)
            return data
        else:
            # Request was not successful
            # Handle the error
            print("GET request failed.")
    else:
        # Authentication failed, so cannot make the request
        print("Authentication failed. Cannot make the GET request.")
    return None



# Step 3: Store the response in a CSV formatted file
def store_response_as_csv(data):
    if data:
        # Define the CSV file path
        file_path = 'response_data.csv'

        # Extract the necessary data from the response
        extracted_data = data['data']  # Adjust this based on the actual structure of the response

        # Write the data to a CSV file
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(extracted_data.keys())  # Write header row
            writer.writerow(extracted_data.values())  # Write data row

        print(f"Response data stored in {file_path}")
    else:
        print("No response data to store.")

# Step 4: Close the connection (optional)
def close_connection():
    # The requests library automatically closes the connection when the request is complete
    print("Connection closed.")

# Main program flow
session_token = authenticate_user()
print("Session token: ")
print(session_token)

response_data = send_get_request_serial_port(session_token)
print(response_data)
#store_response_as_csv(response_data)
close_connection()

