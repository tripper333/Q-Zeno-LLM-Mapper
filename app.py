import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from openai import OpenAI
from utils import get_embedding, compute_mu, compute_variance, compute_token_entropy, generate_field

# --- Page Configuration ---
st.set_page_config(
    page_title="Zenome: Expectation-to-Outcome Mapper",
    layout="wide",
    page_icon="🧠"
)

# --- Style ---
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
</style>
""", unsafe_allow_html=True)

# --- OpenAI Client Setup ---
client = OpenAI()

# --- Memory Logs ---
query_log = []
mu_log, entropy_log, var_log = [], [], []

# --- Sidebar Inputs ---
with st.sidebar:
    st.title("🧭 Query Navigation")
    query_input = st.text_input("🔍 Enter your natural language query")
    zeno_slider = st.slider(
        "📉 Query Ambiguity (μ influence)", 0.0, 1.0, 0.5, 0.01,
        help="Controls how 'uncertain' or ambiguous the query is. Higher = more noise."
    )
    show_entropy = st.checkbox("Overlay Entropy Channel", value=True)
    show_var = st.checkbox("Overlay Variance Channel", value=True)

    st.markdown("""
    ### 🧠 Metric Guide  
    - **μ (Zeno)**: Alignment between expectation & outcome  
    - **Entropy**: Complexity or uncertainty in phrasing  
    - **Variance**: Spread in latent space  
    - *(Cosine Drift & FFT coming soon)*
    """)
    st.info("Each query generates a 3D coherence surface showing semantic topology.")

# --- Main App Execution ---
st.title("🧠 Zenome: Expectation-to-Outcome Mapper")
st.markdown("### Bridging expectation and outcome through coherence-driven topology")

if st.button("▶️ Run Query") and query_input:
    embedding = get_embedding(query_input)
    mu = compute_mu(embedding)
    entropy = compute_token_entropy(query_input)
    var = compute_variance(embedding)

    query_log.append(query_input)
    mu_log.append(mu)
    entropy_log.append(entropy)
    var_log.append(var)

    # Generate field surface
    X, Y, Z = generate_field(mu, entropy if show_entropy else 0.5, var if show_var else 0.1)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="k", alpha=0.9)
    ax.set_title(f"Zeno Surface Field\n{query_input}\nμ={mu:.4f}, H={entropy:.3f}, Var={var:.4f}")
    ax.set_xlabel("Latent X")
    ax.set_ylabel("Latent Y")
    ax.set_zlabel("Zeno Field")
    st.pyplot(fig)

    # GPT Commentary
    try:
        interpret = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a strategic AI analyst interpreting metrics for text queries."},
                {"role": "user", "content": f"The μ (Zeno) score is {mu:.4f}, Entropy is {entropy:.3f}, and Variance is {var:.4f} for the query: {query_input}. Please provide a short strategic insight on the coherence of this query and how it might perform in a semantic mapping system like text-to-SQL."}
            ]
        )
        gpt_analysis = interpret.choices[0].message.content
        st.markdown("### 🧠 GPT Strategic Insight")
        st.success(gpt_analysis)
    except Exception as e:
        st.warning("GPT Insight currently unavailable. Check your OpenAI API key.")

# --- Query Metrics Tracker ---
if query_log:
    st.markdown("### 📊 Query Scoreboard")
    df = pd.DataFrame({
        "Query": query_log,
        "μ": mu_log,
        "Entropy": entropy_log,
        "Variance": var_log
    })
    st.dataframe(df)
    st.line_chart(df.set_index("Query"))
