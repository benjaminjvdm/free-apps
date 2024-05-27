import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

# --- Sidebar: About the Author ---
with st.sidebar:
    st.subheader("About the Author")

    # Fetch image
    image_url = "https://avatars.githubusercontent.com/u/97449931?v=4"
    response = requests.get(image_url)

    if response.status_code == 200:
        image = response.content
        st.image(image, caption="Moon Benjee (문벤지)", use_column_width=True)  # Display image with caption
    else:
        st.write("Image not found.")

    st.markdown(
        """
        This app was created by **Moon Benjee (문벤지)**. 
        You can connect with me on: [LinkedIn](https://www.linkedin.com/in/benjaminjvdm/)
        """
    )

st.title("SWOT Analysis Radar Chart")
st.header("Enter SWOT Factors and Importance")

with st.form("swot_form"):
    st.write("Importance levels: Normal (1), High (2), Highest (3)")

    # Function to get factors and importance values
    def get_factors_and_importance(category_name):
        factors_input = st.text_input(f"{category_name} (comma-separated):")
        factors_list = [f.strip() for f in factors_input.split(",") if f.strip()]
        importance_values = []
        for i, factor in enumerate(factors_list):
            importance = st.number_input(f"Importance of '{factor}':", min_value=1, max_value=3, value=2, key=f"{category_name}_{i}") #Unique key
            importance_values.append(importance)
        return factors_list, importance_values

    # Get input for each category
    strengths_list, strengths_importance = get_factors_and_importance("Strengths")
    weaknesses_list, weaknesses_importance = get_factors_and_importance("Weaknesses")
    opportunities_list, opportunities_importance = get_factors_and_importance("Opportunities")
    threats_list, threats_importance = get_factors_and_importance("Threats")

    submitted = st.form_submit_button("Generate Radar Chart")


if submitted:
    # Data preparation
    categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
    category_values = {
        'Strengths': strengths_importance,
        'Weaknesses': weaknesses_importance,
        'Opportunities': opportunities_importance,
        'Threats': threats_importance
    }

    # Calculate average importance for each category
    avg_values = [np.mean(v) if v else 0 for v in category_values.values()]

    # Optimized Plot Settings
    label_offset = 0.2
    label_size = 10  # Explicitly define label_size here

    # Plot radar chart
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    avg_values += avg_values[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    ax.set_rgrids([])  
    ax.set_xticks([])

    ax.plot(angles, avg_values, 'o-', linewidth=2, color='blue')
    ax.fill(angles, avg_values, alpha=0.25, color='lightblue')

    ax.grid(alpha=0.2)  
    plt.ylim(0, 3.5)

    plt.title("SWOT Analysis", size=16)

    # Display category labels and average values on the points themselves
    for i, category in enumerate(categories):
        angle = angles[i]
        avg_importance = avg_values[i]
        ax.text(angle, avg_importance + 0.2, f"{category} ({avg_importance:.1f})", 
                ha='center', va='center', size=label_size, fontweight='bold')

    # Display the chart
    st.pyplot(fig)
