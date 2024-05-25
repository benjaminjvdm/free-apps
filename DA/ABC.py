import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, norm
import matplotlib.pyplot as plt
from statsmodels.stats.power import GofChisquarePower
from statsmodels.stats.proportion import proportion_effectsize

st.title("A/B Test Calculator by Moon Benjee (문벤지)")

# Create tabs
tab1, tab2 = st.tabs(["Main Results", "Additional Metrics"])

with tab1:  # Main Results Tab
    data_type = st.radio("Select input type:", ("Raw Data", "Conversion Rates"))

    if data_type == "Raw Data":
        visitors_a = st.number_input("Visitors (Group A)", value=1000, step=10)
        conversions_a = st.number_input("Conversions (Group A)", value=50, step=1)
        visitors_b = st.number_input("Visitors (Group B)", value=1200, step=10)
        conversions_b = st.number_input("Conversions (Group B)", value=65, step=1)

        if visitors_a == 0 or visitors_b == 0:
            st.error("Error: Visitors cannot be zero.")
        else:
            rate_a = conversions_a / visitors_a
            rate_b = conversions_b / visitors_b
    else:
        rate_a = st.number_input("Conversion Rate (Group A)", value=0.05, step=0.001, format="%.3f")
        rate_b = st.number_input("Conversion Rate (Group B)", value=0.055, step=0.001, format="%.3f")
        visitors_a = 1000
        visitors_b = 1200
        conversions_a = rate_a * visitors_a
        conversions_b = rate_b * visitors_b

    # Contingency table
    table = [[conversions_a, visitors_a - conversions_a],
             [conversions_b, visitors_b - conversions_b]]

    # Chi-squared test (with zero conversion handling)
    if conversions_a == 0 or conversions_b == 0:
        st.warning("Cannot calculate p-value or significance with zero conversions in either group. Please input data with at least one conversion in each group.")
    else:
        chi2, p, _, _ = chi2_contingency(table)
        alpha = 0.05
        st.markdown("**Results**")
        st.write(f"Conversion Rate A: {rate_a:.1%}")
        st.write(f"Conversion Rate B: {rate_b:.1%}")
        st.write(f"P-value: {p:.4f}")

        if p < alpha:
            st.success("There is a statistically significant difference between the groups.")
        else:
            st.info("There is NOT a statistically significant difference between the groups.")

with tab2:  # Additional Metrics Tab
    # Effect size (Lift)
    st.markdown("**Effect Size (Lift)**")
    lift = (rate_b - rate_a) / rate_a
    st.write(f"Lift (Relative Improvement): {lift:.1%}")

    # Confidence intervals (approximation)
    st.markdown("**Confidence Intervals (95%)**")
    z_score = norm.ppf(1 - alpha / 2)
    se_a = ((rate_a * (1 - rate_a)) / visitors_a) ** 0.5
    se_b = ((rate_b * (1 - rate_b)) / visitors_b) ** 0.5
    ci_a = [rate_a - z_score * se_a, rate_a + z_score * se_a]
    ci_b = [rate_b - z_score * se_b, rate_b + z_score * se_b]

    st.write(f"Group A: [{ci_a[0]:.1%}, {ci_a[1]:.1%}]")
    st.write(f"Group B: [{ci_b[0]:.1%}, {ci_b[1]:.1%}]")

    # Visualization
    st.markdown("**Visualization**")
    fig, ax = plt.subplots()
    ax.bar(["Group A", "Group B"], [rate_a, rate_b], yerr=[se_a, se_b], capsize=10)
    ax.set_ylabel("Conversion Rate")
    st.pyplot(fig)
