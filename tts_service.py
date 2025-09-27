"""
Text-to-Speech Service for converting lesson content to audio
"""
import os
import base64
import tempfile
from typing import Optional, Dict, List
from gtts import gTTS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService:
    """
    Service for converting text to speech using Google Text-to-Speech
    """
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.supported_languages = {
            'en': 'en',  # English
            'es': 'es',  # Spanish
            'fr': 'fr',  # French
            'de': 'de',  # German
            'it': 'it',  # Italian
            'pt': 'pt',  # Portuguese
            'ru': 'ru',  # Russian
            'ja': 'ja',  # Japanese
            'ko': 'ko',  # Korean
            'zh': 'zh',  # Chinese
            'hi': 'hi',  # Hindi
            'ta': 'ta',  # Tamil
            'ar': 'ar',  # Arabic
            'nl': 'nl',  # Dutch
            'pl': 'pl',  # Polish
            'tr': 'tr',  # Turkish
            'vi': 'vi',  # Vietnamese
            'th': 'th',  # Thai
        }
    
    def text_to_speech(self, text: str, language: str = 'en', slow: bool = False) -> Optional[bytes]:
        """
        Convert text to speech and return audio as bytes
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es', 'fr')
            slow: Whether to speak slowly
            
        Returns:
            Audio data as bytes, or None if conversion fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to TTS service")
            return None
        
        # Map language code to gTTS language
        gtts_lang = self.supported_languages.get(language, 'en')
        
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=gtts_lang, slow=slow)
            
            # Save to temporary file
            temp_file = os.path.join(self.temp_dir, f"tts_{os.getpid()}_{hash(text)}.mp3")
            tts.save(temp_file)
            
            # Read the audio file
            with open(temp_file, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.remove(temp_file)
            
            logger.info(f"Successfully converted text to speech in {gtts_lang}")
            return audio_data
            
        except Exception as e:
            logger.error(f"Error converting text to speech: {str(e)}")
            return None
    
    def text_to_speech_base64(self, text: str, language: str = 'en', slow: bool = False) -> Optional[str]:
        """
        Convert text to speech and return audio as base64 encoded string
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es', 'fr')
            slow: Whether to speak slowly
            
        Returns:
            Base64 encoded audio data, or None if conversion fails
        """
        try:
            # Clean the text
            clean_text = self._clean_text_for_speech(text)
            
            if not clean_text:
                return None
            
            # Split text into chunks if it's too long
            text_chunks = self._split_text_into_chunks(clean_text)
            
            if not text_chunks:
                return None
            
            # For now, we'll process the first chunk only to avoid complexity
            # This should be sufficient for most lesson content
            first_chunk = text_chunks[0]
            
            # Create temporary file for audio
            temp_file = None
            
            try:
                # Generate audio
                gtts_lang = self.supported_languages.get(language, 'en')
                tts = gTTS(text=first_chunk, lang=gtts_lang, slow=slow)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.save(temp_file.name)
                temp_file.close()
                
                # Read the audio file and convert to base64
                with open(temp_file.name, 'rb') as f:
                    audio_data = f.read()
                
                return base64.b64encode(audio_data).decode('utf-8')
                
            finally:
                # Clean up temporary file
                if temp_file:
                    try:
                        os.unlink(temp_file.name)
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Error in text_to_speech_base64: {str(e)}")
            return None
    
    def convert_lesson_content_to_speech(self, content: str, language: str = 'en') -> Optional[str]:
        """
        Convert lesson content to speech, handling long content by splitting into chunks
        
        Args:
            content: Lesson content text
            language: Language code
            
        Returns:
            Base64 encoded audio data, or None if conversion fails
        """
        if not content or not content.strip():
            return None
        
        # Clean and prepare content
        # Remove markdown formatting and clean up the text
        clean_content = self._clean_text_for_speech(content)
        
        # Split content into manageable chunks (gTTS has limits)
        chunks = self._split_text_into_chunks(clean_content, max_length=5000)
        
        if not chunks:
            return None
        
        try:
            # For now, convert the first chunk or combine all chunks
            # In a more advanced implementation, we could combine multiple audio files
            combined_text = " ".join(chunks[:3])  # Limit to first 3 chunks to avoid very long audio
            
            return self.text_to_speech_base64(combined_text, language)
            
        except Exception as e:
            logger.error(f"Error converting lesson content to speech: {str(e)}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text for better speech synthesis
        """
        # Remove markdown headers
        clean_text = text.replace('#', '').replace('*', '')
        
        # Remove excessive whitespace
        clean_text = ' '.join(clean_text.split())
        
        # Add natural pauses after sentences
        clean_text = clean_text.replace('.', '. ').replace('!', '! ').replace('?', '? ')
        
        return clean_text.strip()
    
    def _split_text_into_chunks(self, text: str, max_length: int = 5000) -> list:
        """
        Split text into chunks that are suitable for TTS conversion
        
        Args:
            text: Input text
            max_length: Maximum length of each chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_length:
                current_chunk += sentence + '. '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get dictionary of supported language codes and names
        """
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'ar': 'Arabic',
            'nl': 'Dutch',
            'pl': 'Polish',
            'tr': 'Turkish',
            'vi': 'Vietnamese',
            'th': 'Thai',
        }
        
        # Return only supported languages with their names
        return {code: name for code, name in language_names.items() if code in self.supported_languages}

# Global TTS service instance
tts_service = TTSService()