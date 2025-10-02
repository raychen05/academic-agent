import streamlit as st
from services import patent_policy_detector
from components import memory

def get_mock_input():
    return {
        "title": "A Transformer-based Approach for Quantum Chemistry",
        "abstract": "We propose a transformer architecture that replaces density functional theory in molecular property prediction."
    }


def get_mock_output():
    return {
        "impact_detected": True,
        "sources": [
            {
            "type": "patent",
            "title": "System and method for neural network-based quantum simulations",
            "url": "https://patents.google.com/patent/US2024032193A1"
            },
            {
            "type": "policy",
            "title": "US DOE Strategic Plan on AI in Science",
            "url": "https://energy.gov/ai-plan"
            }
        ],
        "llm_explanation": "The paper has been referenced in a patent filed by XYZ Corp and a U.S. Department of Energy strategic document. This indicates its influence in both commercial innovation and government policy."
    }


def render_impact_detector(input):

    # st.title("Policy & Patent Impact Detector")
    #title = st.text_input("Paper Title")
    #abstract = st.text_area("Paper Abstract")

   # if st.button("Analyze Impact"):
    result = memory.get_object("patent_impact_llm")
    if not result:
        result = patent_policy_detector.detect_with_llm_explanation(input["title"], input["abstract"])
        memory.set_object("patent_impact_llm", result)
    if result["impact_detected"]:
        st.success("Real-world impact detected!")
        for src in result["sources"]:
            st.markdown(f"**{src['type'].title()}**: [{src['title']}]({src['url']}) (Score: {src['score']:.2f})")
        st.markdown("**Explanation:**")
        st.info(result["llm_explanation"])
    else:
        st.warning("No real-world impact found in known policy or patent sources.")
