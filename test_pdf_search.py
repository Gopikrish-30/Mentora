from vector_store import VectorStore

def test_pdf_search():
    # Initialize vector store
    vector_store = VectorStore(persist_directory="./pdf_test_vector_db")
    
    # Test different search queries
    search_queries = [
        "corporate training",
        "course creation",
        "digital payments",
        "learning objectives"
    ]
    
    print("\nTesting similarity search in the PDF content:")
    print("-" * 80)
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        results = vector_store.query_similar(query, n_results=1)
        
        if results and len(results['documents'][0]) > 0:
            print("\nFound relevant content:")
            print("-" * 40)
            print(results['documents'][0][0][:300] + "...")
        else:
            print("No relevant content found.")
            
if __name__ == "__main__":
    test_pdf_search()