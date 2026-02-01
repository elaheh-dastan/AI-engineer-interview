# Task 1: write a function to calculate the similarity (Dot Product) between two vectors.
# Task 2: Given a query vector and a list of product vectors, find the ID of the top k similar items.

# Example Data
query_vec = [0.1, 0.5, 0.2]

database = [
  {"id": 101, "vector": [0.1, 0.5, 0.2]},
  {"id": 102, "vector": [0.9, 0.1, 0.0]},
  {"id": 103, "vector": [0.2, 0.4, 0.2]},
]

def get_similarity(v1: list, v2: list) -> int:
  if len(v1) != len(v2):
    return None
  res = 0
  for a, b in zip(v1, v2):
    res += a * b

  return res
