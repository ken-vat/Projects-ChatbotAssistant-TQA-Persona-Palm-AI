##
# Input
# -----
#vendors or products or devices are cisco, juniper, arista
# cisco models are 7200
#juniper models are 7000
#arista models are 7000, 8000
#status of cisco 7200 is off
#status of juniper 7000 is on
#status of arista 7000 is off
#status of arista 8000 is on

#### comments
# -------
### this has shown better outcome than other models bert, roberta with cosine sim but still has issue for example with "how many arista models do i have"
#   this resulted in higher score for juniper
###  lg better than sm. trf did not work in colab.
###
import spacy
# Load the spacy model
nlp = spacy.load("en_core_web_lg")

# Get the user's query
query = input("What is your query? ")

# Parse the query and find the relevant elements
doc = nlp(query)
print(doc)
#elements = [token.text for token in doc if token.is_stop == False]
#print(elements)
# open regular text file
file_path = "sample_data/text file for chat prog .txt"
with open(file_path, 'r') as file:

# Loop over the lines in the file
    for line in file:
# Print the line
        
        doc2 = nlp(line)
        similarity_score = doc.similarity(doc2)

#        print(line, similarity_score)
        print(f"line: {line}: score: {similarity_score} !\n")


------

import csv
import spacy
# Load the spacy model
nlp = spacy.load("en_core_web_sm")

# Get the user's query
query = input("What is your query? ")

# Parse the query and find the relevant elements
doc = nlp(query)
print(doc)
#elements = [token.text for token in doc if token.is_stop == False]
#print(elements)
# open regular text file
file_path = "sample_data/text file for chat prog .txt"
with open(file_path, 'r') as file:

# Loop over the lines in the file
    for line in file:
# Print the line
        print(line)
        doc2 = nlp(line)
        similarity_score = doc.similarity(doc2)

        print(similarity_score)