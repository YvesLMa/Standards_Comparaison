import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Initial data points for x and y
x = np.array([0, 0.25, 0.5, 0.75, 1, 2, 3, 4])
y = np.array([0.04, 0.446, 0.843, 1.251, 1.666, 3.206, 4.908, 6.614])

# Title
st.title("Quadratic Fit of y and y2 Data")

# Prompt user to input y2 values
st.subheader("Enter y2 values:")
y2 = []
for i, value in enumerate(x):
    y2_value = st.number_input(f"y2 value for x = {value}:", value=0.0, step=0.01)
    y2.append(y2_value)
y2 = np.array(y2)

if len(y2) == len(x):
    # Perform quadratic fit for y
    coeffs_y = np.polyfit(x, y, 2)
    a, b, c = coeffs_y
    y_fit = np.polyval(coeffs_y, x)
    r2_y = r2_score(y, y_fit)

    # Perform quadratic fit for y2
    coeffs_y2 = np.polyfit(x, y2, 2)
    a2, b2, c2 = coeffs_y2
    y2_fit = np.polyval(coeffs_y2, x)
    r2_y2 = r2_score(y2, y2_fit)

    # Apply y equation to y2 data
    y2_pred_from_y = np.polyval(coeffs_y, x)
    r2_y_on_y2 = r2_score(y2, y2_pred_from_y)

    # Generate smooth x values for plotting the fit curve
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit_smooth = np.polyval(coeffs_y, x_fit)
    y2_fit_smooth = np.polyval(coeffs_y2, x_fit)

    # Plot data and fit using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, color='red', label='Data y')
    ax.plot(x_fit, y_fit_smooth, color='red', label=f'Fit y: y = {a:.4f}x² + {b:.4f}x + {c:.4f}, R² = {r2_y:.4f}')
    
    ax.scatter(x, y2, color='blue', label='Data y2')
    ax.plot(x_fit, y2_fit_smooth, color='blue', label=f'Fit y2: y = {a2:.4f}x² + {b2:.4f}x + {c2:.4f}, R² = {r2_y2:.4f}')
    
    # Predicted y2 using y equation
    ax.plot(x, y2_pred_from_y, 'o--', color='purple', label=f'Prediction y2 from y equation, R² = {r2_y_on_y2:.4f}')

    ax.set_xlabel('Concentration (mM)')
    ax.set_ylabel('Absorbance (492 nm)')
    ax.set_title('Quadratic Fit of y and y2 Data')
    ax.legend()
    ax.grid(True)

    # Display plot in Streamlit
    st.pyplot(fig)

    # Output equations and R² values
    st.write(f"**Equation for y:** y = {a:.4f}x² + {b:.4f}x + {c:.4f}, R² = {r2_y:.4f}")
    st.write(f"**Equation for y2:** y = {a2:.4f}x² + {b2:.4f}x + {c2:.4f}, R² = {r2_y2:.4f}")
    st.write(f"**R² of y equation applied to y2:** {r2_y_on_y2:.4f}")

else:
    st.error("Please enter valid y2 values for all x points.")

