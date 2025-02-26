import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to fit TotalEnergy with -5855.135 + alpha * T * ln(T)
def fit_function(T, alpha):
    return -5855.135 + alpha * T * np.log(T)

# Streamlit UI setup
st.title("Fit Total Energy for BCT Sn")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if required columns are present
        required_columns = ["Temperature(K)", "TotalEnergy"]
        if not all(column in df.columns for column in required_columns):
            st.error(f"CSV file must contain the following columns: {required_columns}")
        else:
            # Extract data
            T_data = df["Temperature(K)"].values
            E_data = df["TotalEnergy"].values
            
            # Fit the function
            try:
                popt, _ = curve_fit(fit_function, T_data, E_data)
                alpha_fit = popt[0]
                
                # Generate fitted values
                E_fit = fit_function(T_data, alpha_fit)
                
                # Display results
                st.success(f"Fitted Alpha Value: {alpha_fit:.6f}")
                
                # Plot the data and fit
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.scatter(T_data, E_data, color='red', label='Original Data', s=50, alpha=0.7)
                ax.plot(T_data, E_fit, color='blue', linestyle='--', label=f'Fitted Curve (α = {alpha_fit:.6f})')
                ax.set_xlabel("Temperature (K)", fontsize=12)
                ax.set_ylabel("Total Energy", fontsize=12)
                ax.set_title("Total Energy of BCT Sn - Data & Fit", fontsize=14)
                ax.legend(fontsize=12)
                ax.grid(True, linestyle='--', alpha=0.7)
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error during curve fitting: {e}")
                
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
