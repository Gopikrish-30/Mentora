from langchain.text_splitter import RecursiveCharacterTextSplitter

def clean_and_chunk_text(text):
    # Simple cleaning: remove extra whitespace
    text = " ".join(text.split())
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text)
    return chunks