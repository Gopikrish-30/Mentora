import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
import json
from datetime import datetime

class VectorStore:
    def __init__(self, persist_directory="./vector_db"):
        # Create the persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize Chroma client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use simple text embedding for testing
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name="course_content",
            embedding_function=self.embedding_function
        )

    def add_document(self, text, metadata):
        """
        Add a document to the vector store
        
        Args:
            text (str): The extracted text content
            metadata (dict): Information about the document (source, type, timestamp, etc.)
        """
        # Generate a unique ID for the document
        doc_id = f"{metadata['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add the document to the collection
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id

    def query_similar(self, query_text, n_results=5):
        """
        Query the vector store for similar content
        
        Args:
            query_text (str): The text to search for
            n_results (int): Number of results to return
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def get_all_documents(self):
        """Get all documents in the collection"""
        return self.collection.get()

    def get_document_by_id(self, doc_id):
        """Get a specific document by ID"""
        return self.collection.get(ids=[doc_id])

    def get_documents_by_type(self, doc_type):
        """Get all documents of a specific type"""
        return self.collection.get(
            where={"type": doc_type}
        )