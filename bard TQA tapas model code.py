import transformers

# Load the Table Question Answering model
model = transformers.AutoModelForQuestionAnswering.from_pretrained("google/tapas-large-finetuned-wtq")

# Get the query from user
query = input("Enter your query: ")

# Parse the table with the Table Question Answering model
answer = model.generate(
    input_text=query,
    max_length=128,
    do_sample=True,
    temperature=0.7,
    num_beams=4,
    no_repeat_ngram_size=3,
)

# Print the answer
print(answer)
