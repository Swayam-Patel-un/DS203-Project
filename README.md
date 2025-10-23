# DS203 Project: Session Summary Analysis & Search

This project is a comprehensive data science pipeline built to solve an unsupervised learning problem: recovering lost associations for a jumbled set of lecture summaries (Submitted by the students throughout the course). The goal is to take a single file of unlabeled summaries, group them into their respective lecture "sessions," and build analytical tools on top of these discovered groupings.

The final output includes a keyword-based search engine to find the most relevant sessions and their top summaries, and a visualization dashboard for exploring the session clusters.

### Methodology

1. Exploratory Data Analysis (EDA)

2. Text Vectorization (Featurization)

3. Clustering (Session Recovery)

4. Generative Cluster Summarization

5. Intra-Cluster Summary Ranking

Applications & Results

Application 1: Cluster Visualization Dashboard

Application 2: Keyword Search Engine

How to Run

Repository Structure

flowchart-project-pipeline Project Pipeline

The core logic of this project follows a multi-stage NLP and machine learning pipeline:

Raw Data (.csv) → 1. EDA & Text Pre-processing → 2. Text Vectorization (Jina & Doc2Vec) → 3. K-Means Clustering → 4. Generative Summary (API) → 5. Summary Ranking (Cosine Similarity) → 6. Visualization & Search App

🔬 Technical Deep Dive

This section details the models, algorithms, and key decisions made at each stage of the project.

1. Exploratory Data Analysis (EDA)

File: Code/1_Exploratory_Data_Analysis/EDA.ipynb

Libraries: pandas, nltk, matplotlib, seaborn

Process:

The raw data from Session-Summary-for-E6-project.xlsx - Data.csv was loaded.

Standard text pre-processing was performed using nltk:

Converted all summaries to lowercase.

Removed punctuation, special characters, and numbers.

Tokenized summaries into individual words.

Removed common English stop words.

Applied lemmatization to reduce words to their root form (e.g., "running" → "run").

The distribution of summary lengths (word count) was analyzed to understand the data's characteristics.

Output: A cleaned processed_df.csv was generated, which serves as the input for the vectorization stage.

2. Text Vectorization (Featurization)

As per the project requirements, two distinct featurization methods were explored.

Method A: Doc2Vec (gensim)

Files: Code/2_Vectorizating_Summaries/doc2vec/

Process: A Doc2Vec (Paragraph Vector) model was trained from scratch on the processed summary corpus. This model learns a fixed-length vector representation for variable-length texts.

Hyperparameter Tuning: Extensive optimization was performed to find the best model parameters, as seen in the doc2vec_opt_...ipynb notebooks. Key parameters tuned include:

dm=1 (Distributed Memory) vs. dm=0 (Distributed Bag of Words).

vector_size: The dimensionality of the embedding.

window: The context window size.

Result: A final model, doc2vec_300d_w70_dm1_e10000.model, was trained with 300 dimensions, a window size of 70, and 10,000 epochs.

Method B (Selected): Jina AI Embeddings

Files: Code/2_Vectorizating_Summaries/jina/jina_vectorizing_summaries.ipynb

Process: This approach utilized a state-of-the-art, pre-trained transformer model, jina-embeddings-v2-base-en. This model is specifically designed to create high-quality, semantically-rich embeddings for retrieval and clustering tasks.

Each processed summary was fed into the Jina model to obtain a dense vector embedding.

Output: The resulting embeddings were saved to jina_summary_embeddings.csv. These embeddings were chosen for the final clustering step due to their superior semantic representation.

3. Clustering (Session Recovery)

File: Code/3_Clustering_Summaries/jina_kmeans.ipynb

Algorithm: K-Means Clustering (from scikit-learn)

Process:

The high-dimensional Jina embeddings were used as the input features for the K-Means algorithm.

The Elbow Method and Silhouette Score were used to determine the optimal number of clusters (k).

Key Result: An optimal k=30 was identified, indicating that the jumbled summaries likely belong to 30 distinct lecture sessions.

Output:

clustered_summaries_k30.csv: The original summaries with their new cluster label (session ID).

cluster_centroids_k30.csv: The 30 centroid vectors, each representing the "average" topic of a session.

4. Generative Cluster Summarization

Files: Code/4_Cluster_Representative_Summaries/api_call.ipynb, cluster_rep_summary_generation.py

Process: Instead of simply picking one summary to represent a cluster, a more sophisticated approach was used.

For each of the 30 clusters, all summaries belonging to it were concatenated.

This large block of text was fed to a Generative AI API (e.g., Gemini or OpenAI).

The model was prompted to "generate a concise, representative summary that captures the main topics of the following text."

Output: Cluster_Representative_Summaries.csv was created, containing the 30 cluster IDs and their corresponding high-quality, AI-generated representative titles/summaries.

5. Intra-Cluster Summary Ranking

File: Code/6_Ranking_Summaries_Within_a_Cluster/summary_ranking.ipynb

Method: Cosine Similarity

Process:

To rank summaries within each cluster, each summary's Jina vector was compared to its cluster's centroid vector (from cluster_centroids_k30.csv).

The cosine similarity score was calculated for every summary, measuring how "on-topic" or "central" it is to the session's main theme.

Summaries within each of the 30 clusters were then ranked from highest to lowest similarity.

Output:

clustered_ranked_summaries.json: A complete JSON file of all clusters and their ranked summaries.

top3_summaries_app_data.json: A-pre-processed JSON file containing only the top 3 summaries for each cluster, used directly by the search app.

Applications & Results

Application 1: Cluster Visualization Dashboard

File: Code/5_Cluster_Visualization/vizualization_app.py

Framework: Streamlit

Description: A simple web application that visualizes the 30 discovered sessions. The app likely features:

A bubble chart where each bubble is a session, sized by the number of summaries or keywords.

Interactive word clouds that update when a user clicks on a session bubble, showing the most important terms for that topic.

Application 2: Keyword Search Engine

Files: Code/7_Summary_Search_App/main.py, search_engine.py

Framework: Python (likely a console application)

Description: This is the final deliverable, providing a simple search interface for users.

Logic:

A user enters a list of keywords (e.g., "python, loops, data structures").

The search_engine.py module vectorizes this keyword query using the same Jina model used for the summaries.

This query vector is compared against the 30 stored cluster centroid vectors using cosine similarity.

The cluster with the highest similarity score is identified as the "most relevant session."

The application then fetches the AI-generated representative summary for that session (from Cluster_Representative_Summaries.csv) and the top 3 student-written summaries (from top3_summaries_app_data.json) and displays them to the user.

