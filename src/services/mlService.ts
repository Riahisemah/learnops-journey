import httpClient from './httpClient';
import { API_CONFIG } from '@/config/api';

export interface PredictionInput {
  features: Record<string, number | string>;
}

export interface PredictionOutput {
  prediction: number | string;
  model_version: string;
  confidence: number;
  timestamp: string;
}

export const mlService = {
  predict: async (input: PredictionInput): Promise<PredictionOutput> => {
    const response = await httpClient.post<PredictionOutput>(API_CONFIG.ENDPOINTS.ML.PREDICT, input);
    return response.data;
  },
};
