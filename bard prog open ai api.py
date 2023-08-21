import openai
import os

def get_output(query, csv_file):
  # Create a ChatGPT session
  session = openai.Session("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")

  # Get the response from the ChatGPT API

  response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=query,
    max_tokens=100
  )
#  response = session.create_response(
#    prompt=query,
#    max_tokens=100,
#    temperature=0.7,
#    top_p=0.9,
#    presence_penalty=0.2,
#    repetition_penalty=1.0,
#  )

  # Parse the CSV file
  with open(csv_file, "r") as f:
    reader = csv.reader(f)
    data = list(reader)

  # Find the output that best matches the query
  best_match = None
  for row in data:
    if row[0] == response['choices'][0]['message']['content']:
      best_match = row[1]
      break

  return best_match

if __name__ == "__main__":
  # Get the natural language query
  query = input("Enter your query: ")

  # Get the CSV file
#  csv_file = input("Enter the path to the CSV file: ")
   csv_file = os.path.join(os.getcwd(), 'bard inventory csv.csv')

  # Get the output
  output = get_output(query, csv_file)

  # Print the output
  print(output)

