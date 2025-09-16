import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pdfplumber
import io
from collections import Counter
import pandas as pd

# --- Text Extraction with pdfplumber ---
def extract_text_from_pdf(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return " ".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        st.error(f"PDF error: {e}")
        return ""

# --- Word Frequency Analysis ---
def get_word_frequencies(text, extra_stopwords):
    all_stopwords = STOPWORDS.union(set(extra_stopwords.split()))
    words = [word.lower() for word in text.split() if word.lower() not in all_stopwords]
    return Counter(words)

# --- Word Cloud Generator ---
def show_word_cloud(freq, width, height, bg_color):
    wc = WordCloud(
        width=width,
        height=height,
        background_color=bg_color,
        stopwords=STOPWORDS,
        collocations=False
    ).generate_from_frequencies(freq)

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# --- Bar Chart ---
def show_bar_chart(freq):
    df = pd.DataFrame(freq.most_common(10), columns=["Word", "Frequency"])
    st.subheader("📊 Top Words - Bar Chart")
    st.bar_chart(df.set_index("Word"))

# --- Pie Chart ---
def show_pie_chart(freq):
    df = pd.DataFrame(freq.most_common(10), columns=["Word", "Frequency"])
    fig, ax = plt.subplots()
    ax.pie(df["Frequency"], labels=df["Word"], autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.subheader("🥧 Top Words - Pie Chart")
    st.pyplot(fig)

# --- Main App ---
def main():
    st.set_page_config(page_title="Word Cloud & Charts", layout="wide")
    st.title("☁ Word Cloud + Charts from PDF")

    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        raw_text = extract_text_from_pdf(file_bytes)

        if raw_text.strip():
            st.subheader("🔧 Settings")
            max_words = st.slider("Max words", 50, 500, 150)
            bg_color = st.selectbox("Background color", ["white", "black", "lightblue", "lightgrey"])
            width = st.slider("Width", 300, 1000, 800)
            height = st.slider("Height", 300, 800, 400)
            extra_stopwords = st.text_input("Add custom stopwords (space-separated):", "")

            freq = get_word_frequencies(raw_text, extra_stopwords)

            st.subheader("☁ Word Cloud")
            show_word_cloud(freq, width, height, bg_color)

            show_bar_chart(freq)
            show_pie_chart(freq)
        else:
            st.warning("No text found in the PDF.")
    else:
        st.info("Please upload a PDF file to begin.")

# ✅ Entry Point
if __name__ == "__main__":
    main()
