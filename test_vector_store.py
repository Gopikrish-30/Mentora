import os
from content_ingestion import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_youtube,
    extract_text_from_website
)
from vector_store import VectorStore
from datetime import datetime

def test_vector_store():
    # Initialize vector store
    vector_store = VectorStore(persist_directory="./test_vector_db")
    
    # Test website text storage
    print("\nTesting website text storage...")
    url = "https://www.geeksforgeeks.org/introduction-machine-learning/"
    website_text = extract_text_from_website(url)
    if website_text:
        metadata = {
            "type": "website",
            "source": url,
            "timestamp": datetime.now().isoformat()
        }
        vector_store.add_document(website_text, metadata)
        
        # Query to verify storage
        results = vector_store.collection.query(
            query_texts=["machine learning"],
            n_results=1
        )
        print(f"Website text stored successfully: {len(results['documents'][0]) > 0}")
        print(f"First few characters: {results['documents'][0][0][:200]}...")
    
    # Test YouTube text storage
    print("\nTesting YouTube text storage...")
    youtube_url = "https://www.youtube.com/watch?v=aircAruvnKk"
    youtube_text = extract_text_from_youtube(youtube_url)
    if youtube_text:
        metadata = {
            "type": "youtube",
            "source": youtube_url,
            "timestamp": datetime.now().isoformat()
        }
        vector_store.add_document(youtube_text, metadata)
        
        # Query to verify storage
        results = vector_store.collection.query(
            query_texts=["neural networks"],
            n_results=1
        )
        print(f"YouTube text stored successfully: {len(results['documents'][0]) > 0}")
        print(f"First few characters: {results['documents'][0][0][:200]}...")

    # Test PDF text storage if a test PDF exists
    pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
    if os.path.exists(pdf_path):
        print("\nTesting PDF text storage...")
        with open(pdf_path, 'rb') as pdf_file:
            pdf_text = extract_text_from_pdf(pdf_file)
            if pdf_text:
                metadata = {
                    "type": "pdf",
                    "source": pdf_path,
                    "timestamp": datetime.now().isoformat()
                }
                vector_store.add_document(pdf_text, metadata)
                
                # Query to verify storage
                results = vector_store.collection.query(
                    query_texts=["content from pdf"],
                    n_results=1
                )
                print(f"PDF text stored successfully: {len(results['documents'][0]) > 0}")
                print(f"First few characters: {results['documents'][0][0][:200]}...")

    # Get all documents to verify total storage
    print("\nRetrieving all stored documents...")
    try:
        all_docs = vector_store.collection.get()
        print(f"Total documents stored: {len(all_docs['documents'])}")
        print("\nDocument types stored:")
        for meta in all_docs['metadatas']:
            print(f"- {meta['type']} from {meta['source']}")
    except Exception as e:
        print(f"Error retrieving documents: {str(e)}")

if __name__ == "__main__":
    test_vector_store()