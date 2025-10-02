import streamlit as st
import pandas as pd
import altair as alt

# Mock timeline data (normally derived from topic modeling or clustering paper embeddings)
def get_author_timeline(author_name):
    # Simulated topic activity over time
    return pd.DataFrame({
        "Year": [2019, 2020, 2021, 2022, 2023],
        "Topic": ["CNNs", "GANs", "GANs", "Multi-Modal", "Foundation Models"],
        "Papers": [2, 4, 6, 3, 1]
    })

def render_author_timeline(author_name):
    st.subheader(f"📈 Topic Evolution: {author_name}")

    df = get_author_timeline(author_name)

    chart = alt.Chart(df).mark_line(point=True).encode(
        x="Year:O",
        y="Papers:Q",
        color=alt.value("#2a2a8e"),
        tooltip=["Year", "Topic", "Papers"]
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

    st.markdown("**Top Topics by Year:**")
    for _, row in df.iterrows():
        st.markdown(f"- **{row['Year']}**: {row['Topic']} ({row['Papers']} papers)")
