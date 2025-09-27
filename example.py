import os
from content_ingestion import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_youtube,
    extract_text_from_website
)
from vector_store import VectorStore
from datetime import datetime

def process_and_store_document(vector_store, file_path, content_type="pdf"):
    """Process a document and store it in the vector database"""
    try:
        # Extract text based on content type
        if content_type == "pdf":
            with open(file_path, 'rb') as file:
                extracted_text = extract_text_from_pdf(file)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

        if not extracted_text:
            raise ValueError("No text was extracted from the document")

        # Prepare metadata
        metadata = {
            "type": content_type,
            "source": file_path,
            "timestamp": datetime.now().isoformat(),
            "char_count": len(extracted_text),
            "word_count": len(extracted_text.split()),
            "line_count": len(extracted_text.split('\n'))
        }

        # Store in vector database
        doc_id = vector_store.add_document(extracted_text, metadata)
        
        return extracted_text, metadata, doc_id
    
    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return None, None, None

def analyze_text(text):
    """Analyze the extracted text and return statistics"""
    if not text:
        return
        
    lines = text.split('\n')
    words = text.split()
    
    # Calculate word frequency
    word_freq = {}
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    for word in words:
        word = word.lower()
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
            
    return {
        "char_count": len(text),
        "line_count": len(lines),
        "word_count": len(words),
        "top_words": sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    }

def main():
    # Initialize vector store
    vector_store = VectorStore()
    
    # File paths
    pdf_path = r"c:\Users\admin\Desktop\CoC\Hackathon Themes  Final-9-10.pdf"

    # Process and store PDF
    print("\nProcessing PDF:", pdf_path)
    extracted_text, metadata, doc_id = process_and_store_document(vector_store, pdf_path, "pdf")
    
    if extracted_text and metadata and doc_id:
        print("\n✅ Successfully processed and stored the document!")
        print(f"Document ID: {doc_id}")
        
        # Display document content
        print("\nExtracted Content:")
        print("=" * 80)
        print(extracted_text)
        print("=" * 80)
        
        # Display metadata
        print("\nDocument Metadata:")
        print("-" * 40)
        for key, value in metadata.items():
            print(f"{key}: {value}")
            
        # Analyze text
        stats = analyze_text(extracted_text)
        
        print("\nText Analysis:")
        print("-" * 40)
        print(f"Characters: {stats['char_count']}")
        print(f"Lines: {stats['line_count']}")
        print(f"Words: {stats['word_count']}")
        
        print("\nMost common meaningful words:")
        print("-" * 40)
        for word, count in stats['top_words']:
            print(f"{word}: {count} times")
            
        # Test vector similarity search
        print("\nTesting similarity search:")
        print("-" * 40)
        search_query = "course creation learning"
        results = vector_store.query_similar(search_query, n_results=3)
        print(f"Query: '{search_query}'")
        print("Top 3 similar documents:")
        for i, (doc_id, text) in enumerate(zip(results['ids'][0], results['documents'][0])):
            print(f"\n{i+1}. Document ID: {doc_id}")
            print(f"First 100 characters: {text[:100]}...")
    else:
        print("❌ Failed to process the document")

if __name__ == "__main__":
    main()