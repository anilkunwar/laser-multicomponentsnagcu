import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Define Gibbs free energy terms
def gibbs_terms(T):
    term1 = -5855.135  # Constant term
    term2 = 65.443315 * T  # Linear term
    term3 = -15.961 * T * np.log(T)  # T*ln(T) term
    term4 = -0.0188702 * T**2  # Quadratic term
    term5 = 3.121167e-6 * T**3  # Cubic term
    term6 = -61960 / T  # Inverse temperature term
    total = term1 + term2 + term3 + term4 + term5 + term6  # Sum of all terms
    return term1, term2, term3, term4, term5, term6, total

# Streamlit UI setup
st.title("Gibbs Free Energy Terms for BCT Sn")

# Temperature range sliders
T_start = st.slider("Start Temperature (K)", 250, 500, 298, 5)
T_end = st.slider("End Temperature (K)", 300, 600, 495, 5)
T_step = st.slider("Temperature Step (K)", 5, 50, 30, 5)

# Generate temperature range
temperatures = np.arange(T_start, T_end + 1, T_step)

data = {"Temperature(K)": temperatures}
terms = ["Term 1: Constant", "Term 2: Linear", "Term 3: T*ln(T)", 
         "Term 4: Quadratic", "Term 5: Cubic", "Term 6: Inverse T", "Total Energy"]

# Compute Gibbs energy terms
gibbs_data = {term: [] for term in terms}
for T in temperatures:
    values = gibbs_terms(T)
    for term, value in zip(terms, values):
        gibbs_data[term].append(value)

data.update(gibbs_data)
df = pd.DataFrame(data)

# Download CSV button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "gibbs_terms_sn_BCT.csv", "text/csv")

# Select visualization type
plot_type = st.radio("Choose Plot Type", ["Matplotlib", "Plotly"])

if plot_type == "Matplotlib":
    fig, ax = plt.subplots(figsize=(10, 6))
    for term in terms:
        ax.plot(df["Temperature(K)"], df[term], marker='o', label=term)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Term Value")
    ax.set_title("Gibbs Free Energy Terms")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

elif plot_type == "Plotly":
    df_melted = df.melt(id_vars=["Temperature(K)"], var_name="Term", value_name="Value")
    fig = px.line(df_melted, x="Temperature (K)", y="Value", color="Term", markers=True,
                  title="Gibbs Free Energy Terms")
    fig.update_layout(xaxis_title="Temperature (K)", yaxis_title="Term Value")
    st.plotly_chart(fig)

