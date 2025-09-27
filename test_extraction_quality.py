from content_ingestion import (
    extract_text_from_pdf,
    extract_text_from_website
)
from vector_store import VectorStore
from datetime import datetime
import json
import os

def test_extraction_and_storage():
    # Initialize vector store with a clean test directory
    test_db_dir = "./extraction_test_db"
    vector_store = VectorStore(persist_directory=test_db_dir)
    
    # Test URLs and files
    test_urls = [
        "https://www.geeksforgeeks.org/introduction-machine-learning/",
        "https://www.geeksforgeeks.org/artificial-intelligence-an-introduction/"
    ]
    
    pdf_path = r"C:\Users\admin\Desktop\CoC\Hackathon Themes  Final-9-10.pdf"
    
    print("\n=== Testing Text Extraction and Storage ===\n")
    
    # Test Website Extraction
    print("\n--- Testing Website Extraction ---")
    for url in test_urls:
        print(f"\nProcessing URL: {url}")
        
        # Extract text
        website_text = extract_text_from_website(url)
        if website_text:
            print(f"✓ Successfully extracted text from website")
            print(f"Text length: {len(website_text)} characters")
            print(f"Word count: {len(website_text.split())}")
            
            # Store in vector database with detailed metadata
            metadata = {
                "type": "website",
                "source": url,
                "timestamp": datetime.now().isoformat(),
                "char_count": len(website_text),
                "word_count": len(website_text.split()),
                "line_count": len(website_text.splitlines())
            }
            
            doc_id = vector_store.add_document(website_text, metadata)
            print(f"✓ Successfully stored in ChromaDB with ID: {doc_id}")
            
            # Verify storage by querying
            results = vector_store.query_similar(website_text[:100], n_results=1)
            if results and len(results['documents'][0]) > 0:
                print("✓ Successfully verified storage with query")
            
    # Test PDF Extraction
    print("\n--- Testing PDF Extraction ---")
    if os.path.exists(pdf_path):
        print(f"\nProcessing PDF: {pdf_path}")
        
        with open(pdf_path, 'rb') as pdf_file:
            # Extract text
            pdf_text = extract_text_from_pdf(pdf_file)
            if pdf_text:
                print(f"✓ Successfully extracted text from PDF")
                print(f"Text length: {len(pdf_text)} characters")
                print(f"Word count: {len(pdf_text.split())}")
                
                # Store in vector database with detailed metadata
                metadata = {
                    "type": "pdf",
                    "source": pdf_path,
                    "timestamp": datetime.now().isoformat(),
                    "char_count": len(pdf_text),
                    "word_count": len(pdf_text.split()),
                    "line_count": len(pdf_text.splitlines())
                }
                
                doc_id = vector_store.add_document(pdf_text, metadata)
                print(f"✓ Successfully stored in ChromaDB with ID: {doc_id}")
                
                # Verify storage by querying
                results = vector_store.query_similar(pdf_text[:100], n_results=1)
                if results and len(results['documents'][0]) > 0:
                    print("✓ Successfully verified storage with query")
    
    # Test Collection Statistics
    print("\n--- Testing ChromaDB Collection Statistics ---")
    all_docs = vector_store.get_all_documents()
    print(f"\nTotal documents in collection: {len(all_docs['documents'])}")
    
    print("\nDocument Types Breakdown:")
    doc_types = {}
    for meta in all_docs['metadatas']:
        doc_type = meta['type']
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
    
    for doc_type, count in doc_types.items():
        print(f"- {doc_type}: {count} documents")
    
    # Test Content Quality
    print("\n--- Testing Content Quality ---")
    for i, (doc, meta) in enumerate(zip(all_docs['documents'], all_docs['metadatas'])):
        print(f"\nDocument {i+1} ({meta['type']}):")
        print(f"Source: {meta['source']}")
        print(f"Character count: {meta['char_count']}")
        print(f"Word count: {meta['word_count']}")
        print(f"Line count: {meta['line_count']}")
        print("\nFirst 200 characters of content:")
        print("-" * 80)
        print(doc[:200])
        print("-" * 80)
    
    # Test Semantic Search
    print("\n--- Testing Semantic Search Capabilities ---")
    test_queries = [
        "machine learning introduction",
        "artificial intelligence concepts",
        "course creation",
        "learning objectives"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = vector_store.query_similar(query, n_results=2)
        
        if results and len(results['documents'][0]) > 0:
            print("Top 2 matching documents:")
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                print(f"\nMatch {i+1} ({meta['type']} from {meta['source']}):")
                print(f"First 150 characters: {doc[:150]}...")

if __name__ == "__main__":
    test_extraction_and_storage()