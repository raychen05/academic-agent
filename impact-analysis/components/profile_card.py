import streamlit as st

def recommend_mock(author_name):
    return {
        "name": "Dr. Jane Doe",
        "rid": "R-1234-5678",
        "orcid": "0000-0002-1825-0097",
        "organization": "Harvard University",
        "state": "MA",
        "country": "USA",
        "summary": (
            "Dr. Jane Doe is a leading expert in AI and Neuroscience, with over 50 peer-reviewed papers and several patents. "
            "Her work bridges machine learning with cognitive science, contributing to advancements in both theory and application."
        )
    }


# <h3 style="margin-bottom: 1rem;">👤 Author Profile</h3>
# Reusable card-rendering function
def render_author_card(researcher: dict):
    
    # Card styling
    st.markdown("""
        <style>
        .profile-card {
            background-color: #f9fafb;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            font-family: 'Segoe UI', sans-serif;
            max-width: 600px;
            margin: auto;
        }
        .profile-header {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 0.5rem;
        }
        .profile-subheader {
            font-size: 0.95rem;
            color: #4b5563;
            margin-bottom: 1.2rem;
        }
        .profile-location {
            font-size: 0.95rem;
            color: #374151;
            margin-bottom: 1rem;
        }
        .profile-summary-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-top: 1rem;
            color: #111827;
        }
        .profile-summary {
            font-size: 0.95rem;
            color: #374151;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # HTML Card
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-header">🧑 {researcher["name"]}</div>
        <div class="profile-subheader">
            RID: {researcher["rid"]} | ORCID: {researcher["orcid"]}
        </div>
        <div class="profile-location">📍 {researcher["organization"]} · {researcher["state"]} · {researcher["country"]}</div>
        <hr style="border: none; border-top: 1px solid #e5e7eb;" />
        <div class="profile-summary-title">📝 Profile Summary</div>
        <div class="profile-summary">{researcher["summary"]}</div>
    </div>
    """, unsafe_allow_html=True)