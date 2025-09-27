import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Menu,
  MenuItem,
  Tooltip
} from '@mui/material';
import {
  Edit,
  Delete,
  ExpandMore,
  CheckCircle,
  Cancel,
  MoreVert,
  Visibility,
  School,
  Quiz,
  Description,
  Slideshow
} from '@mui/icons-material';
import { CourseStepProps, Module, Lesson, CourseData } from '../types';

interface ExamineProps extends CourseStepProps {}

interface ModificationDialogProps {
  open: boolean;
  onClose: () => void;
  onModify: (prompt: string) => void;
  contentType: string;
  contentTitle: string;
  loading?: boolean;
}

const ModificationDialog: React.FC<ModificationDialogProps> = ({
  open,
  onClose,
  onModify,
  contentType,
  contentTitle,
  loading = false
}) => {
  const [modificationPrompt, setModificationPrompt] = useState('');

  const handleSubmit = () => {
    if (modificationPrompt.trim()) {
      onModify(modificationPrompt);
      setModificationPrompt('');
    }
  };

  const handleClose = () => {
    setModificationPrompt('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        Modify {contentType}: {contentTitle}
      </DialogTitle>
      <DialogContent>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Describe what changes you want to make to this {contentType.toLowerCase()}. 
          Be specific about the modifications needed.
        </Typography>
        <TextField
          fullWidth
          multiline
          rows={6}
          value={modificationPrompt}
          onChange={(e) => setModificationPrompt(e.target.value)}
          placeholder={`Example: "Make the content more beginner-friendly by adding more examples and simplifying the language" or "Add a section about common mistakes and how to avoid them"`}
          variant="outlined"
          disabled={loading}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={loading || !modificationPrompt.trim()}
          startIcon={loading ? <CircularProgress size={16} /> : <Edit />}
        >
          {loading ? 'Modifying...' : 'Modify Content'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

interface DeleteDialogProps {
  open: boolean;
  onClose: () => void;
  onDelete: () => void;
  contentType: string;
  contentTitle: string;
  loading?: boolean;
}

const DeleteDialog: React.FC<DeleteDialogProps> = ({
  open,
  onClose,
  onDelete,
  contentType,
  contentTitle,
  loading = false
}) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Delete {contentType}</DialogTitle>
      <DialogContent>
        <Alert severity="warning" sx={{ mb: 2 }}>
          This action cannot be undone. Are you sure you want to delete this {contentType.toLowerCase()}?
        </Alert>
        <Typography variant="body1">
          <strong>{contentTitle}</strong> will be permanently removed.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          onClick={onDelete}
          color="error"
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={16} /> : <Delete />}
        >
          {loading ? 'Deleting...' : 'Delete'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default function Examine({ onNext, onBack, courseData, setCourseData }: ExamineProps) {
  const [modificationDialog, setModificationDialog] = useState<{
    open: boolean;
    contentType: string;
    contentId: string;
    contentTitle: string;
    content: any;
  }>({
    open: false,
    contentType: '',
    contentId: '',
    contentTitle: '',
    content: null
  });

  const [deleteDialog, setDeleteDialog] = useState<{
    open: boolean;
    contentType: string;
    contentId: string;
    contentTitle: string;
  }>({
    open: false,
    contentType: '',
    contentId: '',
    contentTitle: ''
  });

  const [loading, setLoading] = useState<{ [key: string]: boolean }>({});
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const course = courseData.generatedCourse;

  const handleModifyClick = (contentType: string, contentId: string, contentTitle: string, content: any) => {
    setModificationDialog({
      open: true,
      contentType,
      contentId,
      contentTitle,
      content
    });
  };

  const handleDeleteClick = (contentType: string, contentId: string, contentTitle: string) => {
    setDeleteDialog({
      open: true,
      contentType,
      contentId,
      contentTitle
    });
  };

  const handleDelete = async () => {
    const { contentType, contentId } = deleteDialog;
    const loadingKey = `delete_${contentType}_${contentId}`;
    
    setLoading(prev => ({ ...prev, [loadingKey]: true }));
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('http://localhost:5000/delete-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_type: contentType,
          content_id: contentId
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to delete content');
      }

      // Update the course data to remove deleted content
      if (contentType === 'course') {
        setCourseData({
          ...courseData,
          generatedCourse: null
        });
      } else if (contentType === 'module' && course) {
        const updatedCourse = { ...course };
        if (updatedCourse.modules) {
          updatedCourse.modules = updatedCourse.modules.filter((m: Module) => m.title !== contentId);
          setCourseData({
            ...courseData,
            generatedCourse: updatedCourse
          });
        }
      }

      setSuccess(`${contentType} deleted successfully!`);
      setDeleteDialog({ open: false, contentType: '', contentId: '', contentTitle: '' });
      
    } catch (error) {
      console.error('Error deleting content:', error);
      setError('Failed to delete content. Please try again.');
    } finally {
      setLoading(prev => ({ ...prev, [loadingKey]: false }));
    }
  };

  const handleModify = async (modificationPrompt: string) => {
    const { contentType, contentId, content } = modificationDialog;
    const loadingKey = `modify_${contentType}_${contentId}`;
    
    setLoading(prev => ({ ...prev, [loadingKey]: true }));
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('http://localhost:5000/modify-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_type: contentType,
          content_id: contentId,
          modification_prompt: modificationPrompt,
          original_content: content
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to modify content');
      }

      const data = await response.json();
      
      // Update the course data with modified content
      if (contentType === 'course') {
        setCourseData({
          ...courseData,
          generatedCourse: data.modified_content
        });
      } else if (contentType === 'module' && course) {
        // Update specific module in course
        const updatedCourse = { ...course };
        if (updatedCourse.modules) {
          const moduleIndex = updatedCourse.modules.findIndex((m: Module) => m.title === contentId);
          if (moduleIndex !== -1) {
            updatedCourse.modules[moduleIndex] = data.modified_content;
            setCourseData({
              ...courseData,
              generatedCourse: updatedCourse
            });
          }
        }
      } else if (contentType === 'lesson' && course) {
        // Update specific lesson in module
        const updatedCourse = { ...course };
        // Find and update the lesson (implementation depends on your data structure)
        setCourseData({
          ...courseData,
          generatedCourse: updatedCourse
        });
      }

      setSuccess(`${contentType} modified successfully!`);
      setModificationDialog({ open: false, contentType: '', contentId: '', contentTitle: '', content: null });
      
    } catch (error) {
      console.error('Error modifying content:', error);
      setError('Failed to modify content. Please try again.');
    } finally {
      setLoading(prev => ({ ...prev, [loadingKey]: false }));
    }
  };

  if (!course && courseData.exportType !== 'PowerPoint' && courseData.exportType !== 'PDF') {
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

  // Handle PowerPoint and PDF content examination
  if (courseData.exportType === 'PowerPoint' || courseData.exportType === 'PDF') {
    return (
      <Paper elevation={0} sx={{ p: 4, maxWidth: '1000px', mx: 'auto' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
          <Edit sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
          <Box>
            <Typography variant="h4" component="h1">
              Trainer Review & Approval
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Review and approve {courseData.exportType} content before finalizing
            </Typography>
          </Box>
        </Box>

        <Alert severity="info" sx={{ mb: 3 }}>
          {courseData.exportType} content has been generated and is ready for review. 
          The content will be available for download in the next step.
        </Alert>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                {courseData.exportType === 'PowerPoint' ? 
                  <Slideshow sx={{ fontSize: 20, mr: 2 }} /> : 
                  <Description sx={{ fontSize: 20, mr: 2 }} />
                }
                <Box>
                  <Typography variant="h6" component="h2">
                    {courseData.exportType} Document
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Generated from uploaded content
                  </Typography>
                </Box>
              </Box>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={() => handleDeleteClick('document', 'generated_document', `${courseData.exportType} Document`)}
              >
                Delete Document
              </Button>
            </Box>
          </CardContent>
        </Card>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            variant="text"
            color="primary"
            onClick={onBack}
          >
            Back
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={onNext}
            startIcon={<CheckCircle />}
          >
            Approve & Continue
          </Button>
        </Box>

        {/* Delete Dialog */}
        <DeleteDialog
          open={deleteDialog.open}
          onClose={() => setDeleteDialog({ open: false, contentType: '', contentId: '', contentTitle: '' })}
          onDelete={handleDelete}
          contentType={deleteDialog.contentType}
          contentTitle={deleteDialog.contentTitle}
          loading={loading[`delete_${deleteDialog.contentType}_${deleteDialog.contentId}`]}
        />
      </Paper>
    );
  }

  const getContentIcon = (type: string) => {
    switch (type) {
      case 'course':
        return <School sx={{ fontSize: 20 }} />;
      case 'module':
        return <Description sx={{ fontSize: 20 }} />;
      case 'lesson':
        return <Quiz sx={{ fontSize: 20 }} />;
      case 'slide':
        return <Slideshow sx={{ fontSize: 20 }} />;
      default:
        return <Visibility sx={{ fontSize: 20 }} />;
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 4, maxWidth: '1200px', mx: 'auto' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Edit sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
        <Box>
          <Typography variant="h4" component="h1">
            Trainer Review & Approval
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Review, modify, or delete AI-generated content before finalizing
          </Typography>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Course Overview */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {getContentIcon('course')}
              <Box sx={{ ml: 2 }}>
                <Typography variant="h6" component="h2">
                  {course?.course || 'Untitled Course'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {course?.modules?.length || 0} modules • {course?.modules?.reduce((total: number, module: Module) => total + module.lessons.length, 0) || 0} lessons
                </Typography>
              </Box>
            </Box>
            <Box>
              <Button
                variant="outlined"
                startIcon={<Edit />}
                onClick={() => handleModifyClick('course', course?.course || 'course', course?.course || 'course', course)}
                sx={{ mr: 1 }}
              >
                Modify Course
              </Button>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={() => handleDeleteClick('course', course?.course || 'course', course?.course || 'course')}
              >
                Delete Course
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Modules */}
      <Typography variant="h5" sx={{ mb: 2 }}>
        Modules & Lessons
      </Typography>

      {course?.modules?.map((module: Module, moduleIndex: number) => (
        <Accordion key={moduleIndex} sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
                {getContentIcon('module')}
                <Box sx={{ ml: 2 }}>
                  <Typography variant="h6">
                    Module {moduleIndex + 1}: {module.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {module.lessons.length} lessons
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ mr: 2 }}>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<Edit />}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleModifyClick('module', module.title, module.title, module);
                  }}
                  sx={{ mr: 1 }}
                >
                  Modify
                </Button>
                <Button
                  variant="outlined"
                  size="small"
                  color="error"
                  startIcon={<Delete />}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteClick('module', module.title, module.title);
                  }}
                >
                  Delete
                </Button>
              </Box>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <List>
              {module.lessons.map((lesson: Lesson, lessonIndex: number) => (
                <ListItem key={lessonIndex} divider>
                  <ListItemText
                    primary={
                      <Typography variant="subtitle1">
                        {lesson.title}
                      </Typography>
                    }
                    secondary={
                      <Typography variant="body2" color="text.secondary">
                        {lesson.summary}
                      </Typography>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Edit />}
                      onClick={() => handleModifyClick('lesson', lesson.title, lesson.title, lesson)}
                      sx={{ mr: 1 }}
                    >
                      Modify
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      color="error"
                      startIcon={<Delete />}
                      onClick={() => handleDeleteClick('lesson', lesson.title, lesson.title)}
                    >
                      Delete
                    </Button>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="text"
          color="primary"
          onClick={onBack}
        >
          Back to Learning Path
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={onNext}
          startIcon={<CheckCircle />}
        >
          Approve & Continue
        </Button>
      </Box>

      {/* Modification Dialog */}
      <ModificationDialog
        open={modificationDialog.open}
        onClose={() => setModificationDialog({ open: false, contentType: '', contentId: '', contentTitle: '', content: null })}
        onModify={handleModify}
        contentType={modificationDialog.contentType}
        contentTitle={modificationDialog.contentTitle}
        loading={loading[`modify_${modificationDialog.contentType}_${modificationDialog.contentId}`]}
      />

      {/* Delete Dialog */}
      <DeleteDialog
        open={deleteDialog.open}
        onClose={() => setDeleteDialog({ open: false, contentType: '', contentId: '', contentTitle: '' })}
        onDelete={handleDelete}
        contentType={deleteDialog.contentType}
        contentTitle={deleteDialog.contentTitle}
        loading={loading[`delete_${deleteDialog.contentType}_${deleteDialog.contentId}`]}
      />
    </Paper>
  );
}
