export interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
}

export interface Quiz {
  id: number;
  title: string;
  topic: string;
  questions: Question[];
  totalQuestions: number;
}

export interface QuizResult {
  score: number;
  totalQuestions: number;
  answers: { [questionId: number]: number };
  timeSpent: number;
}