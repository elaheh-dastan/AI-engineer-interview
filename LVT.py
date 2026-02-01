# Task 1: write a function to calculate the similarity (Dot Product) between two vectors.
# Task 2: Given a query vector and a list of product vectors, find the ID of the top k similar items.

import math
# Example Data
query_vec = [0.1, 0.5, 0.2]

database = [
  {"id": 101, "vector": [0.1, 0.5, 0.2]},
  {"id": 102, "vector": [0.9, 0.1, 0.0]},
  {"id": 103, "vector": [0.2, 0.4, 0.2]},
]

def dot_product(v1: list, v2: list) -> int:
  res = 0
  for e1, e2 in zip(v1, v2):
    res += e1 * e2
  return res

def magnitude(v: list) -> int:
  sum_of_product = 0
  for e in v:
    sum_of_product += e ** 2
  return math.sqrt(sum_of_product)
  
def cosine_similarity(v1: list, v2: list) -> int:
  product_of_magnitudes = magnitude(v1) * magnitude(v2)
  return dot_product(v1, v2) / product_of_magnitudes

def get_similarity(v1: list, v2: list) -> int:
  if len(v1) != len(v2):
    return None
  return cosine_similarity
