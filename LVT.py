# Task 1: write a function to calculate the similarity (Dot Product) between two vectors.

import math

def dot_product(v1: list, v2: list) -> int:
  res = 0
  for e1, e2 in zip(v1, v2):
    res += e1 * e2
  return res

def magnitude(v: list) -> float:
  sum_of_product = 0
  for e in v:
    sum_of_product += e ** 2
  return math.sqrt(sum_of_product)

def cosine_similarity(v1: list, v2: list) -> float:
  product_of_magnitudes = magnitude(v1) * magnitude(v2)
  return dot_product(v1, v2) / product_of_magnitudes

def get_similarity(v1: list, v2: list) -> float:
  if len(v1) != len(v2):
    return None
  return cosine_similarity(v1, v2)


def find_index(k_winner_similarity, similarity):
  if len(k_winner_similarity) == 0:
    return 0
  i = len(k_winner_similarity) // 2
  if similarity >= k_winner_similarity[i]:
    return find_index(k_winner_similarity[:i], similarity)

  return i + 1 + find_index(k_winner_similarity[i+1:], similarity)


# Task 2: Given a query vector and a list of product vectors, find the ID of the top k similar items.
## For all products compute similarity and sort them to get the top
class VectorDB:
  def __init__(self, database, top_k=5):
    self.database = database
    self.top_k = top_k
    self.winners = [-1] * top_k
    self.winner_scores = [-1] * top_k

  def __len__(self):
    return len(self.database)

  def heap_sort(self, pv, similarity):
    i = find_index(self.winner_scores, similarity)
    if i >= len(self.winners):
      return
    self.winners = self.winners[:i] + [pv] + self.winners[i:-1]
    self.winner_scores = self.winner_scores[:i] + [similarity] + self.winner_scores[i:-1]

  def find_top_k(self, query: list):
    self.winners = [-1] * self.top_k
    self.winner_scores = [-1] * self.top_k
    for pv in self.database:  # O(n)
      similarity = get_similarity(query, pv["vector"])  # O(d) omitted cause d is fixed
      self.heap_sort(pv, similarity)

    return self.winners

print(find_index([8, 7, 6, 4, 3], 5))
database = [
  {"id": 101, "vector": [0.1, 0.5, 0.2]},
  {"id": 102, "vector": [0.9, 0.1, 0.0]},
  {"id": 103, "vector": [0.2, 0.4, 0.2]},
]

query_vec = [0.1, 0.5, 0.2]

vectorDB = VectorDB(database)
print(vectorDB.find_top_k(query_vec))

