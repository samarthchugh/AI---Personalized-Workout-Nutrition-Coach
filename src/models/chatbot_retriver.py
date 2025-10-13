import os,sys
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from src.exception.exception import PersonalizedCoachException
from src.logging.logger import logging

class ChatRetriever:
    """
    Builds and serves a retrivel-based FAQ system:
    - Uses SenetenceTransformer embeddings for faq['question]
    - fits NearestNeighbors on embeddings (cosine)
    - Saves embeddings array, FAQ dataframe, embedder, and NN model as artifacts.
    """
    def __init__(self, embedded_model_name='all_MiniLM-L6-v2', device=None):
        self.embedded_model_name = embedded_model_name
        self.device = device
        self.embedder = SentenceTransformer(self.embedded_model_name, device = self.device)
        self.faq_df = None
        self.embeddings = None
        self.nn = None
    
    def fit(self, faq_df:pd.DataFrame, question_col='question', answer_col='answer', n_neighbors=4):
        """
        Encode FAQ questions and build NearestNeighbors index.
        """
        if question_col not in faq_df.columns or answer_col not in faq_df.columns:
            raise ValueError("FAQ dataframe must have 'question' and 'answer' columns.")
        
        self.faq_df = faq_df.reset_index(drop=True)
        questions = self.faq_df[question_col].astype('str').tolist()
        
        print("Encoding FAQ questions into Embeddings...")
        self.embeddings = self.embedder.encode(
            questions,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        
        print("Building NearestNeighbors index...")
        self.nn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
        self.nn.fit(self.embeddings)
        
    def retrieve(self, query:str, k=3):
        """
        Retrieve top-k most similar FAQ answers for a query.
        Returns a list of tuples: (index, similarity, question, answer)
        """
        if self.nn is None or self.faq_df is None or self.embeddings is None:
            raise RuntimeError("Model not fitted or loaded. Call fit() or load().")
        
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        dists, idxs = self.nn.kneighbors(q_emb, n_neighbors=k)
        
        results=[]
        for i in range(len(idxs[0])):
            idx = int(idxs[0][i])
            sim = float(1-dists[0][i]) # cosine similarity = 1-distance
            q_text = self.faq_df.iloc[idx]['question']
            a_text = self.faq_df.iloc[idx]['answer']
            results.append((idx,sim,q_text,a_text))
        return results
    
    def save(self, out_dir="models/chatbot"):
        """
        Save embeddings, NearestNeighbors index, and embedder name.
        """
        os.makedirs(out_dir, exist_ok=True)
        
        if self.embeddings is not None:
            np.save(os.path.join(out_dir, 'faq_embeddings.npy'),self.embeddings)
            
        if self.nn is not None:
            joblib.dump(self.nn, os.path.join(out_dir, 'nn.joblib'))
        
        if self.faq_df is not None:
            self.faq_df.to_csv(os.path.join(out_dir, "faq_data.csv"),index=False)
            
        # save onlu model name not full weights
        with open(os.path.join(out_dir, 'embedder_name.txt'),'w') as f:
            f.write(self.embedded_model_name)
            
        print(f"ChatbotRetriever saved to {out_dir}")
        
    def load(self, out_dir="models/chatbot", device=None):
        """
        Load retriever artifacts (embeddings, NN index, embedder by name).
        """
        print(f"Loading retriever from {out_dir}...")

        self.embeddings = np.load(os.path.join(out_dir, 'faq_embeddings.npy'))
        self.nn = joblib.load(os.path.join(out_dir, 'nn.joblib'))
        self.faq_df = pd.read_csv(os.path.join(out_dir, 'faq_data.csv'))

        with open(os.path.join(out_dir, 'embedder_name.txt'), 'r') as f:
            self.embed_model_name = f.read().strip()

        self.embedder = SentenceTransformer(self.embed_model_name, device=device or self.device)
        print(f"✅ Loaded embedder '{self.embed_model_name}' successfully.")

        return self
                