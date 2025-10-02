### ResearchCompass 🚀

**ScholarGPT-X: Next-Gen Academic Research Agent**

### Setup Environment

### activate the local pipenv
cd /path/to/your/project
export PIPENV_IGNORE_VIRTUALENVS=1
export PIPENV_VENV_IN_PROJECT=1
pipenv --rm  # remove old env
pipenv install
pipenv --venv  # should now be in ./venv

pipenv run pip install -r requirements.txt

---


### Replicate SciSpace core + self-developed advanced modules, supporting:

- AI Paper Reader
- Ask AI
- Semantic Search
- Citation Graph
- Novelty Detection
- Expert Finder
- Grant Recommender
- Researcher Impact
- Self-Learning & Feedback Loop

#### 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Initilize vector db
python scripts/init_db.py

# Start Streamlit UI
streamlit run ui/app.py


# create package
zip -r research_compass_starter.zip research_compass/

# install depedncies
pip install fastapi uvicorn pydantic

## Run api service
uvicorn run_api:app --reload --port 8000

### visit
POST http://127.0.0.1:8000/ask
Body: { "query": "Give me a summary for BERT paper." }
```

#### Starter Repo Stucture

```plaintext
research_compass/
├── agent/
│   ├── planner.py
│   ├── memory.py
│   ├── state.py
│   └── feedback.py
│
├── tools/
│   ├── paper_reader.py
│   ├── semantic_search.py
│   ├── co_writer.py
│   ├── citation_graph.py
│   ├── novelty.py
│   ├── expert_finder.py
│   ├── grant_finder.py
│   ├── impact_eval.py
│   └── experiment_aggregator.py
│
├── data/
│   ├── memory_index/
│   └── sample_papers/
│
├── config/
│   ├── prompts.yaml
│   ├── settings.yaml
│
├── ui/
│   ├── app.py
│   ├── components/
│   └── assets/
│
├── scripts/
│   ├── init_db.py
│   ├── test_pipeline.py
│   └── upload_papers.py
│
├── run.py
├── requirements.txt
├── README.md
└── .env.example
```


####  Final pytest structure

```plaintext
tests/
 ├── test_impact_eval.py
 ├── test_paper_reader.py
 ├── test_expert_finder.py
 ├── test_grant_finder.py
 ├── test_experiment_aggregator.py
 ├── test_citation_graph.py
 ├── test_novelty.py
 ```


#### How to run all

``` bash
# Install pytest if needed
pip install pytest

# Run everything
pytest tests/ -v

# Run one test
pytest tests/test_memory_manager.py -v

