"""
PDF Generator for Course Content
Generates structured PDF documents from course data
"""

import os
import uuid
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

class PDFGenerator:
    """Generates PDF documents from course content"""
    
    def __init__(self):
        # Create downloads directory if it doesn't exist
        self.download_folder = 'downloads'
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # Define styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#003366'),
            fontName='Helvetica-Bold'
        ))
        
        # Course title style
        self.styles.add(ParagraphStyle(
            name='CourseTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=HexColor('#1976d2'),
            fontName='Helvetica-Bold'
        ))
        
        # Module title style
        self.styles.add(ParagraphStyle(
            name='ModuleTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#1976d2'),
            fontName='Helvetica-Bold'
        ))
        
        # Lesson title style
        self.styles.add(ParagraphStyle(
            name='LessonTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=HexColor('#424242'),
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Summary style
        self.styles.add(ParagraphStyle(
            name='SummaryText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=HexColor('#666666'),
            fontName='Helvetica-Oblique'
        ))
    
    def generate_from_course(self, course_data: Dict[str, Any]) -> str:
        """
        Generate PDF from course data
        Returns the filename of the generated PDF
        """
        if not course_data.get('generatedCourse'):
            raise ValueError("No course data available for PDF generation")
        
        course = course_data['generatedCourse']
        course_title = course.get('course', 'Generated Course')
        modules = course.get('modules', [])
        course_details = course_data.get('courseDetails', {})
        
        # Create PDF document
        filename = f"course-{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.download_folder, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Add title page
        self._add_title_page(story, course_title, course_details)
        story.append(PageBreak())
        
        # Add table of contents
        self._add_table_of_contents(story, modules)
        story.append(PageBreak())
        
        # Add course content
        for module_idx, module in enumerate(modules, 1):
            self._add_module_content(story, module, module_idx)
            if module_idx < len(modules):  # Don't add page break after last module
                story.append(PageBreak())
        
        # Add summary page
        self._add_summary_page(story, course_title, len(modules))
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def generate_from_text(self, text: str, title: str = "Generated Document") -> str:
        """
        Generate PDF from raw text
        """
        # Create PDF document
        filename = f"document-{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.download_folder, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Add title
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Split text into paragraphs and add to story
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                story.append(Paragraph(paragraph.strip(), self.styles['CustomBodyText']))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def _add_title_page(self, story: List, course_title: str, course_details: Dict):
        """Add title page to the PDF"""
        # Main title
        story.append(Paragraph(course_title, self.styles['CustomTitle']))
        story.append(Spacer(1, 40))
        
        # Course details
        if course_details.get('creatorName'):
            story.append(Paragraph(f"Created by: {course_details['creatorName']}", self.styles['CourseTitle']))
            story.append(Spacer(1, 20))
        
        if course_details.get('difficulty'):
            story.append(Paragraph(f"Difficulty Level: {course_details['difficulty']}", self.styles['CustomBodyText']))
            story.append(Spacer(1, 10))
        
        if course_details.get('language'):
            story.append(Paragraph(f"Language: {course_details['language']}", self.styles['CustomBodyText']))
            story.append(Spacer(1, 10))
        
        if course_details.get('prerequisites'):
            story.append(Paragraph("Prerequisites:", self.styles['ModuleTitle']))
            story.append(Paragraph(course_details['prerequisites'], self.styles['CustomBodyText']))
            story.append(Spacer(1, 20))
        
        if course_details.get('targetAudience'):
            story.append(Paragraph("Target Audience:", self.styles['ModuleTitle']))
            story.append(Paragraph(course_details['targetAudience'], self.styles['CustomBodyText']))
    
    def _add_table_of_contents(self, story: List, modules: List[Dict]):
        """Add table of contents to the PDF"""
        story.append(Paragraph("Table of Contents", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        for module_idx, module in enumerate(modules, 1):
            # Module entry
            module_title = f"Module {module_idx}: {module.get('title', 'Untitled Module')}"
            story.append(Paragraph(module_title, self.styles['ModuleTitle']))
            
            # Lesson entries
            for lesson_idx, lesson in enumerate(module.get('lessons', []), 1):
                lesson_title = f"&nbsp;&nbsp;&nbsp;&nbsp;{module_idx}.{lesson_idx} {lesson.get('title', 'Untitled Lesson')}"
                story.append(Paragraph(lesson_title, self.styles['CustomBodyText']))
            
            story.append(Spacer(1, 15))
    
    def _add_module_content(self, story: List, module: Dict, module_num: int):
        """Add module content to the PDF"""
        # Module title
        module_title = f"Module {module_num}: {module.get('title', 'Untitled Module')}"
        story.append(Paragraph(module_title, self.styles['ModuleTitle']))
        story.append(Spacer(1, 20))
        
        # Module lessons
        for lesson_idx, lesson in enumerate(module.get('lessons', []), 1):
            self._add_lesson_content(story, lesson, module_num, lesson_idx)
            if lesson_idx < len(module.get('lessons', [])):  # Don't add extra space after last lesson
                story.append(Spacer(1, 20))
    
    def _add_lesson_content(self, story: List, lesson: Dict, module_num: int, lesson_num: int):
        """Add lesson content to the PDF"""
        # Lesson title
        lesson_title = f"{module_num}.{lesson_num} {lesson.get('title', 'Untitled Lesson')}"
        story.append(Paragraph(lesson_title, self.styles['LessonTitle']))
        
        # Lesson summary
        if lesson.get('summary'):
            story.append(Paragraph("Summary:", self.styles['CustomBodyText']))
            story.append(Paragraph(lesson['summary'], self.styles['SummaryText']))
            story.append(Spacer(1, 10))
        
        # Lesson detail
        if lesson.get('detail'):
            story.append(Paragraph("Content:", self.styles['CustomBodyText']))
            # Split detail into paragraphs
            detail_paragraphs = lesson['detail'].split('\n\n')
            for paragraph in detail_paragraphs:
                if paragraph.strip():
                    story.append(Paragraph(paragraph.strip(), self.styles['CustomBodyText']))
                    story.append(Spacer(1, 6))
    
    def _add_summary_page(self, story: List, course_title: str, module_count: int):
        """Add summary page to the PDF"""
        story.append(Paragraph("Course Summary", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("Congratulations!", self.styles['CourseTitle']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph(f"You have completed: <b>{course_title}</b>", self.styles['CustomBodyText']))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph(f"This course consisted of {module_count} comprehensive modules designed to provide you with in-depth knowledge and practical skills.", self.styles['CustomBodyText']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Key Takeaways:", self.styles['ModuleTitle']))
        story.append(Paragraph("• Comprehensive understanding of the course material", self.styles['CustomBodyText']))
        story.append(Paragraph("• Practical skills and knowledge applicable in real-world scenarios", self.styles['CustomBodyText']))
        story.append(Paragraph("• Confidence to apply what you've learned", self.styles['CustomBodyText']))
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("Thank you for learning with us!", self.styles['CustomBodyText']))

# Global instance
pdf_generator = PDFGenerator()
