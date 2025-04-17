# Zeno the Dynamic Coherence Controller

This app visualizes semantic queries as dynamic energy fields using an adaptive DGFT controller. You can toggle semantic metrics like Zeno μ (coherence), token entropy, and embedding variance to understand their impact on topology.
## 🧪 Prototype UI

This is a mock-up of the Streamlit interface for the Adaptive DGFT Zeno Controller with metric toggles and live surface visualization:

![App UI](https://github.com/your-username/your-repo-name/blob/main/A_Streamlit_app_interface_titled...png?raw=true](https://github.com/tripper333/Q-Zeno-LLM-Mapper/blob/main/Zeno%20Choherence%20Controller.png)

## Features

- OpenAI-based embeddings
- 3D field generation with μ, entropy, and variance
- Metric toggles for interactive analysis
- Query scoreboard with metric logs

## 🧭 Tool Walkthrough: Q-Zeno Topology Explorer

Introducing **Zeno the Dynamic Coherence Controller** is an experimental tool that blends advanced AI embeddings with dynamic field computation to create a new way of **visualizing and understanding user queries**. It combines:

- 🔬 **DGFT (Dynamic Gradient Field Theory)** — A physics-informed method for mapping energy and information flow in latent space.
- 🌀 **Zeno μ Control** — A novel scalar that measures the ‘stability’ or ‘focus’ of a user query.
- 🚀 **Quasar Alpha-inspired embeddings** — High-quality contextual understanding powering the topology.

---

### 🔄 Core Interaction Flow

| Step | Action | Result |
|------|--------|--------|
| 🧠 1 | Enter a natural language query | Embedding is generated via OpenAI API |
| 🔢 2 | Zeno μ, entropy, variance calculated | Representing coherence, unpredictability, and spread |
| 🌐 3 | Metrics projected to a 3D surface | Topological field reflects semantic structure |
| 📊 4 | Metrics logged | Scoreboard tracks all historical queries |
| 📡 5 | Optional ASC loop | Simulated SQL sketch shown for concept alignment |

---

### 📈 Metrics & Interpretation

#### **Zeno μ (Mu)**
- **Range:** `0.0` to `1.0`
- **Interpretation:** Semantic coherence of the query.
  - 🔹 High μ = focused, deterministic meaning.
  - 🔸 Low μ = ambiguous, diffuse semantics.

#### **Token Entropy (H)**
- Measures lexical complexity and unpredictability.
- Higher values = rich structure or noisy phrasing.

#### **Variance**
- Spread of embedding dimensions.
- Helps detect under- or over-specified inputs.

#### **Cosine Similarity**
- Compares the current embedding to the last.
- Useful for detecting query drift or repetition.

#### **FFT Signature**
- Frequency domain of the latent vector.
- Reveals structural rhythm, periodicity, or entropy clustering.

---

### 🧪 Sample Exploratory Use Cases

| Use Case | Description |
|----------|-------------|
| 📡 `“T-Mobile towers in NYC with >2 outages”` | High μ, medium H, FFT shows clear semantic focus. |
| 🧾 `“Accounts flagged for overbilling in same cycle”` | Generates SQL-like sketch preview in ASC tab. |
| 🔄 Compare similar vs. novel questions | See how field shifts and μ adjusts with each run. |

---

### 🔁 ASC Loop Preview (Text-to-SQL)

When enabled, the app shows an **Active Semantic Compilation (ASC)** sketch — a basic simulated SQL command based on your query:

```sql
-- Example Output
SELECT * FROM service_logs WHERE reason = 'outage' AND region = 'NYC'
