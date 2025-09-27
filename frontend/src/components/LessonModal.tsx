import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  CircularProgress,
  Alert,
  IconButton,
  Divider,
  Chip,
  FormControl,
  Select,
  MenuItem,
  Tooltip
} from '@mui/material';
import {
  Close,
  MenuBook,
  Schedule,
  CheckCircle,
  Translate,
  Language,
  VolumeUp,
  Stop
} from '@mui/icons-material';
import { Lesson, TranslationState, TranslationResponse } from '../types';
import axios from 'axios';

interface LessonModalProps {
  open: boolean;
  onClose: () => void;
  lesson: Lesson | null;
  courseId: string;
}

export default function LessonModal({ open, onClose, lesson, courseId }: LessonModalProps) {
  const [lessonContent, setLessonContent] = useState<string>('');
  const [originalContent, setOriginalContent] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Translation state
  const [translationState, setTranslationState] = useState({
    isTranslated: false,
    currentLanguage: 'en',
    targetLanguage: 'ta',
    isLoading: false,
    error: null
  });

  const [speechState, setSpeechState] = useState({
    isPlaying: false,
    isLoading: false,
    error: null as string | null,
    audioData: null as string | null,
    audioElement: null as HTMLAudioElement | null
  });
  
  const [availableLanguages] = useState([
    { code: 'en', name: 'English' },
    { code: 'ta', name: 'Tamil' },
    { code: 'hi', name: 'Hindi' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ja', name: 'Japanese' }
  ]);

  useEffect(() => {
    if (open && lesson) {
      fetchLessonContent();
    }
  }, [open, lesson]);

  const fetchLessonContent = async () => {
    if (!lesson) return;

    setLoading(true);
    setError(null);
    setLessonContent('');
    setOriginalContent('');

    try {
      const response = await axios.post('http://localhost:5000/lesson-content', {
        lesson_title: lesson.title,
        lesson_summary: lesson.summary,
        course_id: courseId
      });

      const content = response.data.content;
      setLessonContent(content);
      setOriginalContent(content);
      
      // Reset translation state
      setTranslationState(prev => ({
        ...prev,
        isTranslated: false,
        currentLanguage: 'en',
        error: null
      }));
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.error || err.message;
        setError(`Failed to load lesson content: ${errorMessage}`);
      } else {
        setError('Failed to load lesson content. Please try again.');
      }
      console.error('Lesson content error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (!lessonContent || !originalContent) return;

    setTranslationState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await axios.post('http://localhost:5000/translate-lesson', {
        content: translationState.isTranslated ? originalContent : lessonContent,
        target_lang: translationState.isTranslated ? 'en' : translationState.targetLanguage
      });

      const { translated_content, target_lang_name } = response.data;
      
      setLessonContent(translated_content);
      setTranslationState(prev => ({
        ...prev,
        isTranslated: !prev.isTranslated,
        currentLanguage: prev.isTranslated ? 'en' : prev.targetLanguage,
        isLoading: false,
        error: null
      }));
    } catch (err) {
      const errorMessage = axios.isAxiosError(err) 
        ? err.response?.data?.error || err.message
        : 'Translation failed. Please try again.';
      
      setTranslationState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage
      }));
      console.error('Translation error:', err);
    }
  };

  const handleLanguageChange = (event: any) => {
    const newTargetLang = event.target.value;
    setTranslationState(prev => ({
      ...prev,
      targetLanguage: newTargetLang
    }));
  };

  const handleClose = () => {
    // Stop any playing audio
    if (speechState.audioElement) {
      speechState.audioElement.pause();
      speechState.audioElement.currentTime = 0;
    }
    setSpeechState({
      isPlaying: false,
      isLoading: false,
      error: null,
      audioData: null,
      audioElement: null
    });
    
    setLessonContent('');
    setOriginalContent('');
    setError(null);
    setTranslationState({
      isTranslated: false,
      currentLanguage: 'en',
      targetLanguage: 'ta',
      isLoading: false,
      error: null
    });
    onClose();
  };

  const handleListen = async () => {
    try {
      setSpeechState(prev => ({ ...prev, isLoading: true, error: null }));
      
      const currentContent = translationState.isTranslated ? originalContent : lessonContent;
      const currentLanguage = translationState.isTranslated ? translationState.currentLanguage : 'en';
      
      if (!currentContent) {
        setSpeechState(prev => ({ ...prev, isLoading: false, error: 'No content available for speech' }));
        return;
      }

      // If we already have audio data and it's for the same content, just play/pause
      if (speechState.audioData && speechState.audioElement) {
        if (speechState.isPlaying) {
          speechState.audioElement.pause();
          setSpeechState(prev => ({ ...prev, isPlaying: false }));
        } else {
          speechState.audioElement.play();
          setSpeechState(prev => ({ ...prev, isPlaying: true }));
        }
        return;
      }

      // Generate new speech
      const response = await fetch('http://localhost:5000/lesson-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: currentContent,
          language: currentLanguage
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate speech');
      }

      const data = await response.json();
      
      // Create audio element from base64 data
      const audio = new Audio(`data:audio/mp3;base64,${data.audio_base64}`);
      
      audio.onended = () => {
        setSpeechState(prev => ({ ...prev, isPlaying: false }));
      };
      
      audio.onerror = () => {
        setSpeechState(prev => ({ ...prev, isPlaying: false, error: 'Failed to play audio' }));
      };
      
      setSpeechState(prev => ({ 
        ...prev, 
        audioData: data.audio_base64,
        audioElement: audio
      }));
      
      // Start playing
      await audio.play();
      setSpeechState(prev => ({ ...prev, isPlaying: true, isLoading: false }));
      
    } catch (error) {
      console.error('Text-to-speech error:', error);
      setSpeechState(prev => ({ 
        ...prev, 
        isLoading: false, 
        error: error instanceof Error ? error.message : 'Failed to generate speech'
      }));
    }
  };

  const stopSpeech = () => {
    if (speechState.audioElement) {
      speechState.audioElement.pause();
      speechState.audioElement.currentTime = 0;
      setSpeechState(prev => ({ ...prev, isPlaying: false }));
    }
  };

  if (!lesson) return null;

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          maxHeight: '90vh'
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        pb: 1
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <MenuBook sx={{ color: 'primary.main' }} />
          <Typography variant="h6" component="h2" sx={{ fontWeight: 600 }}>
            {lesson.title}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Translation Controls */}
          {lessonContent && !loading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <Select
                  value={translationState.targetLanguage}
                  onChange={handleLanguageChange}
                  disabled={translationState.isLoading}
                  sx={{ fontSize: '0.875rem' }}
                >
                  {availableLanguages.map((lang) => (
                    <MenuItem key={lang.code} value={lang.code}>
                      {lang.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <Tooltip title={translationState.isTranslated ? "Switch to English" : `Translate to ${availableLanguages.find(l => l.code === translationState.targetLanguage)?.name}`}>
                <Button
                  variant={translationState.isTranslated ? "contained" : "outlined"}
                  size="small"
                  onClick={handleTranslate}
                  disabled={translationState.isLoading || !lessonContent}
                  startIcon={translationState.isLoading ? <CircularProgress size={16} /> : <Translate />}
                  sx={{ 
                    minWidth: 'auto',
                    px: 2,
                    fontSize: '0.875rem'
                  }}
                >
                  {translationState.isLoading ? 'Translating...' : 
                   translationState.isTranslated ? 'English' : 'Translate'}
                </Button>
              </Tooltip>
              
              {/* Listen Button */}
              <Tooltip title={speechState.isPlaying ? "Stop listening" : "Listen to lesson content"}>
                <Button
                  variant={speechState.isPlaying ? "contained" : "outlined"}
                  color="secondary"
                  size="small"
                  onClick={speechState.isPlaying ? stopSpeech : handleListen}
                  disabled={speechState.isLoading || !lessonContent}
                  startIcon={speechState.isLoading ? <CircularProgress size={16} /> : 
                           speechState.isPlaying ? <Stop /> : <VolumeUp />}
                  sx={{ 
                    minWidth: 'auto',
                    px: 2,
                    fontSize: '0.875rem'
                  }}
                >
                  {speechState.isLoading ? 'Loading...' : 
                   speechState.isPlaying ? 'Stop' : 'Listen'}
                </Button>
              </Tooltip>
            </Box>
          )}
          
          <IconButton
            onClick={handleClose}
            sx={{ 
              color: 'text.secondary',
              '&:hover': {
                backgroundColor: 'action.hover'
              }
            }}
          >
            <Close />
          </IconButton>
        </Box>
      </DialogTitle>

      <Divider />

      <DialogContent sx={{ p: 3 }}>
        {/* Lesson Summary */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            {lesson.summary}
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              icon={<Schedule />}
              label="15-20 min read"
              size="small"
              variant="outlined"
              color="primary"
            />
            <Chip
              icon={<CheckCircle />}
              label="Comprehensive"
              size="small"
              variant="outlined"
              color="success"
            />
            {lessonContent && (
              <Chip
                icon={<Language />}
                label={translationState.isTranslated 
                  ? availableLanguages.find(l => l.code === translationState.currentLanguage)?.name || 'Translated'
                  : 'English'
                }
                size="small"
                variant="outlined"
                color={translationState.isTranslated ? "secondary" : "default"}
              />
            )}
          </Box>
        </Box>

        <Divider sx={{ mb: 3 }} />

        {/* Lesson Content */}
        <Box sx={{ minHeight: 200 }}>
          {loading && (
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              justifyContent: 'center',
              py: 4
            }}>
              <CircularProgress size={40} sx={{ mb: 2 }} />
              <Typography variant="body2" color="text.secondary">
                Generating comprehensive lesson content...
              </Typography>
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {translationState.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Translation Error: {translationState.error}
            </Alert>
          )}

          {speechState.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Speech Error: {speechState.error}
            </Alert>
          )}

          {lessonContent && !loading && (
            <Box sx={{ 
              '& p': { 
                mb: 2, 
                lineHeight: 1.7,
                fontSize: '1rem'
              },
              '& h1, & h2, & h3, & h4, & h5, & h6': {
                fontWeight: 600,
                mb: 1.5,
                mt: 2,
                color: 'text.primary'
              },
              '& h1': { fontSize: '1.5rem' },
              '& h2': { fontSize: '1.3rem' },
              '& h3': { fontSize: '1.2rem' },
              '& ul, & ol': {
                pl: 3,
                mb: 2
              },
              '& li': {
                mb: 0.5
              },
              '& blockquote': {
                borderLeft: '4px solid',
                borderColor: 'primary.main',
                pl: 2,
                py: 1,
                mb: 2,
                backgroundColor: 'action.hover',
                fontStyle: 'italic'
              },
              '& strong': {
                fontWeight: 600,
                color: 'text.primary'
              }
            }}>
              {lessonContent.split('\n').map((paragraph, index) => {
                if (paragraph.trim() === '') return null;
                
                // Check if it's a heading (starts with # or is all caps)
                if (paragraph.startsWith('#') || (paragraph.length < 50 && paragraph === paragraph.toUpperCase() && paragraph.length > 3)) {
                  const level = paragraph.startsWith('#') ? paragraph.match(/^#+/)?.[0].length || 1 : 2;
                  const text = paragraph.replace(/^#+\s*/, '');
                  const Component = level === 1 ? 'h1' : level === 2 ? 'h2' : 'h3';
                  
                  return (
                    <Typography
                      key={index}
                      component={Component}
                      variant={level === 1 ? 'h5' : level === 2 ? 'h6' : 'subtitle1'}
                      sx={{ 
                        fontWeight: 600, 
                        mb: 1.5, 
                        mt: index > 0 ? 2 : 0,
                        color: 'text.primary'
                      }}
                    >
                      {text}
                    </Typography>
                  );
                }
                
                // Regular paragraph
                return (
                  <Typography
                    key={index}
                    variant="body1"
                    sx={{ 
                      mb: 2, 
                      lineHeight: 1.7,
                      textAlign: 'justify'
                    }}
                  >
                    {paragraph}
                  </Typography>
                );
              })}
            </Box>
          )}

          {!loading && !error && !lessonContent && (
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              justifyContent: 'center',
              py: 4,
              textAlign: 'center'
            }}>
              <MenuBook sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
              <Typography variant="body1" color="text.secondary">
                Click "Load Content" to generate detailed lesson material
              </Typography>
            </Box>
          )}
        </Box>
      </DialogContent>

      <Divider />

      <DialogActions sx={{ p: 3, gap: 1 }}>
        <Button
          onClick={handleClose}
          variant="outlined"
          color="primary"
        >
          Close
        </Button>
        
        {error && (
          <Button
            onClick={fetchLessonContent}
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <CircularProgress size={16} color="inherit" sx={{ mr: 1 }} />
                Loading...
              </>
            ) : (
              'Retry'
            )}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
