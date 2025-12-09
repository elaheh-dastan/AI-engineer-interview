# AI-engineer-interview
## BNSF Railway
You must write a PySpark function group_sort that:

Reads a CSV with columns name and job.

Counts how many times each job appears.

Returns a dictionary {job: count}.

Sorts by:

count ascending

job title ascending

This must be implemented using PySpark (RDD or DataFrame).

[https://github.com/elaheh-dastan/AI-engineer-interview/blob/main/bnsf.py](https://github.com/elaheh-dastan/AI-engineer-interview/blob/main/bnsf.py)


What is the difference between

- reduceByKey(lambda a, b: a + b)
- groupByKey().mapValues(sum)

**groupByKey** groups data but it:

- Pulls all values of a key across nodes, more expensive

- Uses more memory

- Slower

**reduceByKey** is preferred because it:

- Reduces values before sending across network

- Uses less memory

- Is faster for aggregation tasks
