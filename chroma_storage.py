import chromadb
from chromadb.config import Settings
from datetime import datetime
import uuid

class ChromaDocumentStore:
    def __init__(self):
        # Initialize ChromaDB client with new configuration
        self.client = chromadb.PersistentClient(
            path="./chroma_db"    # Store data in local directory
        )
        
        # Create or get our collection for courses
        self.collection = self.client.get_or_create_collection(
            name="courses",
            metadata={"description": "Storage for course content chunks"}
        )

    def store_course_content(self, content_chunks, source_info):
        """
        Store course content chunks in ChromaDB
        
        Args:
            content_chunks (list): List of text chunks to store
            source_info (dict): Information about the source (file type, URL, etc.)
        """
        # Generate a unique ID for this course
        course_id = str(uuid.uuid4())
        
        # Create IDs for each chunk
        chunk_ids = [f"{course_id}_chunk_{i}" for i in range(len(content_chunks))]
        
        # Prepare metadata for each chunk
        metadatas = [{
            "course_id": course_id,
            "chunk_number": i,
            "source_type": source_info.get("type", "unknown"),
            "source_name": source_info.get("name", "unknown"),
            "timestamp": datetime.now().isoformat()
        } for i in range(len(content_chunks))]
        
        # Store in ChromaDB with embeddings
        self.collection.add(
            documents=content_chunks,
            ids=chunk_ids,
            metadatas=metadatas
        )
        
        return course_id

    def search_content(self, query, n_results=5):
        """
        Search for relevant content chunks
        
        Args:
            query (str): The search query
            n_results (int): Number of results to return
            
        Returns:
            dict: Search results including matched chunks and their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def get_course_chunks(self, course_id):
        """
        Retrieve all chunks for a specific course
        
        Args:
            course_id (str): The unique course ID
            
        Returns:
            list: All content chunks for the course
        """
        results = self.collection.get(
            where={"course_id": course_id}
        )
        return results

    def delete_course(self, course_id):
        """
        Delete a course and all its chunks
        
        Args:
            course_id (str): The unique course ID
        """
        chunk_ids = [doc.id for doc in self.collection.get(
            where={"course_id": course_id}
        )]
        self.collection.delete(ids=chunk_ids)

    def get_all_content(self):
        """
        Get all stored content
        
        Returns:
            dict: All stored documents and their metadata
        """
        all_content = self.collection.get()
        
        # Format the response in a more readable way
        formatted_content = []
        for i in range(len(all_content['ids'])):
            content_item = {
                'id': all_content['ids'][i],
                'text': all_content['documents'][i],
                'metadata': all_content['metadatas'][i]
            }
            formatted_content.append(content_item)
            
        return {
            'total_items': len(formatted_content),
            'content': formatted_content
        }