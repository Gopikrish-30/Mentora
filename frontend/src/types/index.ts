export interface Lesson {
  title: string;
  summary: string;
  detail: string;
}

export interface Module {
  title: string;
  lessons: Lesson[];
}

export interface GeneratedCourse {
  course: string;
  modules: Module[];
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

export const exportTypes = [
  'Course',
  'PowerPoint',
  'PDF'
] as const;

export type DifficultyLevel = typeof difficultyLevels[number];
export type Language = typeof languages[number];
export type ExportType = typeof exportTypes[number];

export interface CourseDetails {
  title: string;
  creatorName: string;
  difficulty: DifficultyLevel;
  language: Language;
  prerequisites: string;
  targetAudience: string;
}

export interface CourseData {
  description: string;
  uploadedFiles: File[];
  courseId: string;
  extractedText: string;
  generatedCourse: GeneratedCourse | null;
  courseDetails: CourseDetails;
  exportType: ExportType;
}

export interface CourseStepProps {
  onNext?: () => void;
  onBack?: () => void;
  courseData: CourseData;
  setCourseData: (data: CourseData) => void;
}

export interface TranslationState {
  isTranslated: boolean;
  currentLanguage: string;
  targetLanguage: string;
  isLoading: boolean;
  error: string | null;
}

export interface TranslationResponse {
  original_content: string;
  translated_content: string;
  target_lang: string;
  target_lang_name: string;
}