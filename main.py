import torch
from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis")

# Classify a new sentence
result = pipe("I love this product! It's amazing and works perfectly.")

# Print the result
print(result)
