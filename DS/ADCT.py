import streamlit as st
import pandas as pd
import numpy as np

st.title("Automated Data Cleaning Tool")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Original Data")
    st.write(df)

    # Data cleaning options
    st.subheader("Data Cleaning Options")
    cleaning_options = st.multiselect(
        "Select cleaning operations:",
        ["Drop NaN Values", "Fill NaN Values", "Remove Outliers", "Convert Data Types"]
    )

    if "Drop NaN Values" in cleaning_options:
        df.dropna(inplace=True)

    if "Fill NaN Values" in cleaning_options:
        fill_method = st.selectbox("Fill method:", ["Mean", "Median", "Zero"])
        if fill_method == "Mean":
            df.fillna(df.mean(), inplace=True)
        elif fill_method == "Median":
            df.fillna(df.median(), inplace=True)
        else:
            df.fillna(0, inplace=True)

    if "Remove Outliers" in cleaning_options:
        z_scores = np.abs((df - df.mean()) / df.std())
        df = df[(z_scores < 3).all(axis=1)]  # Remove outliers beyond 3 standard deviations

    if "Convert Data Types" in cleaning_options:
        # Example type conversion (you can add more options)
        for col in df.select_dtypes(include=['object']).columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass  # Handle non-numeric columns

    # Display cleaned data
    st.subheader("Cleaned Data")
    st.write(df)
