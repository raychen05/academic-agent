import streamlit as st

# Optional: Capitalize and space out keys for better labels
def format_label(key):
    return key.replace("_", " ").title()

def render_metric(label, value):
    return f"""
        <div style="background-color:#f7f7f7;
                    border-radius:8px;
                    padding:18px;
                    text-align:center;
                    border:1px solid #ddd;
                    margin:4px;">
            <div style="font-size:16px; color:#555;">{label}</div>
            <div style="font-size:28px; font-weight:bold; color:#2a2a8e;">{value}</div>
        </div>
    """

def render_metric_card(metrics):
    """
    Render a metric card with multiple metrics in a single row.
    :param metrics: Dictionary of metrics to display
    """
    if not metrics:
        st.warning("No metrics available to display.")
        return

    #st.markdown("---")  # Add a horizontal line for separation
    #st.markdown("### Metrics Overview")  # Section title

    # Create one column per metric
    cols = st.columns(len(metrics))  # auto-distributes evenly

    # Loop through metrics and display each as a metric card
    for col, (key, value) in zip(cols, metrics.items()):
        with col:
            if isinstance(value, float):
                display_val = f"{value:.2f}"
            elif isinstance(value, int):
                display_val = f"{value:,}"  # comma-separated thousands
            else:
                display_val = str(value)  # fallback

            #st.metric(label=format_label(key), value=display_val)
            html = render_metric(format_label(key), display_val)
            st.markdown(html, unsafe_allow_html=True)