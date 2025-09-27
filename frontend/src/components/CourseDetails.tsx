import React from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';

import { CourseStepProps, exportTypes, ExportType } from '../types';

interface CourseDetailsProps extends CourseStepProps {
  onNext: () => void; // Make onNext required for this component
  onBack: () => void; // Make onBack required for this component
}

export const difficultyLevels = [
  'Beginner',
  'Intermediate',
  'Advanced',
  'Expert'
] as const;

export const languages = [
  'English',
  'Spanish',
  'French',
  'German',
  'Chinese',
  'Japanese'
] as const;

export type DifficultyLevel = typeof difficultyLevels[number];
export type Language = typeof languages[number];

// Using the constants defined above

export default function CourseDetails({
  onNext,
  onBack,
  courseData,
  setCourseData,
}: CourseDetailsProps) {
  const handleChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setCourseData({
      ...courseData,
      courseDetails: {
        ...courseData.courseDetails,
        [field]: event.target.value
      }
    });
  };

  const handleExportTypeChange = (event: any) => {
    setCourseData({
      ...courseData,
      exportType: event.target.value as ExportType
    });
  };

  const isFormValid = () => {
    const { title, creatorName, difficulty, language, targetAudience } = courseData.courseDetails;
    return title && creatorName && difficulty && language && targetAudience;
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Course Details
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
        Define your course information and target learners
      </Typography>

      <Box sx={{ display: 'grid', gap: 3 }}>
        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
          <TextField
            required
            label="Course Title"
            value={courseData.courseDetails.title}
            onChange={handleChange('title')}
            fullWidth
          />
          <TextField
            required
            label="Creator Name"
            value={courseData.courseDetails.creatorName}
            onChange={handleChange('creatorName')}
            fullWidth
          />
        </Box>

        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
          <TextField
            required
            select
            label="Difficulty Level"
            value={courseData.courseDetails.difficulty}
            onChange={handleChange('difficulty')}
            fullWidth
          >
            {difficultyLevels.map((level) => (
              <MenuItem key={level} value={level}>
                {level}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            required
            select
            label="Language"
            value={courseData.courseDetails.language}
            onChange={handleChange('language')}
            fullWidth
          >
            {languages.map((lang) => (
              <MenuItem key={lang} value={lang}>
                {lang}
              </MenuItem>
            ))}
          </TextField>
        </Box>

        <TextField
          label="Course Prerequisites"
          multiline
          rows={3}
          value={courseData.courseDetails.prerequisites}
          onChange={handleChange('prerequisites')}
          placeholder="e.g., Basic understanding of business principles. No prior experience required"
          fullWidth
          helperText={`${courseData.courseDetails.prerequisites.length}/500`}
        />

        <TextField
          required
          label="Target Audience"
          multiline
          rows={3}
          value={courseData.courseDetails.targetAudience}
          onChange={handleChange('targetAudience')}
          fullWidth
          helperText={`${courseData.courseDetails.targetAudience.length}/500`}
        />

        <FormControl fullWidth required>
          <InputLabel>Export Type</InputLabel>
          <Select
            value={courseData.exportType || 'Course'}
            onChange={handleExportTypeChange}
            label="Export Type"
          >
            {exportTypes.map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
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
          disabled={!isFormValid()}
        >
          {courseData.exportType === 'PowerPoint' ? 'Generate PowerPoint' : 
           courseData.exportType === 'PDF' ? 'Generate PDF' : 'Generate Course'}
        </Button>
      </Box>
    </Paper>
  );
}