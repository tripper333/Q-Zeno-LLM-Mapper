import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from openai import OpenAI
from utils import get_embedding, compute_mu, compute_variance, compute_token_entropy, generate_field

# Page configuration
st.set_page_config(
    page_title="Zenome: Bridging Expectation and Outcome",
    layout="wide",
    page_icon="🧠",
)

# Custom CSS styling
st.markdown("""
<style>
    body {
        background-color: #0f1117;
        color: #FAFAFA;
    }
    .stSlider > div > div {
        background-color: #4f46e5;
    }
    .stSidebar {
        background-color: #1f2937;
    }
    .css-1v3fvcr {
        color: #d1d5db !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI()

# Logs
query_log = []
mu_log, entropy_log, var_log = [], [], []

# Sidebar UI
with st.sidebar:
    st.title("🧭 Query Navigation")

    query_input = st.text_input("🔍 Enter your natural language query")

    zeno_slider = st.slider(
        "📉 Query Ambiguity (μ influence)", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.01,
        help="Controls how 'uncertain' or ambiguous the query is. Higher = more noise."
    )

    show_entropy = st.checkbox("Overlay Entropy Channel", value=True)
    show_var = st.checkbox("Overlay Variance Channel", value=True)

    st.markdown("""
    ### 🧠 Metric Guide  
    - **μ (Zeno)**: Alignment between expectation & outcome  
    - **Entropy**: Complexity or uncertainty in phrasing  
    - **Variance**: Spread of semantic embedding  
    - **Cosine Drift**: Angular shift from previous queries *(coming soon)*  
    - **FFT Energy**: Latent frequency resonance *(coming soon)*  
    """)

    st.info("Each query generates a 3D coherence surface showing topology of response fields.")

# Main content
st.title("🧠 Zenome: Expectation-to-Outcome Mapper")

query = query_input
if st.button("🔄 Run Query") and query:
    # Compute metrics
    embedding = get_embedding(query)
    mu = compute_mu(embedding)
    entropy = compute_token_entropy(query)
    var = compute_variance(embedding)

    # Log metrics
    query_log.append(query)
    mu_log.append(mu)
    entropy_log.append(entropy)
    var_log.append(var)

    # Generate response surface
    X, Y, Z = generate_field(mu, entropy if show_entropy else 0.5, var if show_var else 0.1)

    # Plot 3D field
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="k", alpha=0.9)
    ax.set_title(f"Zeno μ Field\n{query}\nμ={mu:.4f}, H={entropy:.3f}, Var={var:.3f}")
    ax.set_xlabel("Latent X")
    ax.set_ylabel("Latent Y")
    ax.set_zlabel("Z Field")
    st.pyplot(fig)

# Scoreboard
if query_log:
    st.markdown("### 📊 Query Scoreboard")
    df = pd.DataFrame({
        "Query": query_log,
        "μ": mu_log,
        "Entropy": entropy_log,
        "Variance": var_log
    })
    st.dataframe(df)
    st.line_chart(df.set_index("Query")[["μ", "Entropy", "Variance"]])
