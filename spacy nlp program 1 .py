import csv
import spacy

# Open the CSV file
#with open("sample_data/text file for chat prog .txt", "r") as f:
#  reader = csv.reader(f)
#  data = []
#  for row in reader:
#    data.append(row)

        
# Load the spacy model
nlp = spacy.load("en_core_web_sm")

# Get the user's query
query = input("What is your query? ")

# Parse the query and find the relevant elements
doc = nlp(query)
elements = [token.text for token in doc if token.is_stop == False]

# open regular text file
file_path = "sample_data/text file for chat prog .txt"
with open(file_path, 'r') as file:
    file_contents = file.read()
# Create a temporary variable to store each line
    line = ""

# Loop over the lines in the file
    for line in f:
# Print the line
        doc2 = nlp(line)
        similarity_score = doc.similarity(doc2)
        print(line)
        print(similarity_score)

# Search the CSV file for the best response
#best_match = None
#for row in data:
#  for element in elements:
#    if element in row:
#      best_match = row
#      break

# Print the best match
#if best_match is not None:
#  print(best_match[1])
#else:
#  print("No match found.")
