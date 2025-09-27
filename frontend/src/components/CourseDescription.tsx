import React from 'react';
import { Box, Button, TextField, Typography, Paper } from '@mui/material';

import { CourseStepProps } from '../types';

interface CourseDescriptionProps extends CourseStepProps {
  onNext: () => void; // Make onNext required for this component
}

export default function CourseDescription({ onNext, courseData, setCourseData }: CourseDescriptionProps) {
  const handleDescriptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCourseData({
      ...courseData,
      description: event.target.value
    });
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Describe your course
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
        Provide a detailed description of what you want to teach
      </Typography>
      
      <TextField
        fullWidth
        multiline
        rows={8}
        placeholder="e.g., Selling residential real estate in Australia"
        value={courseData.description}
        onChange={handleDescriptionChange}
        variant="outlined"
        sx={{ mb: 2 }}
        helperText={`${courseData.description.length}/1000`}
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="text"
          color="primary"
          sx={{ visibility: 'hidden' }}
        >
          Previous
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={onNext}
          disabled={!courseData.description.trim()}
        >
          Next
        </Button>
      </Box>
    </Paper>
  );
}