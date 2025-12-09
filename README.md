# AI-engineer-interview
## BNSF Railway
### 1.
You must write a PySpark function group_sort that:

Reads a CSV with columns name and job.

Counts how many times each job appears.

Returns a dictionary {job: count}.

Sorts by:

count ascending

job title ascending

This must be implemented using PySpark (RDD or DataFrame).

[https://github.com/elaheh-dastan/AI-engineer-interview/blob/main/bnsf.py](https://github.com/elaheh-dastan/AI-engineer-interview/blob/main/bnsf.py)


### 2.
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

### 3. 
What is the difference between liveness and readiness probe?
<br><br>
🟢 Readiness Probe — “Can this pod receive traffic right now?”

A Readiness Probe tells Kubernetes whether the container is ready to serve requests.

If readiness fails, Kubernetes removes the pod from the Service load balancer.

But the pod is not restarted — it stays alive.

Used when the app is temporarily not able to accept traffic (e.g., warming up, dependencies down).

✔ Example Scenario — App still starting up

Your backend needs 10 seconds to load a large ML model before it can handle requests.

Readiness Probe fails for 10 seconds → K8s sends no traffic to it.

Once the container returns success (200), the pod becomes ready, and traffic starts flowing.
<br><br>
🔴 Liveness Probe — “Is this pod still healthy or should it be restarted?”

A Liveness Probe detects whether the app is alive or stuck.

If liveness fails, Kubernetes will kill and restart the pod.

Used for detecting deadlocks, memory corruption, or frozen processes.

✔ Example Scenario — App gets stuck

Your backend hangs because of a deadlock or runs out of memory.
It no longer responds on /healthz.

Liveness Probe fails → Kubernetes restarts the pod.

This helps self-heal without human intervention.
