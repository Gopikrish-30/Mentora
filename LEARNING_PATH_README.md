# Learning Path Feature

## Overview

The Learning Path feature provides a comprehensive, structured course experience with detailed modules and lessons. It integrates with ChromaDB for RAG (Retrieval-Augmented Generation) to provide in-depth, context-aware lesson content.

## Features

### 1. Enhanced Course Generation
- **Powerful System Prompt**: Updated Gemini API prompt for generating comprehensive course content
- **Detailed Lessons**: Each lesson contains 400-600 words of educational content
- **Structured Modules**: Logical progression with 3-6 lessons per module

### 2. Learning Path UI
- **Module Cards**: Visual representation of course modules with status indicators
- **Progress Tracking**: Active, unlocked, and locked module states
- **Expandable Lessons**: Click to expand and view lesson details
- **Responsive Design**: Clean, modern interface similar to the provided images

### 3. RAG Integration
- **Context-Aware Content**: Lessons are generated using relevant content from ChromaDB
- **Detailed Explanations**: Comprehensive lesson content with definitions, examples, and applications
- **Real-time Generation**: Content is generated on-demand when users click "Read"

## Components

### LearningPath.tsx
Main component that displays the course structure with:
- Module cards with status indicators
- Expandable lesson lists
- Progress tracking
- Integration with lesson modal

### LessonModal.tsx
Modal component for displaying detailed lesson content:
- RAG-powered content generation
- Rich text formatting
- Loading states and error handling
- Responsive design

### Backend Endpoints

#### `/lesson-content` (POST)
Generates detailed lesson content using RAG:
```json
{
  "lesson_title": "Introduction to Machine Learning",
  "lesson_summary": "Basic concepts and definitions",
  "course_id": "course-uuid"
}
```

Response:
```json
{
  "lesson_title": "Introduction to Machine Learning",
  "content": "Detailed lesson content...",
  "context_sources": 5
}
```

## Setup Instructions

### 1. Configure API Key
```bash
cd code_o_clock/course-creator
python setup_api_key.py
```

### 2. Test API Integration
```bash
python test_gemini_api.py
```

### 3. Start the Application
```bash
# Backend
python app.py

# Frontend (in another terminal)
cd frontend
npm start
```

## Usage Flow

1. **Course Creation**: User uploads content and generates course structure
2. **Learning Path**: User views structured modules and lessons
3. **Lesson Reading**: User clicks "Read" to generate detailed content via RAG
4. **Progress Tracking**: System tracks module completion and unlocks next modules

## Technical Details

### System Prompt Enhancement
The updated system prompt ensures:
- Comprehensive lesson content (400-600 words)
- Clear definitions and examples
- Real-world applications
- Common misconceptions addressed
- Actionable insights

### RAG Implementation
- Uses ChromaDB for semantic search
- Combines multiple relevant chunks for context
- Generates detailed, accurate content
- Handles errors gracefully

### UI/UX Features
- Status indicators (Active, Available, Locked)
- Expandable modules and lessons
- Loading states and error handling
- Responsive design
- Clean, modern interface

## File Structure

```
course-creator/
├── app.py                          # Updated with new endpoints
├── llm_processor.py                # Enhanced with new prompt and lesson generation
├── frontend/src/components/
│   ├── LearningPath.tsx            # New learning path component
│   ├── LessonModal.tsx             # New lesson modal component
│   └── CourseStepper.tsx           # Updated to include learning path step
├── setup_api_key.py                # API key setup script
├── test_gemini_api.py              # API testing script
└── LEARNING_PATH_README.md         # This documentation
```

## Future Enhancements

- [ ] User progress persistence
- [ ] Quiz and assessment integration
- [ ] Certificate generation
- [ ] Social learning features
- [ ] Advanced analytics
- [ ] Mobile app support
