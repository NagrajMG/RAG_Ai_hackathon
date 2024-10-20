from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
from langchain.text_splitter import RecursiveCharacterTextSplitter
from nltk.tokenize import word_tokenize
import numpy as np


def MinMaxNorm(values):
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:
        return [0 for _ in values] 
    return [(x - min_val) / (max_val - min_val) for x in values]


def BreakDown(documents,chunk_size=200,chunk_overlap = 20):
    all_documents_concatenated = "\n".join(documents)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap = chunk_overlap)
    text_chunks = text_splitter.split_text(all_documents_concatenated)
    return text_chunks



    
def Search2(query,tokenized_corpus):
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = word_tokenize(query.lower())
    doc_scores = bm25.get_scores(tokenized_query)
    return MinMaxNorm(doc_scores)



def Search1(query,chunks):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(chunks)
    query_vector=tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    return(cosine_similarities)
    

    
    
def Search_with_custom_alpha(query,chunks,tokenized_corpus,best_n,alpha):
    score1= Search1(query,chunks)
    score2= Search2(query,tokenized_corpus)
    score_1_2= alpha*np.array(score1) + (1-alpha)*np.array(score2)
    top_n_docs = sorted(enumerate(score_1_2), key=lambda x: x[1], reverse=True)[:best_n]
    relevant_docs = ".".join([chunks[idx] for idx, score in top_n_docs])
    return relevant_docs
    
       
