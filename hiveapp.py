import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set up the Streamlit app title with logo
col1, col2 = st.columns([1, 8])  # Adjust the ratio as needed

# Function to safely load images
def load_image(image_path):
    if os.path.exists(image_path):
        return image_path
    else:
        st.warning(f"Image not found: {image_path}")
        return None

with col1:
    logo_path = load_image("images/logo.jpg")
    if logo_path:
        st.image(logo_path, width=100)  # Adjust the image path and width

with col2:
    st.title("Insight Hive - Self-Service Analytics for SMEs")

st.markdown("""
Welcome to the Insight Hive prototype! This app showcases the basic features of our data science tool designed for business owners and SMEs.
With Insight Hive, you can easily upload your data, visualize it, and gain insights without needing any coding skills.
""")

# Image paths and captions
image_paths = [
    "Capture Step 1 CSV.PNG",
    "Capture Step 2.PNG",
    "Capture Step 3.PNG",
    "Capture Step 4.PNG",
    "Capture Step 5.PNG"
]

captions = [
    "Step 1: Upload CSV",
    "Step 2: View Statistics",
    "Step 3: Data Visualization",
    "Step 4: Descriptive Analysis",
    "Step 5: Provide Insights"
]

# Load images safely
images = [load_image(path) for path in image_paths]

# Create a slideshow
selected_index = st.selectbox("Select a step to view:", range(len(images)), format_func=lambda x: captions[x])
if images[selected_index]:
    st.image(images[selected_index], caption=captions[selected_index], use_column_width=True)

# Function to upload a CSV file
def upload_file():
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("**Uploaded Data:**")
            st.dataframe(df)
            return df
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            return None
    else:
        st.warning("Please upload a CSV file to proceed.")
        return None

# Function to display basic data statistics
def show_statistics(df):
    st.write("**Basic Statistics:**")
    try:
        st.write(df.describe())
    except Exception as e:
        st.error(f"Error displaying statistics: {e}")

# Function to visualize the data
def visualize_data(df):
    st.write("**Data Visualization:**")
    
    # Select columns for x and y axis
    columns = df.columns.tolist()
    x_axis = st.selectbox("Select X-axis column", columns)
    y_axis = st.selectbox("Select Y-axis column", columns)
    
    # Create a simple line plot
    try:
        fig, ax = plt.subplots()
        ax.plot(df[x_axis], df[y_axis], marker='o')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")
        
        st.pyplot(fig)
        
        return x_axis, y_axis
    except Exception as e:
        st.error(f"Error visualizing data: {e}")
        return None, None

# Function to provide descriptive analysis of the graph
def descriptive_analysis(df, x_axis, y_axis):
    st.write("**Descriptive Analysis:**")
    
    if x_axis is None or y_axis is None:
        st.warning("Cannot perform descriptive analysis without valid axes.")
        return
    
    try:
        # Calculate and display correlation
        correlation = df[x_axis].corr(df[y_axis])
        st.write(f"The correlation between {x_axis} and {y_axis} is: {correlation:.2f}")
        
        # Calculate and display regression line (optional)
        st.write("**Regression Analysis:**")
        slope, intercept = np.polyfit(df[x_axis], df[y_axis], 1)
        st.write(f"Regression line equation: y = {slope:.2f}x + {intercept:.2f}")
    except Exception as e:
        st.error(f"Error in descriptive analysis: {e}")

# Function to provide insights from the data
def provide_insights(df, x_axis, y_axis):
    st.write("**Insights:**")
    
    if x_axis is None or y_axis is None:
        st.warning("Cannot provide insights without valid axes.")
        return
    
    try:
        # Display some example insights (you can customize this part)
        st.write(f"1. The correlation between {x_axis} and {y_axis} indicates the strength of the relationship between these two variables.")
        st.write(f"2. The regression line shows the trend of {y_axis} based on {x_axis}, which can be useful for predictions.")
        st.write(f"3. Any significant outliers or patterns observed in the visualization could indicate underlying issues or opportunities.")
    except Exception as e:
        st.error(f"Error providing insights: {e}")

# Main function to control the app flow
def main():
    # Displaying images at the start (already done above)
    # Displaying the steps
    st.header("Step 1: Upload Your Data")
    df = upload_file()
    
    if df is not None:
        # Step 2: Show statistics
        st.header("Step 2: View Data Statistics")
        show_statistics(df)
        
        # Step 3: Visualize the data
        st.header("Step 3: Visualize Your Data")
        x_axis, y_axis = visualize_data(df)
        
        # Step 4: Descriptive analysis for the graph
        st.header("Step 4: Descriptive Analysis for the Graph")
        descriptive_analysis(df, x_axis, y_axis)
        
        # Step 5: Provide insights
        st.header("Step 5: Provide Insights")
        provide_insights(df, x_axis, y_axis)

if __name__ == "__main__":
    main()
