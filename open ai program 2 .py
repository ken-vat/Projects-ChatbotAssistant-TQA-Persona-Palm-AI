import openai
import csv

# Set your OpenAI API key
openai.api_key = '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'

# Step 1: Take a natural language prompt from the user
prompt = input("Enter your query: ")

# Step 2: Open and read the contents of the CSV file
with open('sample_data/text file for chat prog .txt', 'r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

# Step 3: Parse the content of the CSV file
# Assuming the CSV file has two columns: Question and Response
questions = [row[0] for row in data]
responses = [row[1] for row in data]

# Step 4: Find the best response for the query
best_response = None
max_similarity = 0

for i, question in enumerate(questions):
    # Compare the similarity between the prompt and each question
    response = responses[i]
    similarity = openai.ChatCompletion.compare(
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
            {'role': 'assistant', 'content': question},
        ]
    ).comparison.score

    # Keep track of the highest similarity score and corresponding response
    if similarity > max_similarity:
        max_similarity = similarity
        best_response = response

# Print the best response
print("Best response:", best_response)
