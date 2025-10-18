import os,sys
import joblib
import numpy as np
import torch
from dotenv import load_dotenv
load_dotenv()
from huggingface_hub import InferenceClient
from transformers import AutoModelForCausalLM, AutoTokenizer
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
    def __init__(self, embedded_model_name='all-MiniLM-L6-v2', device=None):
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
        try:
            logging.info("Fitting of FAQ.csv with NearestNeighbor model for retrievel task.")
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
        except PersonalizedCoachException as e:
            logging.info(f"Error while fitting the Retrievel Chatbot: {e}")
            raise PersonalizedCoachException(e,sys)
    def retrieve(self, query:str, k=3):
        """
        Retrieve top-k most similar FAQ answers for a query.
        Returns a list of tuples: (index, similarity, question, answer)
        """
        try:
            logging.info("Retrieving the FAQ based on cosine sim for inference.")
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
        except PersonalizedCoachException as e:
            logging.info(f"Error while retriveing the FAQ from the dataset: {e}")
            raise PersonalizedCoachException(e,sys)
    
    def save(self, out_dir="models/chatbot"):
        """
        Save embeddings, NearestNeighbors index, and embedder name.
        """
        try:
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
        except PersonalizedCoachException as e:
            logging.info(f"Error whike saving the info of the Retrievel Chatbot model: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def load(self, out_dir="models/chatbot", device=None):
        """
        Load retriever artifacts (embeddings, NN index, embedder by name).
        """
        try:
            print(f"Loading retriever from {out_dir}...")

            self.embeddings = np.load(os.path.join(out_dir, 'faq_embeddings.npy'))
            self.nn = joblib.load(os.path.join(out_dir, 'nn.joblib'))
            self.faq_df = pd.read_csv(os.path.join(out_dir, 'faq_data.csv'))

            with open(os.path.join(out_dir, 'embedder_name.txt'), 'r') as f:
                self.embed_model_name = f.read().strip()

            self.embedder = SentenceTransformer(self.embed_model_name, device=device or self.device)
            print(f"✅ Loaded embedder '{self.embed_model_name}' successfully.")

            return self
        except PersonalizedCoachException as e:
            logging.info(f"Error while Loading the info of the Retrievel Chatbot model form the saved dir:{e}")
            raise PersonalizedCoachException(e,sys)
    
class Generative_Chatbot:
    """
    API-based generative chatbot using Hugging Face Inference API.
    """
    def __init__(self, model_name: str='google/gemma-2-2b-it', device:str=None, hf_token=None, temperature=0.7, top_p=0.9, repetition_penalty=1.2):
        try:
            self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
            self.model_name = model_name
            self.hf_token = hf_token or os.getenv("HF_TOKEN")
            self.temperature=temperature
            self.top_p=top_p
            self.repetition_penalty=repetition_penalty
            
            logging.info(f"Initializing API-based Generative ChatBot: {model_name}")
            
            self.client=InferenceClient(provider="auto", api_key=self.hf_token)
        except PersonalizedCoachException as e:
            logging.info(f"Error initializing API Generative Chatbot: {e}")
            raise PersonalizedCoachException(e, sys)
        
    def generate(self, messages:list)->str :
        """
        Generate text using Hugging Face API with streaming.
        """
        try:
            logging.info("Generating response via HuggingFace API...")
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=True
            )
            
            # stream response
            output=""
            for chunk in stream:
                output+=chunk.choices[0].delta.content
            return output
        except PersonalizedCoachException as e:
            logging.info(f"Error generating API response: {e}")
            raise PersonalizedCoachException(e,sys)

class Hybrid_Chatbot:
    """
    Combines retrieval (semantic search on FAQ) and generative (LLM) responses.
    """
    def __init__(self, retriever:ChatRetriever, generator:Generative_Chatbot, retrievel_threshold:float=0.65):
        try:
            logging.info("Initializing Hybrid Chatbot with retriever and generative components")
            self.retriever=retriever
            self.generator=generator
            self.threshold=retrievel_threshold
            logging.info("HybridChatbot intialized with API generator successfully...")
        except PersonalizedCoachException as e:
            logging.info(f"Error initializing Hybrid Chatbot: {e}")
            raise PersonalizedCoachException(e,sys)
        
    def rag_generate(self, query:str, k:int=3)->str:
        """
        Use retrieved FAQ context + generative reasoning to produce a detailed answer.
        """
        try:
            logging.info("Generating response using RAG pipeline.")
            results = self.retriever.retrieve(query, k=k)

            # Combine FAQ Q&A pairs into contextual knowledge
            context = "\n\n".join([f"Q: {r[2]}\nA: {r[3]}" for r in results])

            messages = [
                {'role':"system","content":"You are a professional AI fitness and nutrition assistant."},
                {'role':'assistant',"content":f"Here are some FAQ entries that might help:\n\n{context}"},
                {'role':'user','content':query}
            ]
            # Use the LLM to generate a contextual, motivational, and structured answer
            gen_response = self.generator.generate(messages)
            return gen_response

        except PersonalizedCoachException as e:
            logging.info(f"Error while generating RAG response: {e}")
            raise PersonalizedCoachException(e, sys)
        
    def chat(self, query: str, k: int = 3) -> dict:
        """
        Decides whether to use direct FAQ retrieval or RAG generation.
        Returns a dict: {'mode': 'retrieval'/'rag', 'answer': str, 'score': float}
        """
        try:
            logging.info(f"Processing query through Hybrid Chatbot: {query}")

            # Step 1: Retrieve relevant FAQs
            results = self.retriever.retrieve(query, k=k)
            if not results:
                logging.info("No FAQ results found; defaulting to RAG mode.")
                gen_response = self.rag_generate(query, k=k)
                return {"mode": "rag", "answer": gen_response, "score": None}

            top_idx, top_sim, q_text, ans_text = results[0]
            logging.info(f"Top similarity score from retrieval: {top_sim}")

            # Step 2: If similarity above threshold → use retrieval mode
            if top_sim >= self.threshold:
                logging.info("High similarity found; using Retrieval Mode.")
                return {
                    "mode": "retrieval",
                    "answer": ans_text,
                    "score": float(top_sim)
                }

            # Step 3: Otherwise → use RAG (retrieval + generation)
            logging.info("Low similarity; using RAG Mode (context + LLM generation).")
            gen_response = self.rag_generate(query, k=k)
            return {
                "mode": "rag",
                "answer": gen_response,
                "score": float(top_sim)
            }

        except PersonalizedCoachException as e:
            logging.info(f"Error in Hybrid Chatbot chat method: {e}")
            raise PersonalizedCoachException(e, sys)
        
                