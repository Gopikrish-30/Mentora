import sys
from io import BytesIO
from content_ingestion import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_youtube,
    extract_text_from_website
)

def print_separator():
    print("\n" + "="*80 + "\n")

def test_youtube_extraction():
    try:
        # Test with an educational video URL about machine learning
        url = "https://www.youtube.com/watch?v=GwIo3gDZCVQ"  # Machine Learning Basics video
        print(f"Testing YouTube extraction from: {url}")
        text = extract_text_from_youtube(url)
        if text:
            print("\nSuccessfully extracted text from YouTube video!")
            print("\nFirst 500 characters of extracted text:")
            print("-" * 40)
            print(text[:500] + "...")
            return True
        else:
            print("Error: No text was extracted from the YouTube video")
            return False
    except Exception as e:
        print(f"Error extracting YouTube text: {str(e)}")
        return False

def test_website_extraction():
    try:
        # Test with an educational website about machine learning
        url = "https://www.geeksforgeeks.org/introduction-machine-learning/"
        print(f"Testing website extraction from: {url}")
        text = extract_text_from_website(url)
        if text:
            print("\nSuccessfully extracted text from website!")
            print("\nFirst 500 characters of extracted text:")
            print("-" * 40)
            print(text[:500] + "...")
            return True
        else:
            print("Error: No text was extracted from the website")
            return False
    except Exception as e:
        print(f"Error extracting website text: {str(e)}")
        return False

def main():
    success = True
    
    print_separator()
    print("Starting Content Extraction Tests")
    print_separator()
    
    # Test YouTube extraction
    print("1. Testing YouTube Extraction")
    if not test_youtube_extraction():
        success = False
    print_separator()
    
    # Test website extraction
    print("2. Testing Website Extraction")
    if not test_website_extraction():
        success = False
    print_separator()
    
    # Summary
    print("Test Summary:")
    if success:
        print("✅ All tests completed successfully!")
    else:
        print("❌ Some tests failed. Please check the output above for details.")
    print_separator()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())