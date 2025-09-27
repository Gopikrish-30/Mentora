import React, { useCallback, useState } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  Paper, 
  Tab, 
  Tabs,
  CircularProgress,
  Alert,
  Snackbar,
  TextField
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

import { CourseData, CourseStepProps } from '../types';

interface CourseUploadProps extends CourseStepProps {}

export default function CourseUpload({ onNext, onBack, courseData, setCourseData }: CourseUploadProps) {
  const [uploadType, setUploadType] = useState('files');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [websiteUrl, setWebsiteUrl] = useState('');

  const handleUpload = async () => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    
    try {
      if (uploadType === 'files' && courseData.uploadedFiles.length > 0) {
        const file = courseData.uploadedFiles[0];
        formData.append('file', file);
      } else if (uploadType === 'websites' && websiteUrl) {
        formData.append('url', websiteUrl);
      } else {
        throw new Error('No file or URL provided');
      }

      formData.append('prompt', courseData.description || '');

      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
        maxContentLength: 50 * 1024 * 1024, // 50MB max file size
      });

      // Store the course ID and extracted text in courseData
      setCourseData({
        ...courseData,
        courseId: response.data.course_id,
        extractedText: response.data.extracted_text,
        generatedCourse: response.data.course
      });

      if (onNext) onNext();
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.error || err.message;
        setError(`Upload failed: ${errorMessage}`);
      } else {
        setError('Failed to process content. Please try again.');
      }
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setCourseData({
      ...courseData,
      uploadedFiles: acceptedFiles
    });
    setError(null);
  }, [courseData, setCourseData]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/csv': ['.csv']
    }
  });

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        What course will you box?
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
        Optional: Train AI on existing content
      </Typography>

      <Tabs
        value={uploadType}
        onChange={(_, newValue) => setUploadType(newValue)}
        centered
        sx={{ mb: 4 }}
      >
        <Tab label="Files" value="files" />
        <Tab label="Websites" value="websites" />
      </Tabs>

      {uploadType === 'files' && (
        <Box
          {...getRootProps()}
          sx={{
            border: '2px dashed',
            borderColor: isDragActive ? 'primary.main' : 'grey.300',
            borderRadius: 2,
            p: 4,
            textAlign: 'center',
            cursor: 'pointer',
            bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          }}
        >
          <input {...getInputProps()} />
          <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography>
            Drag & Drop or Browse to upload
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Supported File Types: .pdf, .txt, .docx, .csv
          </Typography>
          
          {courseData.uploadedFiles.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" color="primary">
                {courseData.uploadedFiles.length} file(s) selected
              </Typography>
            </Box>
          )}
        </Box>
      )}

      {uploadType === 'websites' && (
        <Box sx={{ p: 4 }}>
          <TextField
            fullWidth
            label="Enter Website URL"
            value={websiteUrl}
            onChange={(e) => setWebsiteUrl(e.target.value)}
            placeholder="https://example.com"
            sx={{ mb: 2 }}
          />
          <Typography variant="caption" color="text.secondary">
            Enter a valid URL to extract content from a website
          </Typography>
        </Box>
      )}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="text"
          color="primary"
          onClick={onBack}
          disabled={loading}
        >
          Previous
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          disabled={loading || (uploadType === 'files' && courseData.uploadedFiles.length === 0) || 
                   (uploadType === 'websites' && !websiteUrl)}
        >
          {loading ? (
            <>
              <CircularProgress size={20} color="inherit" sx={{ mr: 1 }} />
              Processing...
            </>
          ) : 'Next'}
        </Button>
      </Box>

      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert onClose={() => setError(null)} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </Paper>
  );
}