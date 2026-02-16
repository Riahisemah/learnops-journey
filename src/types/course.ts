// types/course.ts
export type LessonType = 'video' | 'text' | 'quiz' | 'practice';

export interface Lesson {
  id: string;
  title: string;
  type: LessonType;
  duration: number; // in minutes
  description: string;
  completed?: boolean;
  url?: string;
  content?: string;
}

export interface Module {
  id: string;
  week: number;
  title: string;
  description: string;
  icon: string;
  lessons: Lesson[];
  total_duration?: number;
  completion_rate?: number;
}

export interface ContentSection {
  title: string;
  content: string;
  codeBlocks?: { language: string; code: string }[];
}

export interface LessonContent {
  moduleId: string;
  lessonId: string;
  theory: ContentSection;
  practice: ContentSection;
}