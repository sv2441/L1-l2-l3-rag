import streamlit as st
import numpy as np
import os
import time
import base64
from datetime import datetime

from sentence_transformers import SentenceTransformer, util
import pandas as pd


corpus_df = pd.read_csv("registry_data.csv")

model_path= "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model_path)

# Encode the corpus
corpus_embeddings = embedder.encode(corpus_df["OPs"], convert_to_tensor=True)


def get_download_link(df):
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"similar_{current_datetime}.csv"
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download CSV File</a>'
    
    return href

def similarity_finder(df):
     
    df2 = pd.DataFrame(columns=['Title','New Code', 'Similar', 'Similarity Score'])
    op_to_new_code = dict(zip(corpus_df["OPs"], corpus_df["New Code"]))

    similar_counts = {}

    for index, row in df.iterrows():
        query = row["Title"]
        similarity_threshold = 0.6

        query_embedding = embedder.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, corpus_embeddings)

        hits = hits[0]
        found_results = False
        similar_count = 0

        for hit in hits:
            hit_id = hit['corpus_id']
            title = corpus_df.iloc[hit_id]["OPs"]
            score = hit['score']

            if score > similarity_threshold and similar_count < 10:
                
                new_code = op_to_new_code.get(title, "N/A")
                df2 = df2.append({'Title': query, 'New Code': new_code, 'Similar': title, 'Similarity Score': score}, ignore_index=True)
                found_results = True
                similar_count += 1
    
                if query in similar_counts:
                    similar_counts[query] += 1
                else:
                    similar_counts[query] = 1
        
        if not found_results:
            df2 = df2.append({'Title': query,'New Code': "Didn't Found",'Similar': "Didn't Found", 'Similarity Score': "Didn't Found"}, ignore_index=True)

    # Save the results to a CSV file
    # df2.to_csv("similarity_L1_results.csv", index=False)
    st.subheader("Similarity")
    st.dataframe(df2)
    st.markdown(get_download_link(df2), unsafe_allow_html=True)
    
st.title("👨‍💻 Prodago RAG")
st.write("OP Similarity Search")

uploaded_file = st.file_uploader("Upload a file", type=["xlsx", "xls","csv"])

st.markdown("### Download Sample CSV")
sample = pd.read_csv("sample_similarity.csv")
st.markdown(get_download_link(sample), unsafe_allow_html=True)

if uploaded_file is not None:
    ldf = pd.read_csv(uploaded_file,encoding="latin-1")
    st.write(ldf)

    if st.button("Generate Similarities"):
        similarity_finder(ldf)
