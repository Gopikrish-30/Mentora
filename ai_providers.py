"""
Multi-provider AI system with fallback support
Supports: DeepSeek, Ollama (local), Hugging Face, and Gemini
"""

import os
import json
import requests
import time
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course content from text chunks"""
        pass
    
    @abstractmethod
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate detailed lesson content"""
        pass
    
    @abstractmethod
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify existing content based on trainer feedback"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available"""
        pass

class GroqProvider(AIProvider):
    """Groq API provider"""
    
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    def _make_request(self, messages: List[Dict[str, str]], max_tokens: int = 4000) -> str:
        """Make API request to Groq"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course content using Groq"""
        full_text = "\n".join(text_chunks)
        
        system_prompt = """
You are an expert Course Designer AI with deep expertise in educational content creation and curriculum development.
Your task is to transform raw content into a comprehensive, structured learning course that provides real educational value.

### Core Mission:
Create a professional-grade course that feels like a complete educational experience, not just a summary. Each lesson should be substantial, informative, and engaging.

### Rules:
1. Always output valid JSON only - no markdown, no explanations outside JSON.
2. Follow this schema exactly:
   {
     "course": "Course Title",
     "modules": [
       {
         "title": "Module Title",
         "lessons": [
           {
             "title": "Lesson Title",
             "summary": "Concise overview (2-3 sentences, max 50 words) that captures the essence.",
             "detail": "Comprehensive explanation (400-600 words). Must include: clear definitions, key concepts, real-world examples, practical applications, common misconceptions, and actionable insights."
           }
         ]
       }
     ]
   }

### Content Quality Standards:
- **Depth**: Each lesson should be substantial enough to stand alone as educational content
- **Clarity**: Use clear, accessible language while maintaining academic rigor
- **Practicality**: Include real-world examples and applications
- **Structure**: Organize information logically with clear progression
- **Completeness**: Cover topics thoroughly, not just surface-level

### Module Organization Guidelines:
- **Logical Progression**: Modules should build upon each other in a meaningful sequence
- **Balanced Content**: Each module should have 3-6 lessons for optimal learning
- **Clear Themes**: Each module should have a distinct, focused theme
- **Comprehensive Coverage**: Ensure all important aspects of the topic are covered

### Lesson Content Requirements:
- **Introduction**: Start with context and importance
- **Core Concepts**: Explain key ideas with clear definitions
- **Examples**: Provide concrete, relatable examples
- **Applications**: Show how concepts are used in practice
- **Common Pitfalls**: Address typical misconceptions or challenges
- **Takeaways**: End with key insights or actionable points

### Content Adaptation:
- If content is extensive, prioritize the most important and foundational concepts
- If content is limited, expand with related concepts and examples
- Always maintain educational value and depth
- Ensure each lesson provides genuine learning value

### Output Requirements:
- JSON format only
- No additional text or explanations
- Valid JSON structure that can be parsed directly
- All fields must be populated with meaningful content
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}\n\nHere is the content:\n{full_text}\n\nRemember to respond with valid JSON only."}
        ]
        
        try:
            response_text = self._make_request(messages, max_tokens=4000)
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                raise ValueError("Could not extract valid JSON from Groq response")
        except Exception as e:
            raise Exception(f"Groq course generation failed: {str(e)}")
    
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate detailed lesson content using Groq"""
        context_text = "\n".join(context_chunks) if context_chunks else ""
        
        lesson_prompt = f"""
You are an expert educator creating detailed lesson content.

Lesson Title: {lesson_title}
Lesson Summary: {lesson_summary}

Context from source materials:
{context_text}

Create a comprehensive, detailed lesson that:
1. Starts with a clear introduction to the topic
2. Explains key concepts with clear definitions
3. Provides real-world examples and applications
4. Addresses common misconceptions or challenges
5. Includes practical insights and takeaways
6. Is written in an engaging, educational tone
7. Is 500-800 words long
8. Uses the provided context to ensure accuracy and depth

Write the lesson content directly without any formatting or JSON structure.
"""
        
        messages = [
            {"role": "system", "content": "You are an expert educator creating comprehensive lesson content."},
            {"role": "user", "content": lesson_prompt}
        ]
        
        try:
            return self._make_request(messages, max_tokens=2000)
        except Exception as e:
            return f"Error generating lesson content: {str(e)}. Please try again."
    
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify existing content based on trainer feedback using Groq"""
        
        # Create modification prompt based on content type
        if content_type == 'course':
            system_prompt = """
