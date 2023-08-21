
# %pip install transformers
# %pip install pandas
# %pip install torch
# %pip install torch-scatter
# https://huggingface.co/tasks/table-question-answering
# https://github.com/huggingface/transformers/blob/main/src/transformers/pipelines/table_question_answering.py

from transformers import pipeline
import pandas as pd
import torch


# Load the table from CSV file
table_file = "sample_data/simple Q and A csv for openai program.csv"

with open(table_file, "r") as f:
    table = pd.read_csv(table_file, header=None, names=['Vendor', 'Model', 'Status'])

# Get user input for the query
# Example input: "what is the cisco model"
#    ..what is the status of cisco, what is the status of 7200
question = input("Enter your question: ")


# pipeline model
# Note: you must to install torch-scatter first.
tqa = pipeline(task="table-question-answering", model="google/tapas-large-finetuned-wtq")

# result
print(tqa(table=table, query=question)['cells'][0])

print(tqa(table=table, query=question)['cells'])