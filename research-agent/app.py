import streamlit as st
from agent.run_agent import run_agent
from learning.feedback_handler import handle_feedback

st.set_page_config(page_title="Research Expert Agent", layout="wide")

st.title("Research Expert AI Agent")
query = st.text_input("Ask a research question:", "")

if query:
    with st.spinner("Thinking..."):
        response, docs, output_id = run_agent(query)
        st.markdown("### Answer:")
        st.markdown(response)

        st.markdown("---")
        st.markdown("### Top Documents Used:")
        for doc in docs:
            st.markdown(f"- **{doc['title']}**")

        st.markdown("---")
        st.markdown("### Was this helpful?")
        feedback = st.radio("Feedback", ["👍 Yes", "👎 No"])
        comments = st.text_area("Additional comments")
        if st.button("Submit Feedback"):
            handle_feedback({
                "rating": 1 if feedback == "👍 Yes" else 0,
                "comments": comments
            }, query, docs)
            st.success("Thank you! The agent will learn from this.")