You are an expert Course Designer AI. A trainer has reviewed the AI-generated course and wants to modify it based on their feedback.

Your task is to modify the course structure while maintaining the same JSON format and ensuring educational quality.

Rules:
1. Always output valid JSON only - no markdown, no explanations outside JSON.
2. Follow this exact schema:
   {
     "course": "Course Title",
     "modules": [
       {
         "title": "Module Title",
         "lessons": [
           {
             "title": "Lesson Title",
             "summary": "Concise overview (2-3 sentences, max 50 words)",
             "detail": "Comprehensive explanation (400-600 words)"
           }
         ]
       }
     ]
   }
3. Incorporate the trainer's feedback while maintaining educational value
4. Ensure all content is relevant and well-structured
"""
            
            user_prompt = f"""
Original Course Content:
{json.dumps(original_content, indent=2)}

Trainer's Modification Request:
{modification_prompt}

Please modify the course content according to the trainer's feedback. Return only the modified JSON structure.
"""
        
        elif content_type == 'module':
            system_prompt = """
You are an expert Course Designer AI. A trainer wants to modify a specific module in the course.

Your task is to modify the module while maintaining the same JSON format and ensuring educational quality.

Rules:
1. Always output valid JSON only
2. Follow this exact schema:
   {
     "title": "Module Title",
     "lessons": [
       {
         "title": "Lesson Title", 
         "summary": "Concise overview (2-3 sentences, max 50 words)",
         "detail": "Comprehensive explanation (400-600 words)"
       }
     ]
   }
"""
            
            user_prompt = f"""
Original Module Content:
{json.dumps(original_content, indent=2)}

Trainer's Modification Request:
{modification_prompt}

Please modify the module content according to the trainer's feedback. Return only the modified JSON structure.
"""
        
        elif content_type == 'lesson':
            system_prompt = """
You are an expert educator. A trainer wants to modify a specific lesson content.

Your task is to modify the lesson while maintaining educational quality and depth.

Rules:
1. Always output valid JSON only
2. Follow this exact schema:
   {
     "title": "Lesson Title",
     "summary": "Concise overview (2-3 sentences, max 50 words)", 
     "detail": "Comprehensive explanation (400-600 words)"
   }
"""
            
            user_prompt = f"""
Original Lesson Content:
{json.dumps(original_content, indent=2)}

Trainer's Modification Request:
{modification_prompt}

Please modify the lesson content according to the trainer's feedback. Return only the modified JSON structure.
"""
        
        elif content_type == 'slide':
            system_prompt = """
You are an expert presentation designer. A trainer wants to modify a PowerPoint slide.

Your task is to modify the slide content while maintaining clarity and educational value.

Rules:
1. Always output valid JSON only
2. Follow this exact schema:
   {
     "title": "Slide Title",
     "bullets": ["Bullet point 1", "Bullet point 2", "etc."]
   }
"""
            
            user_prompt = f"""
Original Slide Content:
{json.dumps(original_content, indent=2)}

Trainer's Modification Request:
{modification_prompt}

