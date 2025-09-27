import React, { useState } from 'react';
import { Box, Button, Typography, Paper, CircularProgress, Alert, Snackbar } from '@mui/material';
import { Download, Slideshow } from '@mui/icons-material';
import axios from 'axios';

import { CourseStepProps, Module, Lesson } from '../types';

interface CourseOutcomeProps extends Omit<CourseStepProps, 'setCourseData'> {
  onBack: () => void; // Make onBack required for this component
}

export default function CourseOutcome({ onBack, courseData }: CourseOutcomeProps) {
  const [isGeneratingPPT, setIsGeneratingPPT] = useState(false);
  const [pptError, setPptError] = useState<string | null>(null);
  const [pptSuccess, setPptSuccess] = useState<string | null>(null);

  const handleGeneratePowerPoint = async () => {
    if (!courseData.generatedCourse) {
      setPptError('No course data available for PowerPoint generation');
      return;
    }

    setIsGeneratingPPT(true);
    setPptError(null);
    setPptSuccess(null);

    try {
      const response = await axios.post('http://localhost:5000/generate-pptx', {
        courseData: courseData
      });

      if (response.data.success) {
        setPptSuccess('PowerPoint generated successfully!');
        // Trigger download
        const downloadUrl = `http://localhost:5000${response.data.download_url}`;
        window.open(downloadUrl, '_blank');
      } else {
        setPptError('Failed to generate PowerPoint');
      }
    } catch (error) {
      console.error('PowerPoint generation error:', error);
      setPptError('Failed to generate PowerPoint. Please try again.');
    } finally {
      setIsGeneratingPPT(false);
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Generated Course
      </Typography>
      
      {courseData.generatedCourse ? (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h5" gutterBottom>
            {courseData.generatedCourse.course}
          </Typography>
          
          {courseData.generatedCourse.modules.map((module: Module, moduleIndex: number) => (
            <Box key={moduleIndex} sx={{ mb: 4 }}>
              <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
                Module {moduleIndex + 1}: {module.title}
              </Typography>
              
              {module.lessons.map((lesson: Lesson, lessonIndex: number) => (
                <Box key={lessonIndex} sx={{ ml: 2, mb: 2 }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                    Lesson {lessonIndex + 1}: {lesson.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {lesson.summary}
                  </Typography>
                  <Typography variant="body1">
                    {lesson.detail}
                  </Typography>
                </Box>
              ))}
            </Box>
          ))}
        </Box>
      ) : (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      )}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="text"
          color="primary"
          onClick={onBack}
        >
          Previous
        </Button>
        
        {courseData.generatedCourse && (
          <Button
            variant="contained"
            color="secondary"
            startIcon={isGeneratingPPT ? <CircularProgress size={20} /> : <Slideshow />}
            onClick={handleGeneratePowerPoint}
            disabled={isGeneratingPPT}
            sx={{ ml: 2 }}
          >
            {isGeneratingPPT ? 'Generating...' : 'Export to PowerPoint'}
          </Button>
        )}
      </Box>

      {/* Success/Error Messages */}
      <Snackbar 
        open={!!pptSuccess} 
        autoHideDuration={6000} 
        onClose={() => setPptSuccess(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setPptSuccess(null)} severity="success">
          {pptSuccess}
        </Alert>
      </Snackbar>

      <Snackbar 
        open={!!pptError} 
        autoHideDuration={6000} 
        onClose={() => setPptError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setPptError(null)} severity="error">
          {pptError}
        </Alert>
      </Snackbar>
    </Paper>
  );
}