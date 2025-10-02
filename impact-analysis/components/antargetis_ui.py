
import streamlit as st
import json

def render_antargetis_card(recommendations):
    # Display each recommendation in a styled card

    if isinstance(recommendations, str):
        import json
        try:
            recommendations = json.loads(recommendations)
        except json.JSONDecodeError:
            st.error("Failed to decode recommendations JSON.")
            return

    if not isinstance(recommendations, list):
        st.error("Recommendations must be a list.")
        return
    
    for rec in recommendations:
        st.markdown(
            f"""
            <div style="
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: #f9f9f9;
        ">
            <h4 style="margin-bottom: 0.3rem;">{rec['target']}</h4>
            <span style="
                background-color: #e0e0e0;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                color: #333;
            ">{rec['type'].title()}</span>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; line-height: 1.4;">
                {rec['justification']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
