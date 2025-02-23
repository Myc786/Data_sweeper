import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup App UI
st.set_page_config(page_title="Data Sweeper", page_icon="🧼", layout="wide")
st.markdown(
    """
    <style>
    .main-title { text-align: center; font-size: 36px; font-weight: bold; color: #4A90E2; }
    .stButton > button { width: 100%; border-radius: 8px; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    .uploaded-file { font-weight: bold; color: #2E7D32; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-title'>🧼 Data Sweeper</div>", unsafe_allow_html=True)
st.write("**Clean, Transform, and Convert Your Data Easily**")

# File Upload
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
            st.error(f"❌ Unsupported file format: {file_ext}")
            continue

        # Display file info
        with st.expander(f"📂 {uploaded_file.name}"):
            st.markdown(f"<div class='uploaded-file'>File Size: {uploaded_file.size / 1024:.2f} KB</div>", unsafe_allow_html=True)
            st.write("### 🔍 Preview of the Data")
            st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🛠 Data Cleaning Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates", key=f"dup_{uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")
            
            with col2:
                if st.button(f"🧪 Fill Missing Values", key=f"fill_{uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled!")
            
            # Choose specific columns
            selected_columns = st.multiselect(f"🎯 Select Columns to Keep", df.columns, default=df.columns, key=f"cols_{uploaded_file.name}")
            df = df[selected_columns]
            
            # Visualization
            st.subheader("📊 Data Visualizations")
            if st.checkbox(f"📉 Show Graphs", key=f"graph_{uploaded_file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            
            # File Conversion
            st.subheader("🔄 File Conversion")
            conversion_type = st.radio(f"Convert to:", ['CSV', 'Excel'], key=f"convert_{uploaded_file.name}")
            
            if st.button(f"💾 Convert & Download", key=f"download_{uploaded_file.name}"):
                buffer = BytesIO()
                
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    converted_filename = uploaded_file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    converted_filename = uploaded_file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                buffer.seek(0)
                st.download_button(
                    label=f"⬇️ Download {converted_filename}",
                    data=buffer,
                    file_name=converted_filename,
                    mime=mime_type
                )
