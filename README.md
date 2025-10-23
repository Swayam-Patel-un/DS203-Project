# DS203 Project: Session Summary Analysis & Search

### Introduction

This repository contains the complete data science pipeline for a project focused on unsupervised learning and natural language processing. The project addresses the challenge of organizing and analyzing a large, unlabeled corpus of text summaries.

The pipeline proceeds from raw text data through cleaning, advanced vectorization, unsupervised clustering to identify latent topics, and finally, ranking and retrieval. The end products include a set of organized and ranked summaries, a generated representative summary for each topic, and a functional keyword-based search engine to retrieve the most relevant information.

### Problem Statement

The project was initiated with a dataset of jumbled-up session summaries from a data science course. The primary association between each summary and its corresponding lecture session was lost.

The objective is to apply a systematic data science methodology to:

1. Re-establish the connection between summaries and sessions by grouping semantically similar summaries.

2. Compare different text featurization methods to find the most effective one for this task.

3. Rank the summaries within each identified session based on their relevance and detail.

4. Create a representative summary for each session.

5. Build a simple, interactive application that allows a user to find the most relevant session and its top 3 summaries based on a keyword query.

### Methodology

The project is structured as a multi-step pipeline, with each stage feeding into the next.

1. Exploratory Data Analysis and Pre-processing

  * Input: Session-Summary-for-E6-project.xlsx - Data.csv

  * Process: The raw text summaries were loaded and subjected to standard NLP pre-processing steps. This included:

    * Conversion to lowercase.

    * Removal of punctuation, numerical digits, and special characters.

    * Tokenization of summaries into individual words.

    * Removal of common English stop words.

    * Lemmatization to reduce words to their base or root form.

  * Output: A cleaned DataFrame saved as processed_df.csv.

2. Text Featurization (Vectorization)

Two distinct methods were evaluated to convert the cleaned text into numerical vectors:

* Method A (Doc2Vec): A Doc2Vec (Paragraph Vector) model was trained from scratch using the gensim library. This involved extensive hyperparameter tuning (as seen in the doc2vec_opt_... notebooks) to optimize for vector size, context window, and the training algorithm (DM vs. DBOW).

* Method B (Transformer Embeddings): A state-of-the-art, pre-trained transformer model, jina-embeddings-v2-base-en, was used. This model is specifically designed for high-performance semantic retrieval and clustering.

Selection: The Jina embeddings were selected for the final pipeline due to their superior performance in capturing semantic meaning, which is critical for clustering. The resulting vectors were stored in jina_summary_embeddings.csv.

3. Session Recovery (Clustering)

* Algorithm: K-Means Clustering

* Process: The K-Means algorithm was applied to the high-dimensional Jina embeddings. To determine the optimal number of clusters (k), the Elbow Method and Silhouette Score were analyzed.

* Result: An optimal k=30 was identified, indicating that the dataset represents 30 distinct lecture sessions.

* Output:

  * clustered_summaries_k30.csv: The original summaries with their new cluster label (session ID).

  * cluster_centroids_k30.csv: The 30 centroid vectors, each representing the semantic center of a topic.

4. Generative Cluster Summarization

To create a high-quality, human-readable label for each of the 30 clusters, a generative AI model was used.

* Process: For each cluster, all constituent summaries were concatenated into a single large text block. This text was then passed to a generative AI API (e.g., Gemini) with a prompt to generate a single, concise summary capturing the main themes.

* Output: Cluster_Representative_Summaries.csv, which maps each cluster ID to its new, generated summary.

5. Intra-Cluster Summary Ranking

To identify the "best" summaries within each session, a ranking system was implemented.

* Method: Cosine Similarity

* Process: Within each of the 30 clusters, the Jina embedding for every individual summary was compared to the cluster's centroid vector. The resulting cosine similarity score (ranging from 0 to 1) represents how "central" or "on-topic" that summary is.

* Output:

 * clustered_ranked_summaries.json: A complete JSON file of all clusters, each containing its summaries ranked by similarity score.

 * top3_summaries_app_data.json: A smaller, pre-processed file containing only the top 3 ranked summaries for each cluster, designed for use in the final application.

6. Search Application

A final application was built to provide a simple search interface for the data.

Logic:

The user provides a set of keywords. -> The application vectorizes this keyword query using the same Jina model. -> This query vector is compared against all 30 cluster centroid vectors using cosine similarity. -> The cluster with the highest similarity score is identified as the most relevant session. -> The application retrieves and displays the AI-generated representative summary for that session and the top 3 student-written summaries.
