import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { moduleService, type Module } from "@/services/moduleService";
import { quizService, type Quiz, type QuizSubmission, type QuizResult } from "@/services/quizService";
import { adminService, type AdminStats, type Analytics } from "@/services/adminService";
import { mlService, type PredictionInput, type PredictionOutput } from "@/services/mlService";

// ─── Modules ────────────────────────────────────────────────

export function useModules() {
  return useQuery({
    queryKey: ["modules"],
    queryFn: () => moduleService.getAll(),
    staleTime: 5 * 60 * 1000,
  });
}

export function useModule(id: string) {
  return useQuery({
    queryKey: ["modules", id],
    queryFn: () => moduleService.getById(id),
    enabled: !!id,
  });
}

export function useCompleteLesson() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (lessonId: string) => moduleService.completeLesson(lessonId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["modules"] });
    },
  });
}

// ─── Quiz ───────────────────────────────────────────────────

export function useQuiz(id: string) {
  return useQuery({
    queryKey: ["quiz", id],
    queryFn: () => quizService.getById(id),
    enabled: !!id,
  });
}

export function useSubmitQuiz() {
  return useMutation({
    mutationFn: ({ quizId, submission }: { quizId: string; submission: QuizSubmission }) =>
      quizService.submit(quizId, submission),
  });
}

// ─── Admin ──────────────────────────────────────────────────

export function useAdminStats() {
  return useQuery({
    queryKey: ["admin", "stats"],
    queryFn: () => adminService.getStats(),
    staleTime: 60 * 1000,
  });
}

export function useAdminAnalytics() {
  return useQuery({
    queryKey: ["admin", "analytics"],
    queryFn: () => adminService.getAnalytics(),
    staleTime: 60 * 1000,
  });
}

export function useAdminUsers() {
  return useQuery({
    queryKey: ["admin", "users"],
    queryFn: () => adminService.getUsers(),
    staleTime: 60 * 1000,
  });
}

// ─── ML ─────────────────────────────────────────────────────

export function usePredict() {
  return useMutation({
    mutationFn: (input: PredictionInput) => mlService.predict(input),
  });
}
