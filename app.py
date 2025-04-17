import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from openai import OpenAI
import tiktoken
from utils import get_embedding, compute_mu, compute_variance, compute_token_entropy, generate_field

st.set_page_config(page_title="Q-Zeno Topology Explorer", layout="wide")

st.title("🌐 Q-Zeno Topology Explorer")
st.markdown("Semantic topology visualized using DGFT-style latent fields")

client = OpenAI()
query_log = []
mu_log, entropy_log, var_log = [], [], []

# Sidebar options
with st.sidebar:
    st.header("Metric Channels")
    show_mu = st.checkbox("Zeno μ (Semantic Coherence)", True)
    show_entropy = st.checkbox("Entropy (Token Complexity)", True)
    show_var = st.checkbox("Variance (Embedding Spread)", True)
    st.markdown("---")
    st.markdown("🧠 **Metric Guide**
- μ: Embedding norm coherence
- H: Token entropy
- Var: Spread of embedding components")

query = st.text_input("Enter a query to visualize:")
if st.button("Run") and query:
    embedding = get_embedding(query)
    mu = compute_mu(embedding)
    entropy = compute_token_entropy(query)
    var = compute_variance(embedding)

    query_log.append(query)
    mu_log.append(mu)
    entropy_log.append(entropy)
    var_log.append(var)

    X, Y, Z = generate_field(mu, entropy if show_entropy else 0.5, var if show_var else 0.1)
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="k", alpha=0.9)
    ax.set_title(f"Zeno μ Field
{query}\nμ={mu:.4f}, H={entropy:.3f}, Var={var:.3f}")
    ax.set_xlabel("Latent X")
    ax.set_ylabel("Latent Y")
    ax.set_zlabel("Z Field")
    st.pyplot(fig)

if query_log:
    st.markdown("### 📊 Query Scoreboard")
    import pandas as pd
    df = pd.DataFrame({
        "Query": query_log,
        "μ": mu_log,
        "Entropy": entropy_log,
        "Variance": var_log
    })
    st.dataframe(df)
    st.line_chart(df.set_index("Query"))
