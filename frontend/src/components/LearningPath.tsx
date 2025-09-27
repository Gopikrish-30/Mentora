import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Button,
  Chip,
  IconButton,
  Collapse,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Divider,
  CircularProgress,
  Alert,
  Dialog,
  DialogContent
} from '@mui/material';
import {
  PlayArrow,
  Lock,
  ExpandMore,
  ExpandLess,
  MenuBook,
  Schedule,
  CheckCircle,
  Quiz as QuizIcon
} from '@mui/icons-material';
import { CourseStepProps, Module, Lesson } from '../types';
import LessonModal from './LessonModal';
import QuizModal from './QuizModal';
import { Quiz } from '../types/quiz';

interface LearningPathProps extends CourseStepProps {}

export default function LearningPath({ onNext, onBack, courseData, setCourseData }: LearningPathProps) {
  const [expandedModules, setExpandedModules] = useState<Set<number>>(new Set([0])); // First module expanded by default
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loadingLesson, setLoadingLesson] = useState<string | null>(null);
  const [quizModalOpen, setQuizModalOpen] = useState(false);
  const [currentQuizModule, setCurrentQuizModule] = useState<Module | null>(null);
  const [currentQuiz, setCurrentQuiz] = useState<Quiz | null>(null);
  const [isGeneratingQuiz, setIsGeneratingQuiz] = useState(false);
  const [completedModules, setCompletedModules] = useState<Set<number>>(new Set());

  const course = courseData.generatedCourse;

  if (!course) {
    return (
      <Paper elevation={0} sx={{ p: 4, maxWidth: '1000px', mx: 'auto' }}>
        <Alert severity="error">
          No course data available. Please go back and complete the course generation.
        </Alert>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button variant="text" color="primary" onClick={onBack}>
            Back
          </Button>
        </Box>
      </Paper>
    );
  }

  const toggleModule = (moduleIndex: number) => {
    const newExpanded = new Set(expandedModules);
    if (newExpanded.has(moduleIndex)) {
      newExpanded.delete(moduleIndex);
    } else {
      newExpanded.add(moduleIndex);
    }
    setExpandedModules(newExpanded);
  };

  const handleQuizComplete = () => {
    if (currentQuizModule) {
      const moduleIndex = course.modules.findIndex(m => m.title === currentQuizModule.title);
      if (moduleIndex !== -1) {
        setCompletedModules(prev => new Set(Array.from(prev).concat(moduleIndex)));
      }
    }
  };

  const handleLessonClick = async (lesson: Lesson) => {
    setSelectedLesson(lesson);
    setIsModalOpen(true);
  };

  const handleQuizClick = async (module: Module) => {
    setCurrentQuizModule(module);
    setIsGeneratingQuiz(true);
    setQuizModalOpen(true);
    
    try {
      const response = await fetch('http://localhost:5000/generate-module-quiz', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          module_data: module
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate quiz');
      }
      
      const data = await response.json();
      setCurrentQuiz(data.quiz);
      
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('Failed to generate quiz. Please try again.');
      setQuizModalOpen(false);
    } finally {
      setIsGeneratingQuiz(false);
    }
  };

  const getModuleStatus = (moduleIndex: number) => {
    // First and second modules are always accessible
    if (moduleIndex === 0) return 'active';
    if (moduleIndex === 1) return 'unlocked';
    
    // For modules 2 and beyond, unlock if the previous module has been completed
    if (moduleIndex >= 2 && completedModules.has(moduleIndex - 1)) {
      return 'unlocked';
    }
    
    return 'locked';
  };

  const getModuleIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <PlayArrow sx={{ fontSize: 40, color: '#1976d2' }} />;
      case 'unlocked':
        return <CheckCircle sx={{ fontSize: 40, color: '#4caf50' }} />;
      default:
        return <Lock sx={{ fontSize: 40, color: '#9e9e9e' }} />;
    }
  };

  const getModuleColor = (status: string) => {
    switch (status) {
      case 'active':
        return '#e3f2fd';
      case 'unlocked':
        return '#f1f8e9';
      default:
        return '#fafafa';
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '1000px', mx: 'auto' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <MenuBook sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
        <Typography variant="h4" component="h1">
          {course.course}
        </Typography>
      </Box>

      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
        Your structured learning path with comprehensive modules and lessons
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
        {course.modules.map((module: Module, moduleIndex: number) => {
          const status = getModuleStatus(moduleIndex);
          const isExpanded = expandedModules.has(moduleIndex);
          const isActive = status === 'active';
          const isUnlocked = status === 'unlocked' || isActive;

          return (
            <Card
              key={moduleIndex}
              sx={{
                backgroundColor: getModuleColor(status),
                border: isActive ? '2px solid #1976d2' : '1px solid #e0e0e0',
                borderRadius: 3,
                overflow: 'hidden'
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ mr: 3 }}>
                    {getModuleIcon(status)}
                  </Box>
                  
                  <Box sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <Typography variant="h6" component="h2" sx={{ fontWeight: 600 }}>
                        {module.title}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Chip
                          label={status === 'active' ? 'In Progress' : status === 'unlocked' ? 'Available' : 'Locked'}
                          color={status === 'active' ? 'primary' : status === 'unlocked' ? 'success' : 'default'}
                          size="small"
                          icon={status === 'active' ? <PlayArrow /> : status === 'unlocked' ? <CheckCircle /> : <Lock />}
                        />
                        
                        <Button
                          variant="outlined"
                          size="small"
                          startIcon={<QuizIcon />}
                          onClick={() => handleQuizClick(module)}
                          disabled={!isUnlocked || isGeneratingQuiz}
                          sx={{
                            borderColor: isUnlocked ? 'primary.main' : 'grey.400',
                            color: isUnlocked ? 'primary.main' : 'grey.400',
                            '&:hover': {
                              borderColor: isUnlocked ? 'primary.dark' : 'grey.400',
                              backgroundColor: isUnlocked ? 'primary.light' : 'transparent'
                            }
                          }}
                        >
                          Quiz
                        </Button>
                        
                        <IconButton
                          onClick={() => toggleModule(moduleIndex)}
                          disabled={!isUnlocked}
                          sx={{ 
                            color: isUnlocked ? 'primary.main' : 'grey.400',
                            transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
                            transition: 'transform 0.3s'
                          }}
                        >
                          <ExpandMore />
                        </IconButton>
                      </Box>
                    </Box>

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mt: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Schedule sx={{ fontSize: 16, color: 'text.secondary' }} />
                        <Typography variant="body2" color="text.secondary">
                          {module.lessons.length * 30} minutes
                        </Typography>
                      </Box>
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <MenuBook sx={{ fontSize: 16, color: 'text.secondary' }} />
                        <Typography variant="body2" color="text.secondary">
                          {module.lessons.length} lessons
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </Box>

                <Collapse in={isExpanded}>
                  <Divider sx={{ my: 2 }} />
                  
                  <List sx={{ py: 0 }}>
                    {module.lessons.map((lesson: Lesson, lessonIndex: number) => (
                      <React.Fragment key={lessonIndex}>
                        <ListItem
                          sx={{
                            px: 0,
                            py: 1,
                            '&:hover': {
                              backgroundColor: 'action.hover',
                              borderRadius: 1
                            }
                          }}
                        >
                          <ListItemButton
                            onClick={() => handleLessonClick(lesson)}
                            disabled={!isUnlocked}
                            sx={{
                              borderRadius: 1,
                              py: 2,
                              px: 2,
                              '&:hover': {
                                backgroundColor: isUnlocked ? 'primary.light' : 'transparent',
                                '& .MuiListItemText-primary': {
                                  color: isUnlocked ? 'primary.main' : 'text.disabled'
                                }
                              }
                            }}
                          >
                            <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                              <Box sx={{ 
                                width: 8, 
                                height: 8, 
                                borderRadius: '50%', 
                                backgroundColor: isUnlocked ? 'primary.main' : 'grey.400',
                                mr: 2,
                                flexShrink: 0
                              }} />
                              
                              <ListItemText
                                primary={
                                  <Typography 
                                    variant="subtitle1" 
                                    sx={{ 
                                      fontWeight: 500,
                                      color: isUnlocked ? 'text.primary' : 'text.disabled'
                                    }}
                                  >
                                    {lesson.title}
                                  </Typography>
                                }
                                secondary={
                                  <Typography 
                                    variant="body2" 
                                    color={isUnlocked ? 'text.secondary' : 'text.disabled'}
                                    sx={{ mt: 0.5 }}
                                  >
                                    {lesson.summary}
                                  </Typography>
                                }
                              />
                              
                              <Button
                                variant="contained"
                                size="small"
                                disabled={!isUnlocked}
                                sx={{
                                  ml: 2,
                                  minWidth: 80,
                                  backgroundColor: isUnlocked ? 'primary.main' : 'grey.300',
                                  '&:hover': {
                                    backgroundColor: isUnlocked ? 'primary.dark' : 'grey.300'
                                  }
                                }}
                              >
                                {loadingLesson === lesson.title ? (
                                  <CircularProgress size={16} color="inherit" />
                                ) : (
                                  'Read'
                                )}
                              </Button>
                            </Box>
                          </ListItemButton>
                        </ListItem>
                        
                        {lessonIndex < module.lessons.length - 1 && (
                          <Divider variant="inset" component="li" sx={{ ml: 4 }} />
                        )}
                      </React.Fragment>
                    ))}
                  </List>
                </Collapse>
              </CardContent>
            </Card>
          );
        })}
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="text"
          color="primary"
          onClick={onBack}
        >
          Previous
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={onNext}
        >
          Next Page
        </Button>
      </Box>

      <LessonModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        lesson={selectedLesson}
        courseId={courseData.courseId}
      />
      
      <QuizModal
        open={quizModalOpen && !isGeneratingQuiz && currentQuiz !== null}
        onClose={() => {
          setQuizModalOpen(false);
          setCurrentQuizModule(null);
          setCurrentQuiz(null);
        }}
        quiz={currentQuiz}
        moduleTitle={currentQuizModule?.title || 'Module'}
        onQuizComplete={handleQuizComplete}
      />

      {/* Loading overlay for quiz generation */}
      <Dialog open={isGeneratingQuiz} maxWidth="sm">
        <DialogContent sx={{ textAlign: 'center', py: 4 }}>
          <CircularProgress size={60} sx={{ mb: 2 }} />
          <Typography variant="h6">Generating Quiz...</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Creating personalized quiz for {currentQuizModule?.title}
          </Typography>
        </DialogContent>
      </Dialog>
    </Paper>
  );
}
