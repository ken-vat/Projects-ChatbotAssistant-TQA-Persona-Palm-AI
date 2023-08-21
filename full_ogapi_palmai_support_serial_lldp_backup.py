import google.generativeai as palm
import pprint
import json
import requests
import csv
import json

## STATICS
######################

# PALM key
palmai_api_key="AIzaSyC_GhvHWk9Uorf9Pj808KA3gzogfL3_ukA"

# Enhance LLDP JSON output with these key mappings - for better natural language query
lldp_nei_key_mappings = {
        "remote_name": "System name or remote name or device name",
        "port_name": "Remote port name or remote interface name",
        "name": "Local port name or Local interface name",
        "id": "Local row id",
        "port": "Remote port ID or remote port MAC or PortID",
        "mgmt_ip": "Management addresses or management IP addresses or IP addresses",
        "remote_mac": "Chassis ID or MAC address or remote MAC or Chassis MAC"
}

# Prompt for documentation response
og_doc_prompt = """You are a chatbot virtual assistant for Opengear. can you answer user questions by using publicly available and accessible information and documentation on Opengear including from Opengear website, the Opengear zendesk site, the Opengear ftp site * * *
    **Welcome to the Opengear chatbot. I can answer your questions about Opengear products and services.**

    **What can I help you with today?**

    * * *how do i setup opengear 7000 series to send an email or sms alert
"""

# Prompt for LLDP response
lldp_nei_tqa_prompt = """You are a expert table question answering transformers pipeline AI model to help provide precise answers from tables to answer a user's question. 
    The table is provided below as table_input in json format. the user's question is provided below as users_question
table_input:
[
    {
      "System name or remote name or device name or remote system name or remote devices or managed devices": "NGCS-Switch",
      "Remote port name or remote interface": "Port #1",
      "Local port name": "enp3s0f1",
      "id": "1",
      "Remote port ID or remote port MAC or PortID": "52:54:00:76:27:00",
      "Management address or management IP address or remote IP address": "192.168.1.13",
      "Chassis ID or MAC address or remote MAC or Chassis MAC": "ec:9a:74:bc:57:e0"
    },
    {
      "System name or remote name or device name or remote system name or devices": "foobar.hostname",
      "Remote port name or remote interface": "net1",
      "Local port name": "tap1",
      "id": "2",
      "Remote port ID or remote port MAC or PortID": "52:54:00:76:27:fc",
      "Management address or management IP address or remote IP address": "192.168.0.1",
      "Chassis ID or MAC address or remote MAC or Chassis MAC": "52:54:00:76:27:fc"
    }
]

users_question:
Find all Chassis IDs
"""


# Prompt for serial port response
serial_port_tqa_prompt = """You are a expert table question answering transformers pipeline AI model to help provide precise answers from tables to answer a user's question. 
    The table is provided below as table_input in json format. the user's question is provided below as users_question
table_input:
[
    {
      "parity": "none",
      "label or hostname": "cisco6500",
      "id": "ports-1",
      "escape_char": null,
      "control_code": null,
      "stopbits": "1",
      "status": "ok",
      "portnum": 1,
      "pinout": "X2",
      "available_pinouts": [
        "X2",
        "X1"
      ],
      "ip_alias": null,
      "pdu_outlets": null,
      "baudrate": "9600",
      "mode": "localConsole",
      "logging_level": "eventsAndAllCharacters",
      "databits": "8",
      "terminal_emulation": "linux",
      "kernel_debug": false,
      "sessions": [],
      "device": "serial/by-opengear-id/port01",
      "name": "port01"
    },
    {
      "parity": "none",
      "label or hostname": "juniper2k",
      "id": "ports-2",
      "escape_char": "~",
      "control_code": {
        "break": "b",
        "portlog": "l",
        "power": "p",
        "chooser": "c",
        "quit": "q",
        "pmhelp": "h"
      },
      "stopbits": "1",
      "status": "ok",
      "portnum": 2,
      "pinout": "X2",
      "available_pinouts": [
        "X2",
        "X1"
      ],
      "ip_alias": [],
      "pdu_outlets": [],
      "baudrate": "19200",
      "mode": "consoleServer",
      "logging_level": "eventsOnly",
      "databits": "8",
      "terminal_emulation": null,
      "kernel_debug": null,
      "sessions": [],
      "device": "serial/by-opengear-id/port02",
      "name": "port02"
    },
    {
      "parity": "none",
      "label or hostname": "Arista",
      "id": "ports-3",
      "escape_char": "~",
      "control_code": {
        "break": "b",
        "portlog": "l",
        "power": "p",
        "chooser": "c",
        "quit": "q",
        "pmhelp": "h"
      },
      "stopbits": "1",
      "status": "ok",
      "portnum": 3,
      "pinout": "X2",
      "available_pinouts": [
        "X2",
        "X1"
      ],
      "ip_alias": [
        {
          "id": "ipalias-1",
          "port": "serial/by-opengear-id/port03",
          "ipaddress": "192.168.33.11/24",
          "interface": "net1"
        }
      ],
      "pdu_outlets": [],
      "baudrate": "115200",
      "mode": "consoleServer",
      "logging_level": "disabled",
      "databits": "8",
      "terminal_emulation": null,
      "kernel_debug": null,
      "sessions": [],
      "device": "serial/by-opengear-id/port03",
      "name": "port03"
    }
]

users_question:
hostname of port03
label of port02
logging level of port01
"""

