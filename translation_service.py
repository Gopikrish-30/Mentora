from deep_translator import GoogleTranslator
from typing import Optional, Dict

class TranslationService:
    """
    Service for translating text using Google Translate API
    """
    
    def __init__(self):
        self.translator = GoogleTranslator()
        # Common language codes and names
        self.supported_languages = {
            'en': 'English',
            'ta': 'Tamil', 
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'pt': 'Portuguese',
            'it': 'Italian',
            'ru': 'Russian',
            'ar': 'Arabic',
            'bn': 'Bengali',
            'te': 'Telugu',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi'
        }
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the given text (simplified)
        """
        if not text or not text.strip():
            return "en"
        # For simplicity, default to English
        # In a real implementation, you might use a language detection library
        return "en"
    
    def translate_text(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> Optional[str]:
        """
        Translate text from source language to target language
        """
        if not text or not text.strip():
            return text
        
        try:
            # Don't translate if source and target are the same
            if source_lang == target_lang:
                return text
            
            # Use deep-translator for translation
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translation = translator.translate(text)
            return translation
                
        except Exception as e:
            print(f"Translation error: {e}")
            return f"[{self.get_language_name(target_lang)} Translation] {text}"
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get dictionary of supported language codes and names
        """
        return self.supported_languages.copy()
    
    def translate_lesson_content(self, content: str, target_lang: str = 'ta') -> str:
        """
        Translate lesson content, handling paragraphs and preserving formatting
        """
        if not content:
            return content
        
        # Split content into paragraphs
        paragraphs = content.split('\n')
        translated_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Translate each paragraph
                translated_paragraph = self.translate_text(paragraph, 'auto', target_lang)
                translated_paragraphs.append(translated_paragraph)
            else:
                # Preserve empty lines
                translated_paragraphs.append(paragraph)
        
        return '\n'.join(translated_paragraphs)
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get the full language name from language code
        """
        return self.supported_languages.get(lang_code, lang_code.upper())

# Global translation service instance
translation_service = TranslationService()
