import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import streamlit as st
from sklearn.linear_model import LinearRegression
from services.summarize import summarize_citation_growth

def plot_forecast_mock(author_name):
    years = np.arange(2020, 2026)
    citations = np.array([50, 100, 200, 300, 400, 500])
    forecast = citations + np.random.randint(10, 100, len(citations))

    fig, ax = plt.subplots()
    ax.plot(years, citations, label="Citations")
    ax.plot(years, forecast, '--', label="Forecast")
    ax.set_title(f"Citation Forecast for {author_name}")
    ax.legend()
    return fig


def plot_forecast(author_name):
    # Example: citation counts per year
    data = {
        "year": [2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "citations": [3, 7, 15, 30, 60, 90, 120]
    }
    df = pd.DataFrame(data).set_index("year")

    # Train ARIMA model
    model = ARIMA(df["citations"], order=(2,1,2))  # (p,d,q)
    model_fit = model.fit()

    # Forecast 3 years
    forecast = model_fit.forecast(steps=3)
    forecast_years = [2024, 2025, 2026]

    # Combine with original data
    forecast_df = pd.DataFrame({"year": forecast_years, "citations": forecast})
    all_df = pd.concat([df.reset_index(), forecast_df], ignore_index=True)

    # Plot
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.plot(df.index, df["citations"], label="Historical", linewidth=0.5)
    ax.plot(forecast_years, forecast, linestyle='--', color='orange', label="Forecast", linewidth=0.5)
    ax.set_xlabel("Year", fontsize=4)
    ax.set_ylabel("Citations", fontsize=4)
    ax.set_title("Citation Forecast", fontsize=4)
    ax.tick_params(axis='both', labelsize=4)
    for spine in ax.spines.values():
        spine.set_linewidth(0.1)  # Thicker frame line
    ax.legend(fontsize=4)

    st.pyplot(fig)

    growth_data = {
        "annual_citations": df["citations"].to_dict(),
        "forecast": forecast_df.set_index("year")["citations"].to_dict()
    }

     # LLM Summary
    summary = summarize_citation_growth("A Transformer-based Approach for Quantum Chemistry", growth_data)

    st.markdown(
        f"""
        <div style="padding:15px; border-radius:10px; background-color:#f5f5f5; border-left: 5px solid #4CAF50;">
        <h4 style="margin-top:0;">📜 Summary</h4>
        <p>{summary}</p>
        </div>
        """,
        unsafe_allow_html=True
    )




def plot_forecast_lr(author_name):

    # Example input features for training
    X = np.array([
        [5, 120, 8.5, 20],   # age, current citations, JIF, h-index
        [4, 90, 9.1, 18],
        [3, 60, 7.2, 17],
        [2, 30, 6.8, 15]
    ])
    y = np.array([150, 130, 100, 60])  # Future citations

    # Train regression model
    reg = LinearRegression()
    reg.fit(X, y)

    # Predict for a new paper
    new_input = np.array([[1, 15, 5.5, 12]])  # New paper
    predicted_citations = reg.predict(new_input)

    st.write("Predicted citations in 3 years:", int(predicted_citations[0]))
