import os
from content_ingestion import extract_text_from_pdf, extract_text_from_website
from text_preprocessing import clean_and_chunk_text
from chroma_storage import ChromaDocumentStore
import requests
from io import BytesIO

def test_pdf_extraction():
    print("\n=== Testing PDF Extraction ===")
    # Test with a sample PDF
    pdf_url = "https://arxiv.org/pdf/2303.08774.pdf"  # GPT-4 Technical Report as a test PDF
    
    try:
        # Download PDF
        print("Downloading test PDF...")
        response = requests.get(pdf_url)
        pdf_file = BytesIO(response.content)
        
        # Extract text
        print("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(pdf_file)
        
        # Check if we got meaningful text
        print(f"Extracted {len(extracted_text)} characters")
        print("\nFirst 500 characters of extracted text:")
        print("-" * 50)
        print(extracted_text[:500])
        print("-" * 50)
        
        return extracted_text
        
    except Exception as e:
        print(f"Error in PDF extraction: {str(e)}")
        return None

def test_website_extraction():
    print("\n=== Testing Website Extraction ===")
    # Test with a sample website
    web_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    try:
        print(f"Extracting text from {web_url}...")
        extracted_text = extract_text_from_website(web_url)
        
        print(f"Extracted {len(extracted_text)} characters")
        print("\nFirst 500 characters of extracted text:")
        print("-" * 50)
        print(extracted_text[:500])
        print("-" * 50)
        
        return extracted_text
        
    except Exception as e:
        print(f"Error in website extraction: {str(e)}")
        return None

def test_chromadb_storage():
    print("\n=== Testing ChromaDB Storage ===")
    try:
        # Initialize ChromaDB
        print("Initializing ChromaDB...")
        document_store = ChromaDocumentStore()
        
        # Test with PDF content
        print("\nTesting PDF content storage...")
        pdf_text = test_pdf_extraction()
        if pdf_text:
            pdf_chunks = clean_and_chunk_text(pdf_text)
            print(f"Created {len(pdf_chunks)} chunks from PDF")
            
            pdf_course_id = document_store.store_course_content(
                pdf_chunks,
                {"type": "pdf", "name": "GPT-4 Technical Report"}
            )
            print(f"Stored PDF content with course ID: {pdf_course_id}")
            
            # Test retrieval
            print("\nTesting PDF content retrieval...")
            results = document_store.search_content("what is GPT-4", n_results=1)
            print("\nSample search result for 'what is GPT-4':")
            print("-" * 50)
            print(results['documents'][0][0])
            print("-" * 50)
        
        # Test with website content
        print("\nTesting website content storage...")
        web_text = test_website_extraction()
        if web_text:
            web_chunks = clean_and_chunk_text(web_text)
            print(f"Created {len(web_chunks)} chunks from website")
            
            web_course_id = document_store.store_course_content(
                web_chunks,
                {"type": "website", "name": "AI Wikipedia"}
            )
            print(f"Stored website content with course ID: {web_course_id}")
            
            # Test retrieval
            print("\nTesting website content retrieval...")
            results = document_store.search_content("what is artificial intelligence", n_results=1)
            print("\nSample search result for 'what is artificial intelligence':")
            print("-" * 50)
            print(results['documents'][0][0])
            print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"Error in ChromaDB testing: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting extraction and storage tests...")
    test_chromadb_storage()