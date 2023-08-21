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


"""
table_string = """
[
    {
      "remote_name": "NGCS-Switch",
      "port_name": "Port #1",
      "name": "enp3s0f1",
      "id": "1",
      "port": "1",
      "mgmt_ip": "192.168.1.13",
      "remote_mac": "ec:9a:74:bc:57:e0"
    },
    {
      "remote_name": "foobar.hostname",
      "port_name": "net1",
      "name": "tap1",
      "id": "2",
      "port": "52:54:00:76:27:fc",
      "mgmt_ip": "192.168.0.1",
      "remote_mac": "52:54:00:76:27:fc"
    }
]
"""

#print(table_string)
# Convert JSON string to list of dicts
table_dict = json.loads(table_string)
#print(table_dict)

# Convert all items in the JSON object to strings
#string_objects = json.dumps(table_dict, default=str)
#print(string_objects)

    

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

   result = tqa(table=table_dict, query=question)
   #result = tqa(table=table, query=question)
   print(result['cells'][0])
    
except Exception as e:
    # Handle the exception
   print("Error occurred:", str(e))
   traceback.print_exc()
    
finally:
    # Perform cleanup operations even if an error occurred
   print("Performing cleanup")
   del pipeline
   gc.collect()