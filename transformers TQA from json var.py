from transformers import pipeline
#import transformers
import pandas as pd
import torch
import json
import gc
import traceback



# Load the table from CSV file
table_file = "sample_data/lldp neigh csv for transformers TQA.csv"

with open(table_file, "r") as f:
#    table = pd.read_csv(table_file, header=None, names=['Vendor', 'Model', 'Status'])
    table = pd.read_csv(table_file, header=0)
print(table)
#print(type(table))
table_dict = table.to_dict('records')

table_string = """
[
    {
      "remote name": "NGCS-Switch",
      "port name": "Port #1",
      "name": "enp3s0f1",
      "id": "1",
      "port": "1",
      "management ip address": "192.168.1.13",
      "remote mac address": "ec:9a:74:bc:57:e0"
    },
    {
      "remote name": "foobar.hostname",
      "port name": "net1",
      "name": "tap1",
      "id": "2",
      "port": "52:54:00:76:27:fc",
      "management ip address": "192.168.0.1",
      "remote mac address": "52:54:00:76:27:fc"
    }
]
"""
"""
table_string = """
[
  {
    "Vendor": "Cisco",
    "Model": "7200",
    "Status": "Active"
  },
  {
    "Vendor": "Juniper",
    "Model": "MX960",
    "Status": "Down"
  }
]
"""
"""

#print(table_string)
# Convert JSON string to list of dicts
table_dict = json.loads(table_string)
#print(table_dict)

# Convert all items in the JSON object to strings
#string_objects = json.dumps(table_dict, default=str)
#print(string_objects)

#def csv_to_json(csv_file_path):
    # Read CSV into a pandas DataFrame
#    df = pd.read_csv(csv_file_path)
    
# Convert DataFrame to JSON
#json_data = table.to_json(orient='records')

# Convert the JSON string to a Python list of dictionaries 
#data = json.loads(json_data)

# Get user input for the query
# Example input: "what is the cisco model"
#    ..what is the status of cisco, what is the status of 7200
#question = input("Enter your question: ")

question = "ogcs remote mac"
print (question)
try:
  # pipeline model
  # Note: you must to install torch-scatter first.
   tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

#for entry in table_data_dict:
#    answer = tqa(question=question, table=[entry])['cells'][0]
#    print(answer)

# result

   result = tqa(table=table_dict, query=question)
   #result = tqa(table=table, query=question)
   print(result['cells'][0])
#print(tqa(table=table, query=question))
#print(tqa(table=table, query=question)['cells'])

#   raise Exception("Simulated error")
    
except Exception as e:
    # Handle the exception
   print("Error occurred:", str(e))
   traceback.print_exc()
    
finally:
    # Perform cleanup operations even if an error occurred
   print("Performing cleanup")
   del pipeline
   gc.collect()


