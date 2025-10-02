import streamlit as st
from services.attribution import attribute_paper
import pandas as pd
import matplotlib.pyplot as plt
from services.llm_helpers import call_llm


def get_collab_impact_mock():
    return {
        "paper": { "title": "...", "doi": "...", "citations": 12, "year": 2022 },
        "method": "positional",
        "authors": [
            {"name":"Alice Smith", "affiliation":"Univ A","role":"first","share":0.45812,"absolute_impact":5.4974},
            {"name":"Bob Jones", "affiliation":"Univ B","role":"coauthor","share":0.18032,"absolute_impact":2.1638},
            {"name":"Carol Lee","affiliation":"Univ A","role":"last, senior","share":0.36156,"absolute_impact":4.3389}
        ],
        "institutions": {
            "Univ A": {"share": 0.81968, "absolute_impact": 9.8363, "authors": [...]},
            "Univ B": {"share": 0.18032, "absolute_impact": 2.1638, "authors": [...]}
        },
        "grants": {
            "G1": {"allocation":0.6667, "authors":[ ... ]},
            "G2": {"allocation":0.3333, "authors":[ ... ]}
        }
    }
 
def explain_collab_llm(paper_metadata):
    prompt = f"""
You are an expert research-metrics analyst. Given the following paper metadata and computed attribution shares, 
produce a 1-2 sentence human-readable explanation for each author describing why they received their share. 
Be concise and specific about role, authorship position, and any grant linkage.

Input (JSON):
{{
  "paper": {{"title": "{paper_metadata.title}", "doi": "{paper_metadata.doi}", "citations": {paper_metadata.citations}}},
  "authors": [
    {{"name": "Alice Smith", "affiliation": "Univ A", "role": "first", "share": 0.45812}},
    {{"name": "Bob Jones", "affiliation": "Univ B", "role": "coauthor", "share": 0.18032}}
  ],
  "institutions": {{
    "Univ A": {{"share": 0.81968}},
    "Univ B": {{"share": 0.18032}}
  }},
  "grants": {{
    "G1": {{"allocation": 0.6667}},
    "G2": {{"allocation": 0.3333}}
  }}
}}

Return JSON Format:
{{
  "explanations": [
    {{"name": "Alice Smith", "text": "..."}},
    {{"name": "Bob Jones", "text": "..."}}
  ]
}}
"""
    return call_llm(prompt)

def resolve_collab_llm(paper_metadata):
    prompt = f"""
You are a neutral bibliometrics mediator. Alice contests that her share is too low.
She claims she led the experiments and wrote half of the methods.
Using the existing attribution (method: positional + role multipliers),
suggest a fair adjustment and write a short justification to present
to the authors and the institutional admin.

Paper metadata: {paper_metadata}

Output a short JSON with keys: {{
    "proposed_shares": {{"Alice Smith": 0.5, "Bob Jones": 0.2}},
    "justification": "Alice led the experiments and contributed significantly to the methods section."
}}
    """
    return call_llm(prompt)