### END STATICS
#######################################


### Functions
########################

# Step 1: Authenticate the user and create a session token/key
def authenticate_user():
    # Make a POST request with the user credentials to the authentication endpoint
    response = requests.post('https://10.60.17.214/api/v2/sessions', headers={'Content-Type': 'application/json'}, json={'username':'root','password':'snodgrass'}, verify=False)
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

# Step 2: LLDP - Send a GET API request and validate the response
def send_get_request_lldp_nei(session_token):
    if session_token:
        print(session_token)
        # Add the session token to the request headers
        headers = {'Authorization': f'Token {session_token}'}
        print(headers)
        #headers = {'Authorization': f'Bearer {session_token}'}
        # Make a GET request to the API endpoint
        response = requests.get('https://10.60.17.214/api/v2/monitor/lldp/neighbor', headers=headers, verify=False)
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

# Step 2: Serial ports - Send a GET API request and validate the response
def send_get_request_serial_ports(session_token):
    if session_token:
        print(session_token)
        # Add the session token to the request headers
        headers = {'Authorization': f'Token {session_token}'}
        print(headers)
        #headers = {'Authorization': f'Bearer {session_token}'}
        # Make a GET request to the API endpoint
        response = requests.get('https://10.60.17.214/api/v2/ports', headers=headers, verify=False)
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

# Step 3: Close the connection (optional)
def close_connection():
    # The requests library automatically closes the connection when the request is complete
    print("Connection closed.")



# Function to swap original API JSON for LLDP keys with previously defined key mappings
# data: original JSON from OG REST API output;   key_mappings: defined in STATICS above
def replace_keys(data, key_mappings):
    modified_data = []
    for item in data:
        modified_item = {}
        for key, value in item.items():
            if key in key_mappings:
                new_key = key_mappings[key]
                modified_item[new_key] = value
            else:
                modified_item[key] = value
        modified_data.append(modified_item)
    return modified_data




### END FUNCTIONS




#### BEGIN MAIN PROGRAMS
#########################


# Handle OG REST API
"""
session_token = authenticate_user()
print(session_token)

serial_ports_response_data = send_get_request_serial_ports(session_token)
lldp_nei_response_data = send_get_request_lldp_nei(session_token)
print(serial_ports_response_data)
print(lldp_nei_response_data)
#store_response_as_csv(response_data)
close_connection()
"""

# Replace keys in - data variable is enhanced JSON
#modified_data = json.dumps(replace_keys(data,lldp_nei_key_mappings))
#print(modified_data)


# Main program flow - PALM API
palm.configure(api_key=palmai_api_key)
#palm.configure(api_key="AIzaSyC_GhvHWk9Uorf9Pj808KA3gzogfL3_ukA")
defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.7,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
        'stop_sequences': [],

}


## GET User selection
print("Please select an option:")
print("1. Enter number 1 for documentation AI")
print("2. Enter number 2 for serial ports AI")
print("3. Enter number 3 for LLDP neighbor AI")

user_input = input("Enter your choice: ")

#### PALM invoke for options
#########################

if user_input == "1":
# Get response for doc
    response = palm.generate_text(
        **defaults,
        prompt=og_doc_prompt
    )

    

elif user_input == "2":
# Get response for serial ports
    response = palm.generate_text(
        **defaults,
        prompt=serial_port_tqa_prompt
    )
    
elif user_input == "3":
# Get response for LLDP nei
    response = palm.generate_text(
        **defaults,
        prompt=lldp_nei_tqa_prompt
    )

else:
    print("Invalid input!")


print(response.result)


