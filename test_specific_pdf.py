from content_ingestion import extract_text_from_pdf
from vector_store import VectorStore
from datetime import datetime

def test_specific_pdf():
    # Initialize vector store
    vector_store = VectorStore(persist_directory="./pdf_test_vector_db")
    
    # PDF file path
    pdf_path = r"C:\Users\admin\Desktop\CoC\Hackathon Themes  Final-9-10.pdf"
    
    print(f"\nTesting PDF extraction from: {pdf_path}")
    print("-" * 80)
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            # Extract text
            extracted_text = extract_text_from_pdf(pdf_file)
            
            if extracted_text:
                print("Text extracted successfully!")
                print("\nFirst 500 characters of extracted text:")
                print("-" * 80)
                print(extracted_text[:500])
                print("-" * 80)
                
                # Store in vector database
                metadata = {
                    "type": "pdf",
                    "source": pdf_path,
                    "timestamp": datetime.now().isoformat()
                }
                
                doc_id = vector_store.add_document(extracted_text, metadata)
                print("\nDocument stored in vector database with ID:", doc_id)
                
                # Test retrieval
                print("\nTesting retrieval from vector store...")
                doc = vector_store.get_document_by_id(doc_id)
                if doc and len(doc['documents']) > 0:
                    print("Document retrieved successfully!")
                    
                # Get document statistics
                word_count = len(extracted_text.split())
                char_count = len(extracted_text)
                line_count = len(extracted_text.splitlines())
                
                print("\nDocument Statistics:")
                print(f"Word count: {word_count}")
                print(f"Character count: {char_count}")
                print(f"Line count: {line_count}")
                
            else:
                print("No text was extracted from the PDF!")
                
    except FileNotFoundError:
        print(f"Error: The PDF file was not found at {pdf_path}")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    test_specific_pdf()