```

---


#### Collaboration Module 

-	Store annotations/comments per paper and per user.
-	Support adding, updating, deleting comments.
-	Support retrieving comments by paper or user.
-	Use SQLite for persistence (lightweight, easy to test).
-	Designed as a class CollaborationManager.


####  AI Paper Reader module

-	PDF parsing (section-by-section)
-	Terminology extraction (simple keyword matching or more advanced if you want)
-	AI Q&A over the text chunks

   *  Next level ideas
    -	Show term highlights inline with markdown or st.markdown.
    -	Save sections & embeddings to a vector DB for faster reuse.
    -	Chain to OpenAI ChatCompletion to expand the QA from the relevant chunk.
    -	Enable multi-paper QA — easy with your ResearchCompass planner!



#### TrendDetector  module

-	Ingest publication metadata (e.g., topic + year)
-	Aggregate counts by topic over time
-	Use simple NLP (like keyword normalization)
-	Perform time series analysis to detect trends
-	Visualize growth trends or return them in JSON

* Real-world tips
    -	Connect to your publications DB or Elasticsearch
    -	Use named entity recognition to extract topics dynamically
    -	Replace pandas with Polars for bigger data
    -	Use Prophet or ARIMA for advanced forecasting


#### CitationGenerator module

-	Take basic publication metadata (title, authors, year, journal, DOI, etc.)
-	Format it into BibTeX, APA, or any style you want
-	Be easy to plug into your ResearchCompass UI or planner


  * Realistic usage
    -	Integrate with your Streamlit UI: let users paste or upload metadata
    -	Support DOI lookups: auto-fetch BibTeX with requests + Crossref API
    -	Store user’s generated citations in their MemoryManager

  * ⚡️ Extra real-world ideas
    -	DOI Lookup — auto-fetch metadata from Crossref or OpenAlex
    -	Download Button — let user download BibTeX as .bib
    -	Clipboard copy — add st.code or st.text_area for easy copy
    -	 Memory Save — store user’s favorite citations in your agent’s MemoryManager!



####  Self-Learning Agent module

-	It remembers each user’s research interests and preferences
-	Stores and updates user embeddings in your FAISS + SQLite memory
-	Supports RAG (Retrieval-Augmented Generation) to personalize answers

* How it works
    - store_user_profile:  Creates a single embedding for a user’s interests + preferences and saves it in FAISS + SQLite
    - retrieve_user_profile: Searches for the nearest stored user profile
    - recommend: Example personalized generation: retrieves profile + combines with user query
    - _embed_text: Uses dummy random embeddings for testing; replace with real OpenAI embeddings for production


#### Auto-Summarization

-	It uses a pre-trained BART model (facebook/bart-large-cnn) for abstractive summarization.
-	Merges multiple abstracts → produces one short, human-like summary.
-	Good for generating the intro paragraph for a systematic review draft!



#### Research Gap Finder

  - Extracting key topics & trends.
  - Checking what topics are frequently mentioned vs. under-discussed.
  - Generating gap suggestions with simple heuristics (e.g., “X is often mentioned, but Y is rarely studied in context of Z”).

    * Next-Level Ideas

    - 🚀 Add semantic clustering: group topics automatically.
    - 🧠 Use a larger LLM (e.g., GPT-4) for chain-of-thought or custom prompts.
    - 📈 Visualize topic coverage as bar charts.
    - 📄 Export the report as a PDF or markdown.
    - 🔗 Connect with your reference manager or Notion workspace.


#### Citation Quality Analysis module

✅ How it works
    - 🚀 Zero-shot classification: uses natural language inference (NLI) to label each citation context.
    - 📊 Supports systematic reviews: shows whether citations build on, refute, or merely mention prior work.
    - 🔍 Realistic for small corpora; for large corpora you could chunk batches or fine-tune on citation stance data.

🔥 How to improve it
    - Fine-tune with real citation stance data (e.g., SciCite dataset).
    - Add context window (1–2 sentences before/after the citation marker).
    - Build Streamlit dashboard to visualize stance distributions.
    - Combine with sentiment analysis for deeper stance nuance.


#### Paper Quality Estimation module


✅ How it works
    -  Checks DOI against a known retraction list.
    - 🚩 Flags journals in a blacklist.
    - 📉 Warns about low citations or suspicious phrases.
    - ✅ Extensible: plug in more heuristics or chain to a larger LLM for deeper review.

⚡ How to Make It Even Smarter

    -  🔗 Connect to live Retraction Watch or Crossref Retraction API.
    -  🔍 Pull citation counts automatically from Crossref or Semantic Scholar.
    -  🧠 Use a small LLM to highlight suspicious phrasing (e.g., paper mill detection).
    -  📄 Add upload for BibTeX or RIS files.
    -  📤 Export the report as PDF or CSV.



##### Collaboration Insights module 


✅ How it works
    - 1️⃣ Basic co-authorship network extraction from a list of papers
    - 2️⃣ Finds top collaborators for a given researcher or institution
    - 3️⃣ Suggests potential new collaborators by analyzing frequent co-authorship patterns and gaps


✅ How It Works
    - 	🔗 Builds a co-authorship graph from your papers.
    - 	🔍 top_collaborators finds your closest connections.
    - 	🌱 suggest_new_collaborators finds people you’re not yet connected to, but you share many common co-authors with — a simple link     - 	🏛️ institution_trends shows which institutions are most active


✅ Next-Level Ideas

    - 🚀 Add edge weights for multiple co-authorships over time.
    - 🗂️ Use ORCID IDs for accurate name disambiguation.
    - 🌐 Visualize the network with pyvis or networkx + matplotlib.
    - 💡 Extend with clustering to find research groups or communities.


✅ Ideas to make it smarter
    - Add edge weights for repeated collaborations.
    - Visualize the network with pyvis or networkx + matplotlib.
    -  Plug in ORCID IDs for disambiguation.
    - Support BibTeX or CSV uploads instead of manual input.
    - Highlight international or cross-institutional collaborations.
    -  Export results as a CSV or PDF report.


---

🚫 Missing Important AI Features (Compared to What’s Possible Now)

1.	Semantic Concept Extraction: advanced topic modeling to see trends or related concepts at scale.
2.	Auto-Summarization: multi-paper summarization (e.g., systematic review drafts).
3.	Conversational Q&A: chat interface to ask complex research questions across papers.
4.	Research Gap Finder: highlight under-explored areas or unanswered questions.
5.	Code/Data Detection: AI to check if a paper has reproducible code/data or links to them.
6.	Citation Quality Analysis: tell you if citations are supportive, critical, or merely mention a work.
7.	Paper Quality Estimation: warn about retracted or low-quality publications.
8.	Collaboration Insights: smart suggestions for potential collaborators or institution-level trends.
9.	Workflow Integration: integrate with citation managers, note-taking apps, or LLMs natively.


-- sqlite3