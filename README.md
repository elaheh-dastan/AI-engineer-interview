# AI Engineer Interview Questions

A collection of questions (and my answers) from AI-engineering interviews, grouped by
company. Coding answers live in the [`solutions/`](solutions/) directory, one folder per
company.

## Table of contents

- [BNSF Railway](#bnsf-railway)
- [Cresta](#cresta)
- [LVT](#lvt)
- [BitPin](#bitpin)
- [CAT](#cat)
- [PetroPower](#petropower)
- [Goodfolio](#goodfolio)
- [Picnic](#picnic)
- [FanDuel](#fanduel)
- [AveeHealth](#aveehealth)
- [Headspace](#headspace)
- [Sema4](#sema4)

### Solutions index

| Company      | Problem                   | File                                                                               |
| ------------ | ------------------------- | ---------------------------------------------------------------------------------- |
| BNSF Railway | PySpark `group_sort`      | [`solutions/bnsf/group_sort.py`](solutions/bnsf/group_sort.py)                     |
| Cresta       | Job dispatcher            | [`solutions/cresta/job_dispatcher.py`](solutions/cresta/job_dispatcher.py)         |
| LVT          | Similar-product retrieval | [`solutions/lvt/similar_products.py`](solutions/lvt/similar_products.py)           |
| CAT          | Longest common prefix     | [`solutions/cat/longest_common_prefix.py`](solutions/cat/longest_common_prefix.py) |
| CAT          | Timing decorator          | [`solutions/cat/decorator.py`](solutions/cat/decorator.py)                         |
| Goodfolio    | Array problems            | [`solutions/goodfolio/array_problems.py`](solutions/goodfolio/array_problems.py)   |

---

## BNSF Railway

### 1. PySpark `group_sort`

Write a PySpark function `group_sort` that:

- Reads a CSV with columns `name` and `job`.
- Counts how many times each job appears.
- Returns a dictionary `{job: count}`.
- Sorts by count ascending, then job title ascending.

This must be implemented using PySpark (RDD or DataFrame).

➡️ Solution: [`solutions/bnsf/group_sort.py`](solutions/bnsf/group_sort.py)

### 2. `reduceByKey` vs `groupByKey().mapValues(sum)`

What is the difference between `reduceByKey(lambda a, b: a + b)` and
`groupByKey().mapValues(sum)`?

**`groupByKey`** groups data but it:

- Pulls all values of a key across nodes, more expensive
- Uses more memory
- Slower

**`reduceByKey`** is preferred because it:

- Reduces values before sending across network
- Uses less memory
- Is faster for aggregation tasks

### 3. Liveness vs readiness probes

What is the difference between a liveness and a readiness probe?

🟢 **Readiness Probe — "Can this pod receive traffic right now?"**

A readiness probe tells Kubernetes whether the container is ready to serve requests.
If readiness fails, Kubernetes removes the pod from the Service load balancer, but the
pod is **not** restarted — it stays alive. Used when the app is temporarily unable to
accept traffic (e.g., warming up, dependencies down).

✔ _Example — app still starting up:_ your backend needs 10 seconds to load a large ML
model before it can handle requests. The readiness probe fails for 10 seconds → K8s
sends no traffic to it. Once the container returns success (200), the pod becomes ready
and traffic starts flowing.

🔴 **Liveness Probe — "Is this pod still healthy or should it be restarted?"**

A liveness probe detects whether the app is alive or stuck. If liveness fails,
Kubernetes will kill and restart the pod. Used for detecting deadlocks, memory
corruption, or frozen processes.

✔ _Example — app gets stuck:_ your backend hangs because of a deadlock or runs out of
memory. It no longer responds on `/healthz`. The liveness probe fails → Kubernetes
restarts the pod. This helps self-heal without human intervention.

---

## Cresta

### 1. Job dispatcher (coding challenge)

Implement a simple job dispatcher that distributes incoming jobs to a pool of executors
(workers). Each job is represented as an integer (its ID), and executors are dynamically
added and removed during runtime.

Define two classes:

**`Executor`** – represents a worker that can accept jobs.

- `assign_job(job_id: int)` — adds the job to its list of jobs.
- `execute_next_job()` — executes the next job in the list and removes it.

**`JobDispatcher`** – maintains a list of executors and distributes jobs to them.

- `add_executor(executor: Executor)` — add an executor.
- `remove_executor(executor_id: str)` — remove an executor.
- `dispatch(job_id: int)` — assign a job to one of the executors.
- `get_state()` — returns a mapping of `executor_id → job list`.

➡️ Solution: [`solutions/cresta/job_dispatcher.py`](solutions/cresta/job_dispatcher.py)

### 2. How do you know your LLM-as-a-judge is working correctly?

1. Compare the LLM judge against human-labeled gold standards.
2. Check for systematic bias across answer types: LLMs tend to favor longer answers, etc.
   Give two semantically identical but stylistically different answers and check if the
   judge scores them equally.
3. Validate with perturbation tests — e.g. add typos → score shouldn't change.
4. Use adversarial evaluation — e.g. provide confident but wrong answers.
5. Cross-model agreement (ensemble judging).
6. Self-consistency checks — e.g. ask the same question multiple times.
7. Check calibration — e.g. provide ambiguous/borderline inputs and see if the judge
   scores them near the middle (e.g. 0.45–0.55 relevance) instead of overconfident
   extremes.

---

## LVT

### 1. Can you explain OOV?

OOV stands for **Out-Of-Vocabulary**: a word, token, or symbol that does not exist in
the model's known vocabulary.

1. **Traditional word-level models**
   - Vocabulary is fixed.
   - OOV words are mapped to a special token like `<UNK>`.
   - ❌ Loses all information about the word.
2. **Subword-based models (modern NLP)**
   - Examples: BPE, WordPiece, SentencePiece.
   - Split words into smaller units: `playstation5 → play, station, 5`.
   - ✅ Greatly reduces OOV problems.
3. **Character-level models**
   - Operate on characters instead of words.
   - Almost no OOV issues.
   - ❌ Longer sequences, higher compute cost.

### 2. Autoregressive vs masked modeling

AR predicts the next token using only past tokens. Masked modeling predicts missing
tokens using both left and right context.

### 3. Explain prompt caching

A technique where repeated or reusable parts of a prompt are stored and reused. Many LLM
requests share a large, static prefix (for example, system instructions). Prompt caching
allows the model (or the serving system) to:

1. Compute embeddings / internal representations for the static part once.
2. Reuse them across multiple requests.
3. Only process the dynamic part (user query, last turn, variables).

### 4. Similar-product recommendation engine

We are building a simple similar-product recommendation engine. We have a DB of items,
where each item is represented by an embedding.

➡️ Solution: [`solutions/lvt/similar_products.py`](solutions/lvt/similar_products.py)

Important points:

- Cosine similarity equals the dot product of two vectors divided by the product of their
  magnitudes. To measure semantic similarity between product embeddings, use cosine
  similarity rather than a raw dot product. This means the vectors must be normalized;
  otherwise **vector magnitude will incorrectly inflate similarity scores.**
- To find top-k products we can:
  - Compute similarity scores for all products and sort them — `O(n log n)`.
  - Build a max heap from all scores and extract the top k — `O(n + k log n)`.
  - Maintain a min-heap of size k while scanning all products — `O(n log k)`.
  - For large databases, use ANN indexes (FAISS, HNSW, ScaNN) to get ~`O(log n)` or
    sublinear retrieval with tiny accuracy loss.

### 5. Pytest

Key rules:

- Test files must start with `test_`.
- Test functions must start with `test_`.
- Your tests should be separate from your application code.
- **Why is `__init__.py` there?** To make Python treat the folder as a package. Without
  it, imports might fail depending on how you run pytest.
- **What is `pytest.ini`?** A configuration file that tells pytest where tests live,
  which markers exist, etc. Example:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v
```

This means: only look inside `tests/`, only run files that match `test_*.py`, and always
run in verbose mode.

---

## BitPin

### Probability and statistics

**1.** The probability of a fraud transaction is 0.008. If the transaction is fraud we
raise a flag 95% of the time; if it is not fraud we raise the flag 4% of the time. The
cost of not raising a flag on a fraud transaction is \$500, and the cost of raising a
flag on a non-fraud transaction is \$10. Should we deploy the model to production?

_Option A — not deploying the model:_

`Cost per transaction = P(fraud) * 500 = $4`

_Option B — deploying the model:_

```
Cost per transaction = P(~flag|fraud) * P(fraud) * 500 + P(flag|~fraud) * P(~fraud) * 10
                     = 0.05 * 0.008 * 500 + 0.04 * 0.992 * 10
                     = 0.2 + 0.3968
                     = $0.5968
```

So it makes sense to deploy the model to production.

**2.** We can either call a person to become our customer with a 100% success rate at \$5
cost, or send a push notification with a 30% success rate at \$1 cost. Which is better?

Say we want N customers. With the first approach we spend `5N $`; with the second
approach `10/3 N $` is enough, so the second approach is more cost-efficient.

### GenAI

**1.** How can you make sure your semantic-search model works well for queries like
`"تیشرت قرمز زیر ۲۰ دلار مردانه"`?

Two approaches:

- This approach ensures all conditions are met, but it increases the probability of
  returning no results. Use NER to understand the conditions specified in the query —
  such as color, price, and gender — and then apply these as variant filters in our QD
  search.
- This approach cannot guarantee that all conditions are met 100%, but it almost always
  returns a result. Train the model with more generated data and create batches with
  targeted hard negatives. For example, if our dataset contains a T-shirt with a positive
  product pair, use additional specifications of that product — such as color and price —
  add them to the query, and generate more training pairs (e.g., red T-shirt, T-shirt
  under \$20, red T-shirt under \$20). We can also repeat more important pairs more
  frequently; for instance, if price is a critical constraint, assign it a higher weight.
  Additionally, use similar but incorrect products as negatives, such as a blue T-shirt as
  a negative for a red T-shirt query. In this type of training, masking can also be
  effective, allowing the model to learn to attend to all specified constraints.

**2.** We trained a model to encode queries and product titles to embeddings. If we add
extra features to these embeddings (like price or CR) to use for personalized or
business-aware search, do the close embeddings still stay close to each other in this new
space?

In my experience, the embedding had 512 dimensions and I added fewer than 10 features.
Since the number of added features was insignificant compared to the embedding size, it
did not noticeably affect the system. However, theoretically, adding new dimensions does
change the distance calculations.

**3.** What if we want both text and image data at the same time when searching?

- Concatenation.
- Shared multimodal embedding space (CLIP-style).
- Averaging (only safe if text and image embeddings are in the same semantic space — a
  rule of thumb: if you didn't explicitly train the model to be averaged, don't average
  it).

### Statistical ML

**1.** After using K-fold cross-validation, which of the K scalers that were fit should I
use?

K-fold cross-validation is only used for model evaluation — when you want a robust
performance estimate instead of relying on one lucky/unlucky split. All the models you
train are temporary; you do **not** average model weights. After CV is done, you train
**one** final model, and the scaler of this final model should be used.

**2.** An archaeologist wants to take a picture of three pillars such that they are as far
from each other as possible (the worst case is the pillars hiding behind each other).
Where should they stand for the best picture?

When we take a picture, we map a 3D world onto a 2D plane (a reduction in
dimensionality). We want to preserve as much information as possible, meaning the
projected points have maximum variance. Therefore we use **PCA**.

### Python

**What is a generator?**

A generator is a special type of function that **returns values one at a time, instead of
all at once**. It uses the keyword **`yield`** instead of `return`. Generators save memory
and are good for large datasets (for example, **data loaders** are generators).

---

## CAT

### Statistics and probability

**1.** A basket contains eight red apples and two green apples. Find the probability that
all four apples drawn are red.

`P = 8/10 * 7/9 * 6/8 * 5/7 = 1/3`

**2.** Model answer: `[0, 1, 1, 0, 0]`; real target: `[1, 1, 1, 0, 1]`. Calculate
precision and recall.

```
precision = TP / (TP + FP)
recall    = TP / (TP + FN)

TP: 2   FP: 0   FN: 2

precision: 100%
recall:    50%
```

### Coding

**3.** Write a function to find the longest common prefix string amongst an array of
strings. If there is no common prefix, return an empty string `""`.

➡️ Solution: [`solutions/cat/longest_common_prefix.py`](solutions/cat/longest_common_prefix.py)

### Python

**4.** What is a magic method? Methods starting and ending with `__` that perform operator
overloading.

**5.** What is a decorator? A function that takes a function, adds some capability to it,
and returns another function.

➡️ Solution: [`solutions/cat/decorator.py`](solutions/cat/decorator.py)

### AI/ML

**6.** What is vLLM? A high-performance inference engine for LLMs that efficiently serves
models like LLaMA or GPT.

**7.** What is the difference between feature drift and concept drift?

**Feature drift** — the input feature distribution changes but the relationship between
input and target stays the same. The world looks different but the rules haven't changed.
For example, users used to search for cheap cellphones but now they search for expensive
ones. The model sees inputs it hasn't seen before, so performance degrades; retraining
usually fixes it.

**Concept drift** — the relationship between input and output changes (the rules of the
game change). For example, people used to mean fruit when searching for "apple"; now they
mean the cellphone. Now your model is fundamentally wrong. Retraining alone may not solve
it — you may need a new model design, new labels, new features.

🔥 **Rule of thumb**

- If inputs changed → feature drift.
- If predictions became wrong for the same inputs → concept drift.

---

## PertroPower

Imagine an agent that acts as our AI data scientist. In the first node it gets our
requirement; in the second node it translates the requirement to SQL; in the third and
fourth nodes it creates plots and reports. If the user mentions in the first node that
they want the plot in a specific color (like pink), how can this data be passed to the
third node? The second node's job is to create SQL queries — won't this type of data be
lost?

We should use a shared structured state that persists across all nodes. The first step
should extract and decompose the user's intent into different dimensions (e.g., data,
analysis, presentation). Each node then operates only on its relevant part of the state
and updates it without overwriting other parts. This avoids information loss and removes
the need for nodes to infer or recover missing intent.

---

## Goodfolio

**1.** Find the first unrepeated character in a string.
**2.** Given a list of numbers and a target, return all tuples whose sum equals that
target.

➡️ Solution: [`solutions/goodfolio/array_problems.py`](solutions/goodfolio/array_problems.py)

---

## Picnic

### System design

We have a section for recipes and articles. Design a personalized recommendation system
for this content.

---

## FanDuel

### System design

There's a SQLite database on this machine called `products.db`. It has a table called
`product_qa` with three columns: `product`, `question`, and `answer`. Build a simple app
where a store associate types in a question, and the app finds the most relevant answer
from that table and displays it — along with which product it came from.

My answer as an AI engineer was a **semantic-search design**: use an NL model to transform
all the questions in the `product_qa` table to embeddings and store those embeddings in a
vector DB like Qdrant, keeping the primary key as metadata. Then transform the incoming
question to an embedding using the same model and search for the closest question(s) using
the vector DB. Then either return the answer of the top 1 (semantic search) or generate an
answer using an LLM call providing the top-k answers as context.

**But I was rejected.**

I think the reason is I jumped into a complex, costly solution before trying out a simpler
one. A simpler solution:

Use **SQLite FTS5 + BM25 ranking**. SQLite has a built-in full-text search engine that
lets you create a special virtual table optimized for searching text columns, and BM25 is
an algorithm built on TF-IDF that helps estimate the relevance of a document. It won't
need any external vector DB or embedding model. My semantic approach does better when
questions are semantically different or the same, the table is large, and the app must
handle phrases well — but it's not wise to jump into that solution before testing the easy
one.

---

## Aveehealth

A data scientist hands you a Jupyter notebook. It trains an XGBoost model on a pandas
DataFrame, pickles the model, and has a few cells with ad-hoc feature engineering. Your
job is to get this into production. Walk me through what you do, in order.

My answer: we should convert the notebook to a Python script so it can be run end to end.
For the ad-hoc feature engineering I'd use a feature store like Feast; for model storage,
something like S3, plus MLflow for model versioning. I might change the code to use Dask
instead of pandas to speed things up. If the model is trained periodically, I'd use
something like Airflow, and I'd write a microservice in Python or Go to serve the model.

**I was accepted**, but an improved answer thinks about **reproducibility, correctness,
serving, monitoring, and operational risk**:

1. Clarify batch vs online inference, latency requirement, retraining cadence, expected
   input data, and success metric.
2. Make the notebook reproducible — pin dependencies, fix exact training data, rerun it
   end to end.
3. Extract the notebook into a package or pipeline.
4. Add model versioning and monitoring; define online and offline metrics.
5. Choose a serving pattern: a batch scoring job or an online API.
6. Containerize; CI/CD; unit and smoke tests; rollback support.
7. Finally, suggest making the code more mature and increasing speed/throughput by using
   Dask or Spark instead of pandas.

---

## Headspace

1. In our app, people can chat with our AI bot about issues like work pressure, anxiety, etc.
We have a section that recommends articles to users. How do you design it?

   My response:
   
   There are basically two ways to view this problem:
   
   1. I have enough data on what articles my users read and enjoy, and I can figure out
      relationships between users to see whether they look similar to each other. Based on
      that I can say user Y looks like user X, and if user X liked this article I should
      suggest it to user Y too. (**Collaborative filtering** — evidence from behavior.)
   2. Without considering how close or far users act, based on the features that users and
      articles have, and the info on what each user liked, we can create embeddings for users
      and articles. In this embedding space, the articles that users like are close to each
      other. (**Two-tower model** — relevance to the current problem.)
   
   For an MVP, I'd try collaborative filtering because it's straightforward and easy to
   implement. The catch: you need a significant amount of data, and it doesn't work for new
   users or new articles.
   
   In a high-scale real system we need both views, so we either combine the results of both
   approaches or (as I prefer) use a hybrid model from the beginning so we can choose:
   
   1. Two-tower contrastive model.
   2. Feature-aware matrix factorization.
   
   These two approaches are similar but not the same. It makes more sense to use feature-aware
   MF when you have rich, good-quality features for users and articles, for example:
   
   - U: `issue=anxiety, situation=workplace, urgency=high`
   - A: `context=breathing, length=short`
   
   In that case feature-aware MF can learn a latent representation for each feature and the
   relations between them. But if you only want to use user chat history and article content,
   a two-tower contrastive model makes more sense.
   
   Usually feature-aware MF isn't used by itself — theoretically it works, but for high-scale
   use cases it is too slow. Imagine a new user conversation happens: we then have to
   recompute the score between this user and all articles, which can be millions, so it's not
   good for real-time or fast processes. It's fine if you do it periodically (e.g. once a
   week), but if you want to update whenever a new article or new chat arrives, it's not
   realistic to recompute all those scores that fast. In the two-tower contrastive approach,
   when a new chat arrives we can easily and quickly recompute the user embedding; we already
   have article embeddings in a vector DB, and using heuristic nearest-neighbor approaches
   like HNSW we can get related articles in no time.
   
   Usually we use a **two-stage system**. A two-tower contrastive model retrieves
   semantically relevant candidates efficiently from the full catalog. We can include
   features such as urgency and article length in the towers, but the final score is still
   constrained to a similarity between independently computed embeddings. A ranker sees each
   user–article combination jointly and can model richer interactions (such as urgency with
   article length) using a larger computational budget, because it evaluates only hundreds of
   candidates. Explicit ranking features may also make individual score contributions easier
   to inspect. Finally, I can iterate on and retrain the ranker without retraining the
   retrieval model or rebuilding the vector index.
   
   After retrieval, we get to **ranking**:
   
   1. For each article and request, create features:
      - article: article length, retrieval score, etc.
      - request: urgency, age, etc.
   2. During training we attach a label indicating whether the article was helpful for that
      request. The factorization machine learns embeddings for feature values. Gradient
      descent makes interactions common in helpful examples more positive and interactions
      common in unhelpful examples more negative.
   3. At prediction, create the same features and sort by score.
   
   **Follow-up:** some articles are preferred in the daytime and others at night. What if it
   is daytime but the retrieved articles are for nighttime?
   
   Two approaches:
   
   1. If it is really necessary to show nighttime articles at night and daytime articles by
      day, we have to put it in the retrieval step — meaning we put it in the embedding. For
      example, take the embedding from the two-tower model, increase the embedding size, and
      put article time-preference and request time into the article and request embeddings,
      so in retrieval it plays a role and can be given more or less importance based on how
      much weight that dimension gets in the dot product.
   2. If it is just a preference, not a necessity, we can retrieve k articles and, if none are
      in the time we'd like, retrieve 2k, and so on.


2. We have an EBB application and we want to escalate if user is talking about doing something hurtful like commiting suidsice, how can we make sure we're doing it as fast as possible?
   
   To be as fast as possible I try to have two approaches run in **parallel**:
      1. A fast deterministic detector (rule based)
      2. A fast, light weight risk classifier ML model
   and escalate as soon as any of them detects high risk

   Cautions: this is the repsonse I said in the interview and I was rejected, I guess the approach was correct but I used some words that showed me naive. For example
      1. I said I'm going to keep a black list words and raise in case I see any of them, this approach is going to make so many mistakes like "I'm going to take all pills tonigh" is gonna
      pass and "I'm not suicidal" is going to raise, instead I should've said I'm going to have a rule based system that is gonna raise high risk for example in case of seeing some predefined
      phrases alongside some historical signals.
      2. I think I didn't emphasize enough on how recall is much more important than accuracy in this type of tasks so in case of timeout we fail and not ccontinue the conversation normally.
      3. The other weakness in my answer is I said I either raise or not, but it is wiser to have different severity levels

3. How do we feed chat history when it gets large?

   Of course, we don't feed the entire conversation history and make a summary of that before feeding it to the model, but that's all I said, I said I'll use a model to get the conversations and current
   history summary and output a new history summary and so on. what is more senior is to have a compact safety context object instead of just a summary text. A senior design would have multiple layers of
   context:
      1. current user message
      2. recent conversation window
      3. rolling safety summary
      4. retrieved high-risk past snippets

   instead of just text summary of previous chats. It should be something like
      ```json
      {
         "current_user_message": "I can't do this anymore tonight",
         "recent_turns": [
            {"role": "user", "text": "Everything feels pointless"},
            {"role": "assistant", "text": "I'm sorry you're feeling this way..."},
            {"role": "user", "text": "I don't think anyone would care if I disappeared."},
         ],
         "safety summary": {
            "previous_suicidal_ideation": true,
            "previous_self_harm_intent": false,
            "mentioned_plan": false,
            "mentioned_means": false,
            "mentioned_time": "tonight",
            "protective_factors_mentioned": ["friend", "therapy appointment"],
            "last_escalation_level": "P2",
            "highest_previous_level": "P2"
         },
         "retrieved_relevant_snippets": [
            "I don't want to wake up tomorrow",
            "I have pills at home"
         ]
      }
      ```
   This gives the model the important context without sending thousands of tokens.
   The arcitecture:
      ```json
         Last N turns
         safety summary
         safety relavant messages
      ```
   The **rolling safety summary** is the most important part

4. How can you monitor FP and FN and use these feedback to improve the system?
   FP are gathered easily, we understand if we escalated when we shouldn't have, we just have to gather the data.

   But FN are hidden, we should have a human-labeling pipeline over stratfied samples of non-escalated chats. For sampling we can use

      1. random samples of non escalated chats stratified over language, age, religion, region, etc.
      2. near threshold model score
      3. user later escalated
      4. user stopped chatting with us

   I would not just feed the erros back to the model blindly. I would build an error taxonomy:
      1. slang
      2. missed plan/means
      3. sarcasm
      4. multilingual miss
      5. etc
  
   Then I would decide what the fix is:
      1. data labelling
      2. threshold
      3. rules
      4. context summarization
      5. model architecture
  
   Before deploying a new model, I would replay it against frozen validation sets

---

## Sema4

1. **What is the difference between a skill and an agent?**

A **skill** is an instruction package. It tells the model how to do a specific class of
task, such as following a coding convention. It says: "here is how to do X."

An **agent** is an autonomous system that can plan, decide next steps, use tools, manage
state, and iterate toward a goal.

2. Create a small code working with MCP.
   
I implemented a read-only MCP server that exposed internal knowledge-base/runbook search to an AI coding assistant. The server exposed typed tools, resources, and prompts; the host application handled model interaction, user consent, and tool invocation. I used stdio for local IDE usage and Streamable HTTP for remote deployment.”

MCP is a client-host-server protocol

Common case: internal KB

| MCP primitive | Example              | Interview explanation                                                               |
| ------------- | -------------------- | ----------------------------------------------------------------------------------- |
| Tool          | `kb.search_docs`     | Model-callable function. Used when the model needs to search external/private data. |
| Resource      | `kb://docs/{doc_id}` | Read-only contextual data. Similar to a GET endpoint.                               |
| Prompt        | `answer_from_kb`     | Reusable workflow/template for the user or host.                                    |

3. Extracting invoice data from supplier documents with no fixed format

   Imagine a company receives thousands of supplier invoices every month by email, portal upload, scanned PDF, photo, or attached document. Every supplier uses a different invoice template. Some invoices are clean digital PDFs, some are scanned, some have tables across multiple pages, and some include extra pages such as purchase orders, delivery notes, bank details, or terms and conditions.

The business wants to automatically extract a structured object like:

```json
{
  "supplier_name": "ABC Manufacturing Ltd",
  "invoice_number": "INV-2026-00481",
  "invoice_date": "2026-06-12",
  "due_date": "2026-07-12",
  "purchase_order_number": "PO-77819",
  "currency": "GBP",
  "subtotal": 1250.00,
  "tax": 250.00,
  "total": 1500.00,
  "line_items": [
    {
      "description": "Steel brackets",
      "quantity": 100,
      "unit_price": 12.50,
      "amount": 1250.00
    }
  ]
}
```

Why this is difficult?
   1. Documents do not have the same layout

      **Text-only** extraction reads the document as a long string.

      **Layout-aware** extraction reads the document as text plus where that text appears on the page.

      Use layout-aware extraction rather than only text extraction. Especially for Tables which are much harder than single fields layout models are useful because they preserve the 2D structure
      
   2. OCR errors corrupt important fields

        Example: INV-10058 -> lNV-1O058

        Treat OCR as a noisy upstream signal, not the final answer.
      
   3. Some fields are ambiguous

         For example, an invoice may contain several dates:
            ```json
               Invoice Date: 2026-06-12
               Delivery Date: 2026-06-10
               Due Date: 2026-07-12
               Payment Terms: 30 days
            ```
         A naive model may extract the wrong date.
         Extract with evidence, not just values.
         ask it to return:
         ```json
            {
              "field": "invoice_date",
              "value": "2026-06-12",
              "evidence_text": "Invoice Date: 12/06/2026",
              "page": 1,
              "bbox": [420, 90, 560, 115],
              "confidence": 0.94
            }
         ```
