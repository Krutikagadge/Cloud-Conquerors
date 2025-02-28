import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configure Page ---
st.set_page_config(page_title="Twitter Sentiment Analyzer", layout="wide")

# --- Custom Styling for Light/Dark Mode ---
def set_theme(theme):
    if theme == "Dark Mode":
        st.markdown(
            """
            <style>
            body { background-color: #181818; color: white; }
            .stTextInput, .stSlider, .stButton, .stDataFrame { background-color: #252525; color: white; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body { background-color: white; color: black; }
            </style>
            """,
            unsafe_allow_html=True
        )

# --- Navigation Bar ---
tabs = ["🔍 Tweet Search", "📊 Dashboard", "⚙️ Settings"]
selected_tab = st.radio("", tabs, horizontal=True)

# --- Settings (Dark/Light Mode) ---
if selected_tab == "⚙️ Settings":
    st.title("⚙️ Settings")
    theme = st.radio("Select Theme:", ["Light Mode", "Dark Mode"], key="theme")
    set_theme(theme)  # Apply theme dynamically
    st.success("Changes will apply instantly across the app.")

# --- Function to Fetch Placeholder Tweets ---
def fetch_tweets(query, max_tweets=100):
    sentiments = ["Positive", "Negative", "Neutral"]
    data = {
        "Date": pd.date_range(start="2024-02-01", periods=max_tweets, freq="D"),
        "Tweet": [f"Sample tweet {i+1} about {query}" for i in range(max_tweets)],
        "Sentiment": [sentiments[i % 3] for i in range(max_tweets)]
    }
    return pd.DataFrame(data)

# --- 1️⃣ Tweet Search ---
if selected_tab == "🔍 Tweet Search":
    st.title("🔍 Twitter Sentiment Analyzer")
    st.markdown("**Search for tweets and analyze their sentiment.**")

    query = st.text_input("Enter a keyword to search tweets:")
    max_tweets = st.slider("Select number of tweets:", 10, 500, 100)

    if st.button("🔄 Fetch Tweets"):
        df = fetch_tweets(query, max_tweets)
        if not df.empty:
            st.success(f"Showing {len(df)} tweets for **{query}**")
            sentiment_filter = st.multiselect("Filter by Sentiment:", ["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"])
            filtered_df = df[df["Sentiment"].isin(sentiment_filter)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning("No tweets found! Try a different keyword.")

# --- 2️⃣ Sentiment Dashboard ---
if selected_tab == "📊 Dashboard":
    st.title("📊 Sentiment Analysis Dashboard")
    df = fetch_tweets("sample", 100)

    selected_sentiments = st.multiselect("Filter Sentiments:", ["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"])
    df = df[df["Sentiment"].isin(selected_sentiments)]

    sentiment_count = df["Sentiment"].value_counts().reset_index()
    sentiment_count.columns = ["Sentiment", "Count"]

    fig_pie = px.pie(sentiment_count, names="Sentiment", values="Count", title="Sentiment Distribution", hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

    df["Date"] = pd.to_datetime(df["Date"])
    sentiment_trend = df.groupby(["Date", "Sentiment"]).size().reset_index(name="Count")

    fig_trend = px.line(sentiment_trend, x="Date", y="Count", color="Sentiment", title="Sentiment Trend Over Time", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

    fig_bar = px.bar(sentiment_count, x="Sentiment", y="Count", title="Sentiment Breakdown", color="Sentiment")
    st.plotly_chart(fig_bar, use_container_width=True)
