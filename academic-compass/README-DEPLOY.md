###  ResearchCompass - Cloud Deployment Guide

This guide demonstrates how to deploy your full-stack Agent (ScholarGPT-X / ResearchCompass) on a server using Docker Compose with a one-click setup.

####  1️⃣ Environment Preparation

A server (Linux Ubuntu recommended)
Docker and Docker Compose installed
A valid OpenAI API Key


####  2️⃣ Clone & Configure
Let me know if you'd like the rest of the guide translated too!

```bash
git clone https://github.com/yourname/research_compass.git
cd research_compass
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY 和数据库连接

```

---

Let’s complete  ResearchCompass Starter Repo with a production-ready docker-compose.yml so you can spin up:

- ✅ FastAPI backend
- ✅ Superset dashboard
- ✅ Postgres DB (for logs, feedback, citation data, whatever you want)
- ✅ Optional: PgAdmin for easy DB admin


- 1️⃣ Example docker-compose.yml
  
- 2️⃣ Example Dockerfile.api
  
- 3️⃣ Example .env
The PG_HOST=postgres matches your docker-compose service name. 

- 4️⃣ How to spin up

```bash
  # Build and start everything:
docker-compose up --build

# Or run detached:
docker-compose up -d
```

-	FastAPI API: http://localhost:8000/docs
-	Superset UI: http://localhost:8088
-	PgAdmin: http://localhost:5050	


- 5️⃣ Initialize Superset
  
Inside the Superset container:
```bash
docker exec -it researchcompass_superset superset fab create-admin
docker exec -it researchcompass_superset superset db upgrade
docker exec -it researchcompass_superset superset init
```

Then log in with your admin user.


- 6️⃣ Next-level tips


✅ Connect Superset ➜ Postgres

In Superset, add your Postgres DB:
```tetx
postgresql+psycopg2://compass_user:compass_pass@postgres:5432/compass_db
```

✅ Mount your local code

If you want hot-reload:
```
    volumes:
      - .:/app
```

✅ Persist data

The postgres_data named volume keeps your DB even if containers restart.

✅ Secrets

Don’t forget to manage real keys safely with .env and docker-compose.yml.

⸻

-  7️⃣ Final structure

```plaintext
    research_compass/
    ├── Dockerfile.api
    ├── docker-compose.yml
    ├── .env
    ├── run_api.py
    ├── ...
```

🎉 You now have:

- ✅ Local dev stack: FastAPI + Postgres + Superset + PgAdmin
- ✅ One-command orchestration
- ✅ Easy to deploy on Render, Fly.io, Railway, or any VPS
- ✅ Ready for local experiments or team sharing

---

-  7️⃣  🏁 Run end-to-end

```bash
# 1️⃣ Upload some PDFs to data/sample_papers/

# 2️⃣ Run: 
python scripts/upload_papers.py

# 3️⃣ Run planner: 
python run.py --query "Explain the impact of GPT models."

# 4️⃣ Or test with FastAPI:
uvicorn run_api:app --reload

```