from transformers import TapasTokenizer, TapasForTableQuestionAnswering
import torch
import pandas as pd

# Load the Tapas model and tokenizer
model_name = "google/tapas-large-finetuned-wtq"
tokenizer = TapasTokenizer.from_pretrained(model_name)
model = TapasForTableQuestionAnswering.from_pretrained(model_name)

# Load the table from CSV file
table_path = "table.csv"
table = pd.read_csv(table_path)

# Get user input for the query
query = input("Enter your question: ")

# Preprocess the query and table
inputs = tokenizer(table=table, queries=query, padding="max_length", truncation=True, return_tensors="pt")

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)

# Extract and print the answer
answer_coordinates = outputs.answer_coordinates[0].tolist()
answer = table.iloc[answer_coordinates[0]][answer_coordinates[1]]
print("Answer:", answer)
