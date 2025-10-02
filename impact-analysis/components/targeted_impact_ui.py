import streamlit as st

# Sample structured data
def recommend_mock(author_name):
    return {
        "venues": [
            {
                "name": "Nature Plants",
                "justification": "High-impact interdisciplinary journal covering plant biology and biotechnology."
            },
            {
                "name": "Bioinformatics",
                "justification": "Well-known for machine learning applications in biological systems."
            }
        ],
        "collaborators": [
            {
                "name": "Dr. Maria Thompson",
                "affiliation": "CIMMYT (International Maize and Wheat Improvement Center)",
                "justification": "Leads large-scale breeding programs that align with the paper’s application goals."
            }
        ],
        "topics_to_expand": [
            {
                "topic": "Explainable AI in genomics",
                "justification": "Boosts interpretability and transparency, improving adoption by biologists and policymakers."
            }
        ],
        "dissemination_strategies": [
            {
                "strategy": "Submit research insights to the Global Food Security Policy Brief Series.",
                "justification": "Amplifies policy visibility and real-world application in food security efforts."
            },
            {
                "strategy": "Publish a visual summary on LinkedIn and ResearchGate.",
                "justification": "Improves reach among practitioners and funders outside academia."
            }
        ]
    }

# Styling helper
def render_card_v1(title,  justification=None, subtitle=None):
    return f"""
    <div style="
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    ">
        <h4 style="margin-bottom: 0.3rem;">{title}</h4>
        {f"<div style='font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;'>{subtitle}</div>" if subtitle else ""}
        <div style="font-size: 0.95rem; color: #333; line-height: 1.4;">{justification}</div>
    </div>
    """

def render_card(title, justification=None, subtitle=None):
    subtitle_html = f"""
    <div style='font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;'>
        {subtitle}
    </div>""" if subtitle else ""

    justification_html = f"""
    <div style="font-size: 0.95rem; color: #333; line-height: 1.4;">
        {justification}
    </div>""" if justification else ""

    return f"""
    <div style="
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    ">
        <h4 style="margin-bottom: 0.3rem;">{title}</h4>
        {subtitle_html}
        {justification_html}
    </div>
    """

def render_targeted_impact(recommendations):
    # Render all sections
    #st.title("🔍 Targeted Impact Recommendations")

    if not recommendations or not isinstance(recommendations, dict):
        st.warning("No targeted impact data available.")
        return

    for section, items in recommendations.items():

        st.markdown(f"### {section.replace('_', ' ').title()}")

        for item in items:
            if section == "venues":
                st.markdown(render_card(
                    title=item["name"],
                    justification=item["justification"]
                ), unsafe_allow_html=True)

            elif section == "collaborators":
                st.markdown(render_card(
                    title=item["name"],
                    justification=item["justification"],
                    subtitle=item.get("affiliation", "")
                ), unsafe_allow_html=True)

            elif section == "topics_to_expand":
                st.markdown(render_card(
                    title=item["topic"],
                    justification=item["justification"]
                ), unsafe_allow_html=True)

            elif section == "dissemination_strategies":
                st.markdown(render_card(
                    title=item["strategy"],
                    justification=item["justification"]
                ), unsafe_allow_html=True)
