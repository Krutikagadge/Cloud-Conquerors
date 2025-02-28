import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config as the first command
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")

# Custom CSS to make the 'Tweet' column wider
st.markdown(
    """
    <style>
        .dataframe tbody tr th {
            width: 100px !important;
        }
        .dataframe tbody tr td {
            max-width: 800px !important;  /* Adjust width */
            white-space: wrap !important; /* Enable text wrapping */
        }
        [data-testid="stDataFrame"] {
            width: 100% !important;  /* Expand table to full width */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# File path
file_path = r"D:\Projects\tp\srever\processed_twitter_data.csv"

# Load and preprocess data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        df = df.rename(columns={"tweet": "Tweet", "new_sentiment": "Sentiment"})  # Standardize column names
        df = df[["Tweet", "Sentiment"]]  # Keep only relevant columns
        df = df.dropna()
        return df
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}. Ensure it's in the correct location.")
        return pd.DataFrame(columns=["Tweet", "Sentiment"])
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        return pd.DataFrame(columns=["Tweet", "Sentiment"])

df = load_data()

# Limit dataset for better performance
max_rows_to_display = 1000  # Limit table display
max_chart_rows = 10000  # Limit chart processing

# Main UI Layout
st.markdown("<h1 style='text-align: center;'>📊 Twitter Sentiment Analysis</h1>", unsafe_allow_html=True)

# Navigation Bar
tabs = ["Home", "Sentiment Dashboard"]
selected_tab = st.radio("", tabs, horizontal=True)

# 🔍 **Home Page (Search Tweets)**
if selected_tab == "Home":
    st.subheader("🔍 Search Tweets")
    
    # Make search bar full-width for better alignment
    query = st.text_input("Enter a keyword to filter tweets:", key="search", help="Search for tweets containing this word")

    # Filter tweets based on search query
    if query:
        filtered_df = df[df["Tweet"].str.contains(query, case=False, na=False)]
        st.write(f"### Showing results for: **{query}** ({len(filtered_df)} tweets found)")
    else:
        filtered_df = df
        st.write("### Showing all tweets")

    # **Display tweets in a horizontally expanded table**
    st.dataframe(filtered_df.head(max_rows_to_display), height=400, use_container_width=True)

# 📊 **Sentiment Dashboard**
elif selected_tab == "Sentiment Dashboard":
    st.subheader("📊 Sentiment Analysis Dashboard")

    # Filtered data based on search query
    query = st.text_input("Enter a keyword to analyze sentiment:", key="dashboard_search")
    if query:
        filtered_df = df[df["Tweet"].str.contains(query, case=False, na=False)]
    else:
        filtered_df = df

    # Limit data for visualization performance
    filtered_df = filtered_df.tail(max_chart_rows)

    sentiment_counts = filtered_df["Sentiment"].value_counts()
    
    # Pie Chart
    fig_pie = px.pie(
        values=sentiment_counts.values, 
        names=sentiment_counts.index, 
        title="Sentiment Distribution",
        color=sentiment_counts.index,
        color_discrete_map={"positive": "green", "negative": "red", "neutral": "blue"}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar Chart
    fig_bar = px.bar(
        x=sentiment_counts.index, 
        y=sentiment_counts.values, 
        title="Sentiment Counts",
        labels={"x": "Sentiment", "y": "Count"},
        color=sentiment_counts.index,
        color_discrete_map={"positive": "green", "negative": "red", "neutral": "blue"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
