import React, { useState } from 'react';
import { Box, Button, Typography, Paper, CircularProgress, Alert, Snackbar } from '@mui/material';
import { Download, PictureAsPdf } from '@mui/icons-material';
import axios from 'axios';

import { CourseStepProps, Module, Lesson } from '../types';

interface PDFOutcomeProps extends Omit<CourseStepProps, 'setCourseData'> {
  onBack: () => void; // Make onBack required for this component
}

export default function PDFOutcome({ onBack, courseData }: PDFOutcomeProps) {
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);
  const [pdfSuccess, setPdfSuccess] = useState<string | null>(null);

  const handleGeneratePDF = async () => {
    if (!courseData.generatedCourse) {
      setPdfError('No course data available for PDF generation');
      return;
    }

    setIsGeneratingPDF(true);
    setPdfError(null);
    setPdfSuccess(null);

    try {
      const response = await axios.post('http://localhost:5000/generate-pdf', {
        courseData: courseData
      });

      if (response.data.success) {
        setPdfSuccess('PDF generated successfully!');
        // Trigger download
        const downloadUrl = `http://localhost:5000${response.data.download_url}`;
        window.open(downloadUrl, '_blank');
      } else {
        setPdfError('Failed to generate PDF');
      }
    } catch (error) {
      console.error('PDF generation error:', error);
      setPdfError('Failed to generate PDF. Please try again.');
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Generated Course - PDF Export
      </Typography>
      
      {courseData.generatedCourse ? (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h5" gutterBottom>
            {courseData.generatedCourse.course}
          </Typography>
          
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Your course has been generated and is ready for PDF export. Click the button below to generate and download a professional PDF document.
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
            startIcon={isGeneratingPDF ? <CircularProgress size={20} /> : <PictureAsPdf />}
            onClick={handleGeneratePDF}
            disabled={isGeneratingPDF}
            sx={{ ml: 2 }}
          >
            {isGeneratingPDF ? 'Generating...' : 'Export to PDF'}
          </Button>
        )}
      </Box>

      {/* Success/Error Messages */}
      <Snackbar 
        open={!!pdfSuccess} 
        autoHideDuration={6000} 
        onClose={() => setPdfSuccess(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setPdfSuccess(null)} severity="success">
          {pdfSuccess}
        </Alert>
      </Snackbar>

      <Snackbar 
        open={!!pdfError} 
        autoHideDuration={6000} 
        onClose={() => setPdfError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setPdfError(null)} severity="error">
          {pdfError}
        </Alert>
      </Snackbar>
    </Paper>
  );
}
