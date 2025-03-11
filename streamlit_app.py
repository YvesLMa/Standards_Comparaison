import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from io import BytesIO

# Initial data points for x and original standards
x = np.array([0, 0.25, 0.5, 0.75, 1, 2, 3, 4])
original_standards = np.array([0.04, 0.446, 0.843, 1.251, 1.666, 3.206, 4.908, 6.614])

# Title
st.title("Quadratic Fit of Original and Your Standards")

# Prompt user to input 'your standards' values
st.subheader("Enter 'Your Standards' Values:")
your_standards = []
your_standards = []
for i, value in enumerate(x):
    y2_value = st.number_input(f"Value for x = {value}:", value=0.0, step=0.01)
    your_standards.append(y2_value)
your_standards = np.array(your_standards)  # ✅ Fix: Convert list to array correctly

if len(your_standards) == len(x):
    # Perform quadratic fit for original standards
    coeffs_orig = np.polyfit(x, original_standards, 2)
    a_orig, b_orig, c_orig = coeffs_orig
    original_fit = np.polyval(coeffs_orig, x)
    r2_orig = r2_score(original_standards, original_fit)

    # Perform quadratic fit for your standards
    coeffs_your = np.polyfit(x, your_standards, 2)
    a_your, b_your, c_your = coeffs_your
    your_fit = np.polyval(coeffs_your, x)
    r2_your = r2_score(your_standards, your_fit)

    # Apply original equation to your standards data
    your_pred_from_orig = np.polyval(coeffs_orig, x)
    r2_orig_on_your = r2_score(your_standards, your_pred_from_orig)

    # Generate smooth x values for plotting the fit curve
    x_fit = np.linspace(min(x), max(x), 100)
    original_fit_smooth = np.polyval(coeffs_orig, x_fit)
    your_fit_smooth = np.polyval(coeffs_your, x_fit)

    # Plot data and fit using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, original_standards, color='red', label='Original Standards')
    ax.plot(x_fit, original_fit_smooth, color='red', label=f'Fit (Original): y = {a_orig:.4f}x² + {b_orig:.4f}x + {c_orig:.4f}, R² = {r2_orig:.4f}')
    
    ax.scatter(x, your_standards, color='blue', label='Your Standards')
    ax.plot(x_fit, your_fit_smooth, color='blue', label=f'Fit (Your): y = {a_your:.4f}x² + {b_your:.4f}x + {c_your:.4f}, R² = {r2_your:.4f}')
    
    # Prediction of "your standards" using "original standards" equation
    ax.plot(x, your_pred_from_orig, 'o--', color='purple', label=f'Prediction from Original Fit, R² = {r2_orig_on_your:.4f}')

    ax.set_xlabel('Concentration (mM)')
    ax.set_ylabel('Absorbance (492 nm)')
    ax.set_title('Quadratic Fit of Original and Your Standards')
    ax.legend()
    ax.grid(True)

    # Display plot in Streamlit
    st.pyplot(fig)

    # Output equations and R² values
    st.write(f"**Equation for Original Standards:** y = {a_orig:.4f}x² + {b_orig:.4f}x + {c_orig:.4f}, R² = {r2_orig:.4f}")
    st.write(f"**Equation for Your Standards:** y = {a_your:.4f}x² + {b_your:.4f}x + {c_your:.4f}, R² = {r2_your:.4f}")
    st.write(f"**R² of Original Equation Applied to Your Standards:** {r2_orig_on_your:.4f}")

    # Create a button to download the plot as PNG
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    st.download_button(
        label="Download Plot as PNG",
        data=buffer,
        file_name="quadratic_fit.png",
        mime="image/png"
    )

else:
    st.error("Please enter valid values for all x points.")

