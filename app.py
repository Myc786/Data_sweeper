# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# setup app
st.set_page_config(page_title="Data Sweeper", page_icon="🧊", layout="wide")
st.title("Data Sweeper")
st.write("This app allows you to clean your data and convert file formats easily.")

uploaded_files = st.file_uploader("Upload your data", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
        
        # Read file
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024} KB")
        st.write("### Preview of the Data")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {uploaded_file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values have been filled!")

            # Choose specific columns
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Visualization
            st.subheader("Data Visualizations")
            if st.checkbox(f"Show visualizations for {uploaded_file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # File Conversion
            st.subheader("File Conversion")
            conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ['csv', 'xlsx'], key=uploaded_file.name)

            if st.button(f"Convert {uploaded_file.name}"):
                buffer = BytesIO()

                if conversion_type == "csv":
                    df.to_csv(buffer, index=False)
                    converted_filename = uploaded_file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                
                elif conversion_type == "xlsx":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    converted_filename = uploaded_file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)  # Reset buffer position

                # Download Button
                st.download_button(
                    label=f"Download {converted_filename}",
                    data=buffer,
                    file_name=converted_filename,
                    mime=mime_type
                )
