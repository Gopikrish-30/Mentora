import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Box } from '@mui/material';
import CourseDescription from './CourseDescription';
import CourseUpload from './CourseUpload';
import CourseDetails from './CourseDetails';
import LearningPath from './LearningPath';
import Examine from './Examine';
import CourseOutcome from './CourseOutcome';
import PDFOutcome from './PDFOutcome';
import { CourseData } from '../types';

const steps = ['Course', 'Upload', 'Learner', 'Learning Path', 'Examine', 'Outcome'];

export default function CourseStepper() {
  const [activeStep, setActiveStep] = useState(0);
  const [courseData, setCourseData] = useState<CourseData>({
    description: '',
    uploadedFiles: [],
    courseId: '',
    extractedText: '',
    generatedCourse: null,
    courseDetails: {
      title: '',
      creatorName: '',
      difficulty: 'Beginner',  // Default value
      language: 'English',    // Default value
      prerequisites: '',
      targetAudience: ''
    },
    exportType: 'Course'  // Default export type
  });

  const handleNext = () => {
    // Skip Learning Path and Examine steps for PowerPoint and PDF exports
    if (activeStep === 2 && (courseData.exportType === 'PowerPoint' || courseData.exportType === 'PDF')) {
      setActiveStep(5); // Jump directly to outcome step (step 5 in the 6-step flow)
    } else {
      setActiveStep((prevStep) => prevStep + 1);
    }
  };

  const handleBack = () => {
    // Handle back navigation for PowerPoint and PDF exports
    if (activeStep === 5 && (courseData.exportType === 'PowerPoint' || courseData.exportType === 'PDF')) {
      setActiveStep(2); // Go back to Course Details step
    } else {
      setActiveStep((prevStep) => prevStep - 1);
    }
  };

  // Get dynamic step labels based on export type
  const getStepLabels = () => {
    if (courseData.exportType === 'PowerPoint' || courseData.exportType === 'PDF') {
      return ['Course', 'Upload', 'Learner', 'Outcome'];
    }
    return ['Course', 'Upload', 'Learner', 'Learning Path', 'Examine', 'Outcome'];
  };

  const getStepContent = (step: number) => {
    // Handle different flows based on export type
    if (courseData.exportType === 'PowerPoint' || courseData.exportType === 'PDF') {
      // 4-step flow: Course, Upload, Learner, Outcome
      switch (step) {
        case 0:
          return <CourseDescription 
                   onNext={handleNext} 
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 1:
          return <CourseUpload 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 2:
          return <CourseDetails 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 3:
          // Outcome step for PowerPoint and PDF
          if (courseData.exportType === 'PowerPoint') {
            return <CourseOutcome 
                     onBack={handleBack}
                     courseData={courseData} 
                   />;
          } else if (courseData.exportType === 'PDF') {
            return <PDFOutcome 
                     onBack={handleBack}
                     courseData={courseData} 
                   />;
          }
          break;
        default:
          return 'Unknown step';
      }
    } else {
      // 6-step flow: Course, Upload, Learner, Learning Path, Examine, Outcome
      switch (step) {
        case 0:
          return <CourseDescription 
                   onNext={handleNext} 
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 1:
          return <CourseUpload 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 2:
          return <CourseDetails 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 3:
          return <LearningPath 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 4:
          return <Examine 
                   onNext={handleNext} 
                   onBack={handleBack}
                   courseData={courseData} 
                   setCourseData={setCourseData} 
                 />;
        case 5:
          return <CourseOutcome 
                   onBack={handleBack}
                   courseData={courseData} 
                 />;
        default:
          return 'Unknown step';
      }
    }
  };

  return (
    <Box sx={{ width: '100%', p: 4 }}>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {getStepLabels().map((label, index) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      {getStepContent(activeStep)}
    </Box>
  );
}