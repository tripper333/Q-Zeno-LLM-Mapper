# Finalizing the polished Streamlit app (`app.py`) with:
# - Enhanced metric surface deformation
# - Clean sidebar color scheme
# - Improved GPT feedback handling
# - Seaborn visual for query chart
# - Session persistence

app_py_code = """
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from openai import OpenAI
from utils import get_embedding, compute_mu, compute_variance, compute_token_entropy, generate_field

st.set_page_config(
    page_title="Zenome: Expectation-to-Outcome Mapper",
    layout="wide",
    page_icon="🧠"
)

# --- Style Overrides ---
st.markdown(\"""
<style>
    body {
        background-color: #f5f7fa;
        color: #1f2937;
    }
    .stSlider > div > div {
        background-color: #6366f1;
    }
    .stSidebar {
        background-color: #f1f5f9;
        color: #1e293b;
    }
    .css-1v3fvcr {
        color: #1e293b !important;
    }
</style>
\""", unsafe_allow_html=True)

# --- State Management ---
if "query_log" not in st.session_state:
    st.session_state.query_log = []
    st.session_state.mu_log = []
    st.session_state.entropy_log = []
    st.session_state.var_log = []

# --- Sidebar Controls ---
with st.sidebar:
    st.title("🧭 Query Navigation")
    query_input = st.text_input("🔍 Enter your natural language query")
    zeno_slider = st.slider("📉 Query Ambiguity (μ influence)", 0.0, 1.0, 0.5, 0.01)
    show_entropy = st.checkbox("Overlay Entropy Channel", value=True)
    show_var = st.checkbox("Overlay Variance Channel", value=True)

    st.markdown(\"""
    ### 🧠 Metric Guide  
    - **μ (Zeno)**: Alignment between expectation & outcome  
    - **Entropy**: Linguistic uncertainty  
    - **Variance**: Latent semantic spread  
    - *(Drift & Frequency coming soon)*

    Each query generates a topological 3D surface.
    \""")

# --- Title Block ---
st.title("🧠 Zenome: Expectation-to-Outcome Mapper")
st.markdown("### Bridging expectation and outcome through coherence-driven topology")

# --- Main Execution ---
client = OpenAI()

if st.button("▶️ Run Query") and query_input:
    embedding = get_embedding(query_input)
    mu = compute_mu(embedding)
    entropy = compute_token_entropy(query_input)
    var = compute_variance(embedding)

    st.session_state.query_log.append(query_input)
    st.session_state.mu_log.append(mu)
    st.session_state.entropy_log.append(entropy)
    st.session_state.var_log.append(var)

    # --- Field Surface ---
    X, Y = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
    R = np.sqrt(X**2 + Y**2)
    Z = 1 / (1 + np.exp(-(np.sin(3*R) + np.cos(2*X)*np.sin(2*Y)) + 6 * (mu - 0.5) + 3 * entropy + 2 * var))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="k", alpha=0.9)
    ax.set_title(f"Zeno Surface Field\\n{query_input}\\nμ={mu:.4f}, H={entropy:.3f}, Var={var:.4f}")
    ax.set_xlabel("Latent X")
    ax.set_ylabel("Latent Y")
    ax.set_zlabel("Zeno Field")
    st.pyplot(fig)

    # --- GPT Interpretation ---
    try:
        interpretation = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a strategic AI analyst interpreting coherence metrics from natural language."},
                {"role": "user", "content": f"The μ (Zeno) score is {mu:.4f}, Entropy is {entropy:.3f}, and Variance is {var:.4f} for the query: {query_input}. Offer a short insight on coherence and potential next step."}
            ]
        )
        st.markdown("### 🧠 GPT Strategic Insight")
        st.success(interpretation.choices[0].message.content)
    except Exception as e:
        st.warning("⚠️ GPT Insight unavailable. Check API key.")

# --- Scoreboard & Plot ---
if st.session_state.query_log:
    df = pd.DataFrame({
        "Query": st.session_state.query_log,
        "μ": st.session_state.mu_log,
        "Entropy": st.session_state.entropy_log,
        "Variance": st.session_state.var_log
    })

    st.markdown("### 📊 Query Scoreboard")
    st.dataframe(df)

    st.markdown("### 📈 Query Coherence Trends")
    fig2, ax = plt.subplots()
    sns.lineplot(data=df.set_index("Query"), ax=ax, palette="coolwarm")
    st.pyplot(fig2)
"""

with open("/mnt/data/app.py", "w") as f:
    f.write(app_py_code)

"/mnt/data/app.py"

