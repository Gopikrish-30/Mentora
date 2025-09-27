from flask import Flask, request, jsonify
from flask_cors import CORS
from content_ingestion import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx,
    extract_text_from_youtube,
    extract_text_from_website,
)
from text_preprocessing import clean_and_chunk_text
from ai_providers import ai_manager
from chroma_storage import ChromaDocumentStore
from translation_service import translation_service
from quiz_generator import quiz_generator
from tts_service import tts_service
from pptx_generator import pptx_generator
from pdf_generator import pdf_generator

app = Flask(__name__)
CORS(app)

# Initialize ChromaDB
document_store = ChromaDocumentStore()

@app.route('/upload', methods=['POST'])
def upload_content():
    try:
        text = ""
        user_prompt = request.form.get('prompt', '')
        source_info = {}
        
        if not request.files and not request.form.get('url'):
            return jsonify({"error": "No file or URL provided"}), 400

        if 'file' in request.files:
            file = request.files['file']
            if not file.filename:
                return jsonify({"error": "No file selected"}), 400
                
            source_info = {
                "type": file.filename.split('.')[-1].lower(),
                "name": file.filename
            }
            
            try:
                if file.filename.endswith('.pdf'):
                    text = extract_text_from_pdf(file)
                elif file.filename.endswith('.docx'):
                    text = extract_text_from_docx(file)
                elif file.filename.endswith('.pptx'):
                    text = extract_text_from_pptx(file)
                else:
                    return jsonify({"error": "Unsupported file type"}), 400
            except Exception as e:
                return jsonify({"error": f"Failed to extract content: {str(e)}"}), 500
                
        elif 'url' in request.form:
            url = request.form['url']
            if not url:
                return jsonify({"error": "No URL provided"}), 400
                
            source_info = {
                "type": "youtube" if ('youtube.com' in url or 'youtu.be' in url) else "website",
                "name": url
            }
            
            try:
                if 'youtube.com' in url or 'youtu.be' in url:
                    text = extract_text_from_youtube(url)
                else:
                    text = extract_text_from_website(url)
            except Exception as e:
                return jsonify({"error": f"Failed to extract content: {str(e)}"}), 500

        if not text.strip():
            return jsonify({"error": "No content could be extracted"}), 400

        # Clean and chunk the text
        try:
            chunks = clean_and_chunk_text(text)
            if not chunks:
                return jsonify({"error": "Content processing failed"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to process text: {str(e)}"}), 500

        try:
            # Store chunks in ChromaDB
            course_id = document_store.store_course_content(chunks, source_info)
            
            # Generate course using AI manager with fallback
            generated_course = ai_manager.generate_course(chunks, user_prompt)
            
            response_data = {
                "course_id": course_id,
                "extracted_text": text,
                "course": generated_course
            }
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": f"Failed to store or process content: {str(e)}"}), 500
            
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/search', methods=['POST'])
def search_content():
    """
    Search for relevant content in stored courses
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        course_id = data.get('course_id', '')
        n_results = data.get('n_results', 5)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Search in ChromaDB
        results = document_store.search_content(query, n_results)
        
        return jsonify({
            "results": results,
            "query": query
        })
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/lesson-content', methods=['POST'])
def get_lesson_content():
    """
    Get detailed lesson content using RAG from ChromaDB
    """
    try:
        data = request.get_json()
        lesson_title = data.get('lesson_title', '')
        lesson_summary = data.get('lesson_summary', '')
        course_id = data.get('course_id', '')
        
        if not lesson_title:
            return jsonify({"error": "Lesson title is required"}), 400
        
        # Create a comprehensive query for RAG
        query = f"{lesson_title} {lesson_summary}"
        
        # Search for relevant content
        search_results = document_store.search_content(query, n_results=10)
        
        # Combine the search results into context
        context_chunks = []
        if search_results and 'documents' in search_results:
            for doc_list in search_results['documents']:
                for doc in doc_list:
                    if doc and len(doc.strip()) > 50:  # Filter out very short chunks
                        context_chunks.append(doc)
        
        # Create comprehensive lesson content using the context
        lesson_content = ai_manager.generate_lesson_content(
            lesson_title=lesson_title,
            lesson_summary=lesson_summary,
            context_chunks=context_chunks
        )
        
        return jsonify({
            "lesson_title": lesson_title,
            "content": lesson_content,
            "context_sources": len(context_chunks)
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate lesson content: {str(e)}"}), 500
    query = request.json.get('query')
    n_results = request.json.get('n_results', 5)
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
        
    results = document_store.search_content(query, n_results)
    return jsonify(results)

@app.route('/course/<course_id>', methods=['GET'])
def get_course(course_id):
    """
    Retrieve all content for a specific course
    """
    try:
        course_content = document_store.get_course_chunks(course_id)
        return jsonify(course_content)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a course and all its content
    """
    try:
        document_store.delete_course(course_id)
        return jsonify({"message": "Course deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/all-content', methods=['GET'])
def get_all_content():
    """Get all stored content from ChromaDB"""
    try:
        all_content = document_store.get_all_content()
        return jsonify(all_content)
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve content: {str(e)}"}), 500

@app.route('/translate', methods=['POST'])
def translate_content():
    """
    Translate text content to target language
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_lang = data.get('target_lang', 'ta')  # Default to Tamil
        source_lang = data.get('source_lang', 'auto')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Translate the text
        translated_text = translation_service.translate_text(text, source_lang, target_lang)
        
        return jsonify({
            "original_text": text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "target_lang_name": translation_service.get_language_name(target_lang)
        })
        
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

@app.route('/translate-lesson', methods=['POST'])
def translate_lesson():
    """
    Translate lesson content preserving formatting
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        target_lang = data.get('target_lang', 'ta')  # Default to Tamil
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        # Translate lesson content
        translated_content = translation_service.translate_lesson_content(content, target_lang)
        
        return jsonify({
            "original_content": content,
            "translated_content": translated_content,
            "target_lang": target_lang,
            "target_lang_name": translation_service.get_language_name(target_lang)
        })
        
    except Exception as e:
        return jsonify({"error": f"Lesson translation failed: {str(e)}"}), 500

@app.route('/languages', methods=['GET'])
def get_supported_languages():
    """
    Get list of supported languages for translation
    """
    try:
        languages = translation_service.get_supported_languages()
        return jsonify({
            "languages": languages,
            "default_languages": {
                "en": "English",
                "ta": "Tamil",
                "hi": "Hindi",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "zh": "Chinese",
                "ja": "Japanese"
            }
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get languages: {str(e)}"}), 500

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    """
    Generate a quiz from lesson or module content
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        topic = data.get('topic', 'Quiz')
        num_questions = data.get('num_questions', 5)
        content_type = data.get('content_type', 'lesson')  # 'lesson' or 'module'
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        # Generate quiz based on content type
        if content_type == 'module':
            # For module, content should be module data with lessons
            quiz = quiz_generator.generate_quiz_from_module(content)
        else:
            # For individual lesson
            quiz = quiz_generator.generate_quiz_from_content(content, topic, num_questions)
        
        return jsonify({
            "quiz": quiz.to_dict(),
            "topic": topic,
            "content_type": content_type
        })
        
    except Exception as e:
        return jsonify({"error": f"Quiz generation failed: {str(e)}"}), 500

@app.route('/generate-module-quiz', methods=['POST'])
def generate_module_quiz():
    """
    Generate a quiz from a complete module with lessons
    """
    try:
        data = request.get_json()
        module_data = data.get('module_data')
        
        if not module_data or not isinstance(module_data, dict):
            return jsonify({"error": "Module data is required"}), 400
        
        quiz = quiz_generator.generate_quiz_from_module(module_data)
        
        return jsonify({
            "quiz": quiz.to_dict(),
            "module_title": module_data.get('title', 'Module')
        })
        
    except Exception as e:
        return jsonify({"error": f"Module quiz generation failed: {str(e)}"}), 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech and return audio as base64 encoded string
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text or not text.strip():
            return jsonify({"error": "Text is required"}), 400
        
        # Convert text to speech
        audio_base64 = tts_service.text_to_speech_base64(text, language)
        
        if audio_base64 is None:
            return jsonify({"error": "Failed to convert text to speech"}), 500
        
        return jsonify({
            "audio_base64": audio_base64,
            "text_length": len(text),
            "language": language,
            "format": "mp3"
        })
        
    except Exception as e:
        return jsonify({"error": f"Text-to-speech conversion failed: {str(e)}"}), 500

@app.route('/lesson-speech', methods=['POST'])
def lesson_speech():
    """
    Convert lesson content to speech, optimized for lesson formatting
    """
    try:
        data = request.get_json()
        content = data.get('content', '')
        language = data.get('language', 'en')
        
        if not content or not content.strip():
            return jsonify({"error": "Content is required"}), 400
        
        # Convert lesson content to speech
        audio_base64 = tts_service.convert_lesson_content_to_speech(content, language)
        
        if audio_base64 is None:
            return jsonify({"error": "Failed to convert lesson content to speech"}), 500
        
        return jsonify({
            "audio_base64": audio_base64,
            "content_length": len(content),
            "language": language,
            "format": "mp3"
        })
        
    except Exception as e:
        return jsonify({"error": f"Lesson speech conversion failed: {str(e)}"}), 500

@app.route('/tts-languages', methods=['GET'])
def get_tts_languages():
    """
    Get list of supported languages for text-to-speech
    """
    try:
        languages = tts_service.get_supported_languages()
        return jsonify({
            "languages": languages,
            "default_language": "en"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get TTS languages: {str(e)}"}), 500

@app.route('/generate-pptx', methods=['POST'])
def generate_pptx():
    """
    Generate PowerPoint presentation from course data
    """
    try:
        data = request.get_json()
        course_data = data.get('courseData')
        
        if not course_data:
            return jsonify({"error": "No course data provided"}), 400
        
        # Generate PowerPoint from course data
        filename = pptx_generator.generate_from_course(course_data)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "download_url": f"/downloads/{filename}"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate PowerPoint: {str(e)}"}), 500

@app.route('/generate-pptx-from-text', methods=['POST'])
def generate_pptx_from_text():
    """
    Generate PowerPoint presentation from raw text
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        title = data.get('title', 'Generated Presentation')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate PowerPoint from text
        filename = pptx_generator.generate_from_text(text, title)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "download_url": f"/downloads/{filename}"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate PowerPoint: {str(e)}"}), 500

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Generate PDF document from course data
    """
    try:
        data = request.get_json()
        course_data = data.get('courseData')
        
        if not course_data:
            return jsonify({"error": "No course data provided"}), 400
        
        # Generate PDF from course data
        filename = pdf_generator.generate_from_course(course_data)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "download_url": f"/downloads/{filename}"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

@app.route('/generate-pdf-from-text', methods=['POST'])
def generate_pdf_from_text():
    """
    Generate PDF document from raw text
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        title = data.get('title', 'Generated Document')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate PDF from text
        filename = pdf_generator.generate_from_text(text, title)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "download_url": f"/downloads/{filename}"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

@app.route('/modify-content', methods=['POST'])
def modify_content():
    """
    Modify AI-generated content based on trainer feedback
    """
    try:
        data = request.get_json()
        content_type = data.get('content_type', '')  # 'course', 'module', 'lesson', 'slide'
        content_id = data.get('content_id', '')
        modification_prompt = data.get('modification_prompt', '')
        original_content = data.get('original_content', {})
        
        if not modification_prompt:
            return jsonify({"error": "Modification prompt is required"}), 400
        
        if not original_content:
            return jsonify({"error": "Original content is required"}), 400
        
        # Generate modified content using AI
        modified_content = ai_manager.modify_content(
            content_type=content_type,
            original_content=original_content,
            modification_prompt=modification_prompt
        )
        
        return jsonify({
            "success": True,
            "modified_content": modified_content,
            "content_type": content_type,
            "content_id": content_id
        })
        
    except Exception as e:
        return jsonify({"error": f"Content modification failed: {str(e)}"}), 500

@app.route('/delete-content', methods=['POST'])
def delete_content():
    """
    Delete specific content (course, module, lesson, or slide)
    """
    try:
        data = request.get_json()
        content_type = data.get('content_type', '')  # 'course', 'module', 'lesson', 'slide'
        content_id = data.get('content_id', '')
        parent_content = data.get('parent_content', {})  # For nested deletions
        
        if not content_type or not content_id:
            return jsonify({"error": "Content type and ID are required"}), 400
        
        # Handle different content types
        if content_type == 'course':
            # Delete entire course from ChromaDB
            document_store.delete_course(content_id)
        elif content_type == 'module':
            # Remove module from course structure
            # This would require updating the course data structure
            pass
        elif content_type == 'lesson':
            # Remove lesson from module
            pass
        elif content_type == 'slide':
            # Remove slide from presentation
            pass
        
        return jsonify({
            "success": True,
            "message": f"{content_type} deleted successfully",
            "deleted_id": content_id
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to delete content: {str(e)}"}), 500

@app.route('/approve-content', methods=['POST'])
def approve_content():
    """
    Approve content after trainer review
    """
    try:
        data = request.get_json()
        content_type = data.get('content_type', '')
        content_id = data.get('content_id', '')
        approved_content = data.get('approved_content', {})
        
        if not content_type or not approved_content:
            return jsonify({"error": "Content type and approved content are required"}), 400
        
        # Store approved content (could be in a separate collection or mark as approved)
        # For now, we'll just return success
        
        return jsonify({
            "success": True,
            "message": f"{content_type} approved successfully",
            "approved_content": approved_content
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to approve content: {str(e)}"}), 500

@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    """
    Serve generated files for download (PowerPoint, PDF, etc.)
    """
    try:
        from flask import send_from_directory
        
        # Determine file type based on extension
        if filename.endswith('.pptx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            directory = pptx_generator.download_folder
        elif filename.endswith('.pdf'):
            mimetype = 'application/pdf'
            directory = pdf_generator.download_folder
        else:
            mimetype = 'application/octet-stream'
            directory = 'downloads'
        
        return send_from_directory(
            directory=directory,
            path=filename,
            as_attachment=True,
            mimetype=mimetype
        )
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404

if __name__ == '__main__':
    app.run(debug=True)