def render_collab_impact_attribution():

    with st.expander("Paste sample JSON (or edit)"):
        sample = {
            "title": "Large Language Models for Predicting Catalyst Reaction Pathways",
            "doi": "10.1000/exampledoi",
            "authors": [
                {"name": "Alice Smith", "affiliation": "Univ A", "role": "first"},
                {"name": "Bob Jones", "affiliation": "Univ B", "role": "coauthor"},
                {"name": "Carol Lee", "affiliation": "Univ A", "role": "last, senior"}
            ],
            "citations": 12,
            "year": 2022
        }
        st.code(sample, language="json")

    st.sidebar.header("Attribution options")
    method = st.sidebar.selectbox("Method", ["positional", "harmonic", "fractional"], index=0)
    first_w = st.sidebar.slider("First author weight", 0.0, 0.8, 0.45)
    last_w = st.sidebar.slider("Last author weight", 0.0, 0.8, 0.35)
    use_role = st.sidebar.checkbox("Use role multipliers (first/corresponding/last)", True)

    st.subheader("Paper input")
    title = st.text_input("Title", sample["title"])
    doi = st.text_input("DOI (optional)", sample["doi"])
    year = st.number_input("Year", value=sample["year"])
    citations = st.number_input("Citations", min_value=0, value=sample["citations"])
    # Small author editor
    st.write("Authors (name | affiliation | role)")
    authors_input = st.text_area("One per line: name|affiliation|role",
                                value="\n".join([f'{a["name"]}|{a["affiliation"]}|{a.get("role","")}' for a in sample["authors"]]),
                                height=120)
    authors = []
    for line in authors_input.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 2:
            name = parts[0]
            aff = parts[1]
            role = parts[2] if len(parts) >= 3 else ""
            authors.append({"name": name, "affiliation": aff, "role": role})

    if st.button("Compute Attribution"):
        paper = {"title": title, "doi": doi, "authors": authors, "citations": citations, "year": year}
        # For demo, no grants passed
        res = attribute_paper(paper, method=method, first_weight=first_w, last_weight=last_w, use_role_multiplier=use_role, grants=None)
        st.success("Attribution computed")

        # --- Top summary card ---
        left, mid, right = st.columns([2,3,2])
        left.markdown("### 📄 Paper")
        left.write(res["paper"]["title"])
        left.write(f"DOI: {res['paper'].get('doi','-')}")
        left.write(f"Citations: {res['paper'].get('citations',0)}")

        mid.markdown("### 🧾 Summary")
        # nice badges
        total_authors = len(res["authors"])
        mid.markdown(f"- **Authors:** {total_authors}")
        mid.markdown(f"- **Method:** {res['method']}")
        mid.markdown(f"- **Normalized shares sum:** {sum([a['share'] for a in res['authors']]):.4f}")

        right.markdown("### 🔍 Quick Insights")
        # highlight highest contributor and institution
        top_author = max(res["authors"], key=lambda x: x["share"])
        top_inst = max(res["institutions"].items(), key=lambda kv: kv[1]["share"])
        right.markdown(f"**Top author:** {top_author['name']} ({top_author['share']:.2%})")
        right.markdown(f"**Top institution:** {top_inst[0]} ({top_inst[1]['share']:.2%})")

        st.markdown("---")

        # --- Author cards ---
        st.markdown("## 👥 Author Attributions")
        cols = st.columns(len(res["authors"]))
        for col, a in zip(cols, res["authors"]):
            col.markdown(
                f"""
                <div style="background:#ffffff;padding:16px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.06)">
                <h4 style="margin:0 0 8px 0">{a['name']}</h4>
                <div style="color: #666">{a['affiliation']} — {a['role']}</div>
                <div style="margin-top:8px"><b>Share</b>: {a['share']:.2%}</div>
                <div><b>Absolute impact</b>: {a['absolute_impact']}</div>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown("---")
        # --- Institution table ---
        st.markdown("## 🏛 Institutions")
        inst_rows = []
        for inst, info in res["institutions"].items():
            inst_rows.append({"institution": inst, "share": info["share"], "absolute_impact": info["absolute_impact"], "n_authors": len(info["authors"])})
        inst_df = pd.DataFrame(inst_rows).sort_values("share", ascending=False)
        st.table(inst_df.style.format({"share":"{:.2%}", "absolute_impact":"{:.2f}"}))

        st.markdown("---")
        # --- Plot: authors shares ---
        st.markdown("## 📈 Visual: Author Shares")
        fig, ax = plt.subplots(figsize=(8, 3))
        names = [a["name"] for a in res["authors"]]
        shares = [a["share"] for a in res["authors"]]
        ax.barh(names[::-1], shares[::-1])
        ax.set_xlabel("Normalized Share (sum=1)")
        st.pyplot(fig)

        # --- Export JSON button ---
        import json, io
        buf = io.StringIO()
        json.dump(res, buf, indent=2)
        st.download_button("Download attribution JSON", buf.getvalue(), file_name="attribution.json", mime="application/json")
