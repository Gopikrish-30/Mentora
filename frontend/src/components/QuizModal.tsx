import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  LinearProgress,
  Card,
  CardContent,
  CardHeader,
  Chip,
  IconButton,
  Grid,
  Alert
} from '@mui/material';
import {
  Close,
  CheckCircle,
  RadioButtonChecked,
  RadioButtonUnchecked,
  Timer,
  ArrowBack,
  ArrowForward,
  EmojiEvents,
  TrendingUp,
  Assessment
} from '@mui/icons-material';
import { Quiz } from '../types/quiz';

interface QuizModalProps {
  open: boolean;
  onClose: () => void;
  quiz: Quiz | null;
  moduleTitle: string;
  onQuizComplete?: () => void;
}

interface QuizResult {
  score: number;
  totalQuestions: number;
  answers: { [questionId: number]: number };
  timeSpent: number;
}

export default function QuizModal({ open, onClose, quiz, moduleTitle, onQuizComplete }: QuizModalProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [questionId: number]: number }>({});
  const [showResults, setShowResults] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [startTime] = useState(Date.now());
  const [showFeedback, setShowFeedback] = useState(false);
  const [questionAnswered, setQuestionAnswered] = useState(false);

  useEffect(() => {
    if (!showResults) {
      const timer = setInterval(() => {
        setTimeSpent(Math.floor((Date.now() - startTime) / 1000));
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [startTime, showResults]);

  useEffect(() => {
    // Reset state when modal opens/closes
    if (open) {
      setCurrentQuestionIndex(0);
      setSelectedAnswers({});
      setShowResults(false);
      setTimeSpent(0);
      setShowFeedback(false);
      setQuestionAnswered(false);
    }
  }, [open]);

  if (!quiz) return null;

  const currentQuestion = quiz.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / quiz.questions.length) * 100;
  const selectedAnswer = selectedAnswers[currentQuestion.id];
  const isCorrect = selectedAnswer === currentQuestion.correctAnswer;

  const handleAnswerSelect = (answerIndex: number) => {
    if (questionAnswered) return;
    
    setSelectedAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: answerIndex
    }));
    setQuestionAnswered(true);
    setShowFeedback(true);
  };

  const handleNext = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setShowFeedback(false);
      setQuestionAnswered(false);
    } else {
      handleFinishQuiz();
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setShowFeedback(!!selectedAnswers[quiz.questions[currentQuestionIndex - 1].id]);
      setQuestionAnswered(!!selectedAnswers[quiz.questions[currentQuestionIndex - 1].id]);
    }
  };

  const handleFinishQuiz = () => {
    const finalTime = Math.floor((Date.now() - startTime) / 1000);
    setTimeSpent(finalTime);
    setShowResults(true);
    
    // Call the completion callback when quiz is finished
    if (onQuizComplete) {
      onQuizComplete();
    }
  };

  const calculateScore = (): QuizResult => {
    let correctAnswers = 0;
    quiz.questions.forEach(question => {
      if (selectedAnswers[question.id] === question.correctAnswer) {
        correctAnswers++;
      }
    });

    return {
      score: correctAnswers,
      totalQuestions: quiz.questions.length,
      answers: selectedAnswers,
      timeSpent
    };
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getGradeInfo = (percentage: number) => {
    if (percentage >= 90) return {
      grade: 'A+',
      color: 'success',
      message: 'Outstanding Performance',
      description: 'You have mastered this topic.'
    };
    if (percentage >= 80) return {
      grade: 'A',
      color: 'success',
      message: 'Excellent Work',
      description: 'You have a strong understanding of the material.'
    };
    if (percentage >= 70) return {
      grade: 'B',
      color: 'primary',
      message: 'Good Performance',
      description: 'You have a solid grasp of the concepts.'
    };
    if (percentage >= 60) return {
      grade: 'C',
      color: 'warning',
      message: 'Fair Performance',
      description: 'Consider reviewing the material for better understanding.'
    };
    return {
      grade: 'D',
      color: 'error',
      message: 'Needs Improvement',
      description: 'Review the material and try again to improve your score.'
    };
  };

  if (showResults) {
    const result = calculateScore();
    const percentage = Math.round((result.score / result.totalQuestions) * 100);
    const gradeInfo = getGradeInfo(percentage);

    return (
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <EmojiEvents color="primary" />
            <Typography variant="h6">Quiz Results - {moduleTitle}</Typography>
            <IconButton onClick={onClose} sx={{ ml: 'auto' }}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h3" color={gradeInfo.color} gutterBottom>
              {gradeInfo.grade}
            </Typography>
            <Typography variant="h4" gutterBottom>
              {result.score}/{result.totalQuestions} Correct
            </Typography>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              {gradeInfo.message}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {gradeInfo.description}
            </Typography>
          </Box>

          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Assessment color="primary" />
                  <Typography variant="h6">{percentage}%</Typography>
                  <Typography variant="body2" color="text.secondary">Accuracy</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <CheckCircle color="success" />
                  <Typography variant="h6">{result.score}</Typography>
                  <Typography variant="body2" color="text.secondary">Correct</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Timer color="primary" />
                  <Typography variant="h6">{formatTime(result.timeSpent)}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Time</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <TrendingUp color="primary" />
                  <Typography variant="h6">{Math.round(result.timeSpent / result.totalQuestions)}s</Typography>
                  <Typography variant="body2" color="text.secondary">Avg/Question</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Typography variant="h6" gutterBottom>Detailed Review</Typography>
          {quiz.questions.map((question, index) => {
            const userAnswer = result.answers[question.id];
            const isCorrect = userAnswer === question.correctAnswer;

            return (
              <Card key={question.id} sx={{ mb: 2, borderColor: isCorrect ? 'success.main' : 'error.main' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    {isCorrect ? (
                      <CheckCircle color="success" sx={{ mt: 0.5 }} />
                    ) : (
                      <Close color="error" sx={{ mt: 0.5 }} />
                    )}
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {index + 1}. {question.question}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
                        <Chip 
                          label={`Your Answer: ${userAnswer !== undefined ? String.fromCharCode(65 + userAnswer) : 'Not answered'}`}
                          color={isCorrect ? 'success' : 'error'}
                          size="small"
                        />
                        {!isCorrect && (
                          <Chip 
                            label={`Correct: ${String.fromCharCode(65 + question.correctAnswer)}`}
                            color="success"
                            size="small"
                          />
                        )}
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary">
                        {question.explanation}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            );
          })}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={onClose} variant="contained">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="h6">{moduleTitle} Quiz</Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Timer fontSize="small" />
              <Typography variant="body2">{formatTime(timeSpent)}</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              {Object.keys(selectedAnswers).length}/{quiz.questions.length} answered
            </Typography>
            <IconButton onClick={onClose}>
              <Close />
            </IconButton>
          </Box>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        <Box sx={{ mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Question {currentQuestionIndex + 1} of {quiz.questions.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {Math.round(progress)}% Complete
            </Typography>
          </Box>
          <LinearProgress variant="determinate" value={progress} />
        </Box>

        <Card>
          <CardHeader title={currentQuestion.question} />
          <CardContent>
            <Box sx={{ mb: 3 }}>
              {currentQuestion.options.map((option, index) => {
                const isSelected = selectedAnswer === index;
                const isCorrectAnswer = index === currentQuestion.correctAnswer;
                
                let optionColor = 'default';
                if (showFeedback) {
                  if (isSelected && isCorrect) optionColor = 'success';
                  else if (isSelected && !isCorrect) optionColor = 'error';
                  else if (isCorrectAnswer) optionColor = 'success';
                } else if (isSelected) {
                  optionColor = 'primary';
                }

                return (
                  <Box
                    key={index}
                    onClick={() => handleAnswerSelect(index)}
                    sx={{
                      p: 2,
                      mb: 1,
                      border: 1,
                      borderColor: optionColor === 'error' ? 'error.main' : 
                                   optionColor === 'success' ? 'success.main' : 
                                   optionColor === 'primary' ? 'primary.main' : 'grey.300',
                      borderRadius: 1,
                      cursor: questionAnswered ? 'default' : 'pointer',
                      backgroundColor: optionColor === 'error' ? 'error.50' : 
                                      optionColor === 'success' ? 'success.50' : 
                                      optionColor === 'primary' ? 'primary.50' : 'background.paper',
                      '&:hover': {
                        backgroundColor: questionAnswered ? undefined : 'action.hover'
                      }
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      {isSelected ? (
                        <RadioButtonChecked color={optionColor as any} />
                      ) : (
                        <RadioButtonUnchecked color={optionColor as any} />
                      )}
                      <Typography>
                        {String.fromCharCode(65 + index)}. {option}
                      </Typography>
                    </Box>
                  </Box>
                );
              })}
            </Box>

            {showFeedback && (
              <Alert 
                severity={isCorrect ? 'success' : 'error'}
                sx={{ mb: 2 }}
              >
                <Typography variant="subtitle2" gutterBottom>
                  {isCorrect ? 'Correct!' : 'Incorrect'}
                </Typography>
                <Typography variant="body2">
                  {currentQuestion.explanation}
                </Typography>
                {!isCorrect && (
                  <Typography variant="body2" sx={{ mt: 1, fontWeight: 'bold' }}>
                    Correct answer: {String.fromCharCode(65 + currentQuestion.correctAnswer)}. {currentQuestion.options[currentQuestion.correctAnswer]}
                  </Typography>
                )}
              </Alert>
            )}

            <Box sx={{ display: 'flex', justifyContent: 'space-between', pt: 2 }}>
              <Button
                variant="outlined"
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
                startIcon={<ArrowBack />}
              >
                Previous
              </Button>

              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!questionAnswered}
                endIcon={<ArrowForward />}
              >
                {currentQuestionIndex === quiz.questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </DialogContent>
    </Dialog>
  );
}