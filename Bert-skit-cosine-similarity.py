from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

# Load the fine-tuned BERT model
model = BertModel.from_pretrained("bert-large-cased")
tokenizer = BertTokenizer.from_pretrained("bert-large-cased")

# Example queries
query1 = "How can I improve my coding skills?"
query2 = "What are some tips for becoming a better cook?"

# Tokenize and encode the queries
encoded_query1 = tokenizer.encode_plus(query1, add_special_tokens=True, padding="max_length", max_length=128, truncation=True, return_tensors="pt")
encoded_query2 = tokenizer.encode_plus(query2, add_special_tokens=True, padding="max_length", max_length=128, truncation=True, return_tensors="pt")

# Get the token embeddings
input_ids1 = encoded_query1["input_ids"]
attention_mask1 = encoded_query1["attention_mask"]

input_ids2 = encoded_query2["input_ids"]
attention_mask2 = encoded_query2["attention_mask"]

# Pass the queries through the BERT model
with torch.no_grad():
    output1 = model(input_ids1, attention_mask=attention_mask1)[0].squeeze(0)
    output2 = model(input_ids2, attention_mask=attention_mask2)[0].squeeze(0)

# Reshape the tensors
output1 = output1.reshape(1, -1)
output2 = output2.reshape(1, -1)

# Calculate cosine similarity between the query embeddings
similarity = cosine_similarity(output1, output2)

# Print the similarity score
print("Similarity Score:", similarity[0][0])
