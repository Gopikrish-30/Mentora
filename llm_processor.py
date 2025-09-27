from ai_providers import ai_manager

def generate_course_from_text(text_chunks, user_prompt):
    """
    Generate course content using the AI provider manager.
    """
    try:
        return ai_manager.generate_course(text_chunks, user_prompt)
    except Exception as e:
        return {
            "course": "Error in Course Generation",
            "modules": [{
                "title": "Error",
                "lessons": [{
                    "title": "Error in Processing",
                    "summary": f"Failed to generate course content: {str(e)}",
                    "detail": "There was an error in processing the content. Please try again with different content or check the input format."
                }]
            }]
        }

def generate_lesson_content(lesson_title, lesson_summary, context_chunks):
    """
    Generate detailed lesson content using the AI provider manager.
    """
    try:
        return ai_manager.generate_lesson_content(lesson_title, lesson_summary, context_chunks)
    except Exception as e:
        return f"Error generating lesson content: {str(e)}. Please try again."