import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';

export interface QuizQuestion {
  id: string;
  question: string;
  type: 'single' | 'multiple' | 'boolean';
  options: string[];
  correct_answers: number[];
  explanation?: string;
}

export interface Quiz {
  id: string;
  title: string;
  module_id: string;
  questions: QuizQuestion[];
  passing_score: number;
  time_limit?: number;
}

export interface QuizSubmission {
  answers: Record<string, number[]>;
}

export interface QuizResult {
  attempt_id: string;
  score: number;
  passed: boolean;
  correct_answers: number;
  total_questions: number;
  time_taken: number;
  answers: Record<string, boolean>;
}

export const quizService = {
  getById: async (id: string): Promise<Quiz> => {
    const response = await httpClient.get<Quiz>(API_CONFIG.ENDPOINTS.QUIZ.GET(id));
    return response.data;
  },

  submit: async (quizId: string, submission: QuizSubmission): Promise<QuizResult> => {
    const response = await httpClient.post<QuizResult>(API_CONFIG.ENDPOINTS.QUIZ.SUBMIT(quizId), submission);
    return response.data;
  },

  getResults: async (quizId: string, attemptId: string): Promise<QuizResult> => {
    const response = await httpClient.get<QuizResult>(API_CONFIG.ENDPOINTS.QUIZ.RESULTS(quizId, attemptId));
    return response.data;
  },
};