Please modify the slide content according to the trainer's feedback. Return only the modified JSON structure.
"""
        
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response_text = self._make_request(messages, max_tokens=3000)
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                raise ValueError("Could not extract valid JSON from Groq response")
        except Exception as e:
            raise Exception(f"Groq content modification failed: {str(e)}")

class OllamaProvider(AIProvider):
    """Ollama local model provider"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama2"  # Default model, can be changed
    
    def is_available(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _make_request(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make request to local Ollama instance"""
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course content using Ollama"""
        full_text = "\n".join(text_chunks)
        
        prompt = f"""
Create a structured course in JSON format from the following content:

User Request: {user_prompt}

Content:
{full_text}

Return a JSON object with this structure:
{{
  "course": "Course Title",
  "modules": [
    {{
      "title": "Module Title",
      "lessons": [
        {{
          "title": "Lesson Title",
          "summary": "Brief summary (max 50 words)",
          "detail": "Detailed explanation (400-600 words)"
        }}
      ]
    }}
  ]
}}

Make sure the JSON is valid and well-structured.
"""
        
        try:
            response_text = self._make_request(prompt, max_tokens=3000)
            # Clean up response and extract JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                raise ValueError("Could not extract valid JSON from Ollama response")
        except Exception as e:
            raise Exception(f"Ollama course generation failed: {str(e)}")
    
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate detailed lesson content using Ollama"""
        context_text = "\n".join(context_chunks) if context_chunks else ""
        
        prompt = f"""
Create a comprehensive lesson about: {lesson_title}

Summary: {lesson_summary}

Context:
{context_text}

Write a detailed lesson (500-800 words) that includes:
- Clear introduction
- Key concepts and definitions
- Real-world examples
- Practical applications
- Common misconceptions
- Key takeaways

Write in an engaging, educational tone.
"""
        
        try:
            return self._make_request(prompt, max_tokens=1500)
        except Exception as e:
            return f"Error generating lesson content: {str(e)}. Please try again."
    
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify existing content based on trainer feedback using Ollama"""
        prompt = f"""
Modify the following {content_type} content based on the trainer's feedback:

Original Content:
{json.dumps(original_content, indent=2)}

Trainer's Modification Request:
{modification_prompt}

Please return the modified content in the same JSON format as the original.
"""
        
        try:
            response_text = self._make_request(prompt, max_tokens=2000)
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                raise ValueError("Could not extract valid JSON from Ollama response")
        except Exception as e:
            raise Exception(f"Ollama content modification failed: {str(e)}")

class HuggingFaceProvider(AIProvider):
    """Hugging Face Transformers provider (local)"""
    
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"  # Lightweight model
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the Hugging Face model"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
        except ImportError:
            print("Transformers library not installed. Install with: pip install transformers torch")
        except Exception as e:
            print(f"Error loading Hugging Face model: {e}")
    
    def is_available(self) -> bool:
        return self.model is not None and self.tokenizer is not None
    
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course content using Hugging Face (simplified)"""
        # For now, return a basic structure since HF models need more complex setup
        return {
            "course": "Generated Course",
            "modules": [{
                "title": "Introduction",
                "lessons": [{
                    "title": "Overview",
                    "summary": "Basic overview of the topic",
                    "detail": "This is a placeholder lesson. Hugging Face integration requires more complex setup for quality content generation."
                }]
            }]
        }
    
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate lesson content using Hugging Face"""
        return f"This is a placeholder lesson about {lesson_title}. Hugging Face integration requires more complex setup for quality content generation."
    
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify content using Hugging Face (placeholder)"""
        return {
            "error": "Hugging Face content modification not fully implemented",
            "original_content": original_content,
            "modification_request": modification_prompt
        }

class GeminiProvider(AIProvider):
    """Original Gemini provider (fallback)"""
    
    def __init__(self):
        try:
            import google.generativeai as genai
            if os.environ.get("GOOGLE_API_KEY"):
                genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
                self.model = genai.GenerativeModel('gemini-pro')
            else:
                self.model = None
        except ImportError:
            self.model = None
    
    def is_available(self) -> bool:
        return self.model is not None
    
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course using Gemini (original implementation)"""
        if not self.is_available():
            raise Exception("Gemini API not available")
        
        from llm_processor import generate_course_from_text
        return generate_course_from_text(text_chunks, user_prompt)
    
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate lesson content using Gemini"""
        if not self.is_available():
            raise Exception("Gemini API not available")
        
        from llm_processor import generate_lesson_content
        return generate_lesson_content(lesson_title, lesson_summary, context_chunks)
    
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify content using Gemini (fallback to simple implementation)"""
        if not self.is_available():
            raise Exception("Gemini API not available")
        
        # Simple fallback implementation
        return {
            "message": "Content modification using Gemini - basic implementation",
            "original_content": original_content,
            "modification_request": modification_prompt,
            "note": "Full Gemini integration for content modification requires additional implementation"
        }

class AIProviderManager:
    """Manager class to handle multiple AI providers with fallback"""
    
    def __init__(self):
        # Prioritize Groq as the primary provider
        self.providers = [
            GroqProvider(),
            GeminiProvider()
        ]
        self.current_provider = None
        self._select_provider()
    
    def _select_provider(self):
        """Select the best available provider, prioritizing Groq"""
        # First, try to find Groq specifically
        groq_provider = None
        for provider in self.providers:
            if isinstance(provider, GroqProvider) and provider.is_available():
                groq_provider = provider
                break
        
        if groq_provider:
            self.current_provider = groq_provider
            print(f"Selected AI provider: {groq_provider.__class__.__name__}")
            return
        
        # If Groq is not available, try other providers
        for provider in self.providers:
            if provider.is_available():
                self.current_provider = provider
                print(f"Selected AI provider: {provider.__class__.__name__}")
                return
        
        raise Exception("No AI providers available. Please configure at least one provider.")
    
    def generate_course(self, text_chunks: List[str], user_prompt: str) -> Dict[str, Any]:
        """Generate course with fallback support, prioritizing Groq"""
        # First try Groq specifically
        groq_provider = None
        for provider in self.providers:
            if isinstance(provider, GroqProvider) and provider.is_available():
                groq_provider = provider
                break
        
        if groq_provider:
            try:
                print(f"Attempting course generation with {groq_provider.__class__.__name__}")
                result = groq_provider.generate_course(text_chunks, user_prompt)
                self.current_provider = groq_provider
                return result
            except Exception as e:
                print(f"Failed with {groq_provider.__class__.__name__}: {str(e)}")
        
        # If Groq fails, try other providers
        for provider in self.providers:
            if provider.is_available() and not isinstance(provider, GroqProvider):
                try:
                    print(f"Attempting course generation with {provider.__class__.__name__}")
                    result = provider.generate_course(text_chunks, user_prompt)
                    self.current_provider = provider
                    return result
                except Exception as e:
                    print(f"Failed with {provider.__class__.__name__}: {str(e)}")
                    continue
        
        raise Exception("All AI providers failed. Please check your configuration.")
    
    def generate_lesson_content(self, lesson_title: str, lesson_summary: str, context_chunks: List[str]) -> str:
        """Generate lesson content with fallback support, prioritizing Groq"""
        # First try Groq specifically
        groq_provider = None
        for provider in self.providers:
            if isinstance(provider, GroqProvider) and provider.is_available():
                groq_provider = provider
                break
        
        if groq_provider:
            try:
                print(f"Attempting lesson generation with {groq_provider.__class__.__name__}")
                result = groq_provider.generate_lesson_content(lesson_title, lesson_summary, context_chunks)
                self.current_provider = groq_provider
                return result
            except Exception as e:
                print(f"Failed with {groq_provider.__class__.__name__}: {str(e)}")
        
        # If Groq fails, try other providers
        for provider in self.providers:
            if provider.is_available() and not isinstance(provider, GroqProvider):
                try:
                    print(f"Attempting lesson generation with {provider.__class__.__name__}")
                    result = provider.generate_lesson_content(lesson_title, lesson_summary, context_chunks)
                    self.current_provider = provider
                    return result
                except Exception as e:
                    print(f"Failed with {provider.__class__.__name__}: {str(e)}")
                    continue
        
        return "Error: All AI providers failed. Please check your configuration."
    
    def modify_content(self, content_type: str, original_content: Dict[str, Any], modification_prompt: str) -> Dict[str, Any]:
        """Modify existing content based on trainer feedback"""
        # First try Groq specifically
        groq_provider = None
        for provider in self.providers:
            if isinstance(provider, GroqProvider) and provider.is_available():
                groq_provider = provider
                break
        
        if groq_provider:
            try:
                print(f"Attempting content modification with {groq_provider.__class__.__name__}")
                result = groq_provider.modify_content(content_type, original_content, modification_prompt)
                self.current_provider = groq_provider
                return result
            except Exception as e:
                print(f"Failed with {groq_provider.__class__.__name__}: {str(e)}")
        
        # If Groq fails, try other providers
        for provider in self.providers:
            if provider.is_available() and not isinstance(provider, GroqProvider):
                try:
                    print(f"Attempting content modification with {provider.__class__.__name__}")
                    result = provider.modify_content(content_type, original_content, modification_prompt)
                    self.current_provider = provider
                    return result
                except Exception as e:
                    print(f"Failed with {provider.__class__.__name__}: {str(e)}")
                    continue
        
        raise Exception("All AI providers failed for content modification. Please check your configuration.")

# Global instance
ai_manager = AIProviderManager()
