from sentence_transformers import SentenceTransformer, util
import json
from expert_finder.prompt import build_prompt
from expert_finder.data_loader import load_expert_profiles
import openai
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
openai.api_key = os.getenv("OPENAI_API_KEY")

def find_experts(title, abstract, excluded_institution, preferred_region, min_citations):
    query_text = title + " " + abstract
    query_embedding = model.encode(query_text, convert_to_tensor=True)

    experts = load_expert_profiles()
    scored_experts = []

    for expert in experts:
        if expert["total_citations"] < min_citations:
            continue
        if excluded_institution and excluded_institution.lower() in expert["affiliation"].lower():
            continue
        if preferred_region and preferred_region.lower() not in expert.get("region", "").lower():
            continue

        expert_embedding = model.encode(" ".join(expert["expertise"]), convert_to_tensor=True)
        score = float(util.cos_sim(query_embedding, expert_embedding)[0])
        if score > 0.4:
            expert["score"] = score
            scored_experts.append(expert)

    scored_experts = sorted(scored_experts, key=lambda x: x["score"], reverse=True)[:10]

    prompt = build_prompt(title, abstract, scored_experts)
    llm_response = call_llm(prompt)
    return llm_response

def call_llm(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful academic expert recommender."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    content = completion["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except:
        return []
