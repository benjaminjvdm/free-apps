import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("SWOT Analysis Radar Chart")

st.header("Enter SWOT Factors and Importance")

with st.form("swot_form"):
    st.write("Importance levels: Highest (3), High (2), Normal (1)")

    # Strengths
    strengths = st.text_area("Strengths (comma-separated):", value="Strong brand, Loyal customer base, Efficient production")
    strengths_list = [s.strip() for s in strengths.split(",") if s.strip()]
    strengths_importance = {}
    for s in strengths_list:
        strengths_importance[s] = st.slider(f"Importance of '{s}':", min_value=1, max_value=3, value=2)

    # Weaknesses
    weaknesses = st.text_area("Weaknesses (comma-separated):", value="High production costs, Limited distribution network, Lack of innovation")
    weaknesses_list = [w.strip() for w in weaknesses.split(",") if w.strip()]
    weaknesses_importance = {}
    for w in weaknesses_list:
        weaknesses_importance[w] = st.slider(f"Importance of '{w}':", min_value=1, max_value=3, value=2)

    # Opportunities
    opportunities = st.text_area("Opportunities (comma-separated):", value="Growing market, New technology, Emerging trends")
    opportunities_list = [o.strip() for o in opportunities.split(",") if o.strip()]
    opportunities_importance = {}
    for o in opportunities_list:
        opportunities_importance[o] = st.slider(f"Importance of '{o}':", min_value=1, max_value=3, value=2)

    # Threats
    threats = st.text_area("Threats (comma-separated):", value="Increased competition, Economic downturn, Regulatory changes")
    threats_list = [t.strip() for t in threats.split(",") if t.strip()]
    threats_importance = {}
    for t in threats_list:
        threats_importance[t] = st.slider(f"Importance of '{t}':", min_value=1, max_value=3, value=2)

    submitted = st.form_submit_button("Generate Radar Chart")


if submitted:
    # Data preparation
    categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
    category_values = {
        'Strengths': list(strengths_importance.values()),
        'Weaknesses': list(weaknesses_importance.values()),
        'Opportunities': list(opportunities_importance.values()),
        'Threats': list(threats_importance.values())
    }

    # Calculate average importance for each category
    avg_values = [np.mean(v) if v else 0 for v in category_values.values()]

    # Plot radar chart (with improvements and no radial gridlines)
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    avg_values += avg_values[:1]  # Close the loop
    angles += angles[:1]

    fig = plt.figure(figsize=(10, 10))  
    ax = fig.add_subplot(111, polar=True)
    ax.set_rgrids([]) # Remove radial gridlines
    
    #Plot the lines and fill
    ax.plot(angles, avg_values, 'o-', linewidth=2, color='blue')  
    ax.fill(angles, avg_values, alpha=0.25, color='lightblue') 
    
    ax.grid(alpha=0.2)  # Keep the circular gridlines for reference
    plt.yticks([1, 2, 3], ["Normal", "High", "Highest"], color="grey", size=7)  
    plt.ylim(0, 3.5) 
    plt.title("SWOT Analysis", size=14)

    #Set the labels 
    labels = [f"{category}\n({avg:.1f})" for category, avg in zip(categories, avg_values)]
    ax.set_thetagrids(angles[:-1], labels)  # Set labels with averages

    # Display the chart
    st.pyplot(fig)
