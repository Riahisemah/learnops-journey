import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { moduleService, type Module } from "@/services/moduleService";
import { quizService, type Quiz, type QuizSubmission, type QuizResult } from "@/services/quizService";
import { adminService, type AdminStats, type Analytics } from "@/services/adminService";
import { mlService, type PredictionInput, type PredictionOutput } from "@/services/mlService";
import { modules as localModules } from "@/data/course-data";
import { mockUsers } from "@/data/mock-users";

const BACKEND_STATUS_KEY = "devops-mlops-backend-status";
const isBackendUp = () => localStorage.getItem(BACKEND_STATUS_KEY) === "true";

// ─── Modules ────────────────────────────────────────────────

export function useModules() {
  return useQuery({
    queryKey: ["modules"],
    queryFn: async () => {
      if (isBackendUp()) {
        try {
          return await moduleService.getAll();
        } catch {
          console.warn("API modules failed, using local data");
        }
      }
      // Fallback: local course data mapped to Module shape
      return localModules.map(m => ({
        id: m.id,
        title: m.title,
        description: m.description,
        week: m.week,
        order: m.week,
        lessons: m.lessons.map(l => ({
          id: l.id,
          title: l.title,
          type: l.type,
          duration: String(l.duration),
          completed: false,
          content: l.description,
        })),
        completion_rate: 0,
        total_duration: m.lessons.reduce((a, l) => a + l.duration, 0),
      })) as Module[];
    },
    staleTime: 5 * 60 * 1000,
  });
}

export function useModule(id: string) {
  return useQuery({
    queryKey: ["modules", id],
    queryFn: async () => {
      if (isBackendUp()) {
        try {
          return await moduleService.getById(id);
        } catch { /* fallback */ }
      }
      const local = localModules.find(m => m.id === id);
      if (!local) throw new Error("Module not found");
      return {
        id: local.id,
        title: local.title,
        description: local.description,
        week: local.week,
        order: local.week,
        lessons: local.lessons.map(l => ({
          id: l.id,
          title: l.title,
          type: l.type,
          duration: String(l.duration),
          completed: false,
          content: l.description,
        })),
        completion_rate: 0,
        total_duration: local.lessons.reduce((a, l) => a + l.duration, 0),
      } as Module;
    },
    enabled: !!id,
  });
}

export function useCompleteLesson() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (lessonId: string) => {
      if (isBackendUp()) {
        return moduleService.completeLesson(lessonId);
      }
      return Promise.resolve();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["modules"] });
    },
  });
}

// ─── Quiz ───────────────────────────────────────────────────

export function useQuiz(id: string) {
  return useQuery({
    queryKey: ["quiz", id],
    queryFn: async () => {
      if (isBackendUp()) {
        try {
          return await quizService.getById(id);
        } catch { /* fallback */ }
      }
      return null;
    },
    enabled: !!id,
  });
}

export function useSubmitQuiz() {
  return useMutation({
    mutationFn: ({ quizId, submission }: { quizId: string; submission: QuizSubmission }) => {
      if (isBackendUp()) {
        return quizService.submit(quizId, submission);
      }
      // Fallback: simulate result
      return Promise.resolve({
        attempt_id: `local-${Date.now()}`,
        score: 75,
        passed: true,
        correct_answers: 15,
        total_questions: 20,
        time_taken: 600,
        answers: {},
      } as QuizResult);
    },
  });
}

// ─── Admin ──────────────────────────────────────────────────

export function useAdminStats() {
  return useQuery({
    queryKey: ["admin", "stats"],
    queryFn: async () => {
      if (isBackendUp()) {
        try {
          return await adminService.getStats();
        } catch { /* fallback */ }
      }
      const students = mockUsers.filter(u => u.role === "student");
      const completions = students.filter(s => s.progression === 100).length;
      return {
        total_users: mockUsers.length,
        total_modules: localModules.length,
        total_completions: completions,
        average_rating: 4.8,
        users_growth: 12,
        completions_rate: Math.round((completions / (students.length || 1)) * 100),
      } as AdminStats;
    },
    staleTime: 60 * 1000,
  });
}

export function useAdminAnalytics() {
  return useQuery({
    queryKey: ["admin", "analytics"],
    queryFn: async () => {
      if (isBackendUp()) {
        try {
          return await adminService.getAnalytics();
        } catch { /* fallback */ }
      }
      // Generate mock analytics
      const last7Days = Array.from({ length: 7 }, (_, i) => {
        const d = new Date();
        d.setDate(d.getDate() - (6 - i));
        return { date: d.toISOString().split("T")[0], count: Math.floor(Math.random() * 5) + 1 };
      });
      return {
        registrations_per_day: last7Days,
        popular_modules: localModules.map(m => ({
          module_id: m.id,
          title: m.title,
          views: Math.floor(Math.random() * 500) + 100,
        })),
        user_roles: [
          { role: "student", count: mockUsers.filter(u => u.role === "student").length },
          { role: "instructor", count: mockUsers.filter(u => u.role === "instructor").length },
          { role: "admin", count: mockUsers.filter(u => u.role === "admin").length },
        ],
        recent_activity: [
          { user: "Sophie L.", action: "a complété le Module 3", timestamp: new Date().toISOString() },
          { user: "Admin", action: "a ajouté un nouveau quiz", timestamp: new Date(Date.now() - 3600000).toISOString() },
          { user: "Jean M.", action: "s'est inscrit", timestamp: new Date(Date.now() - 7200000).toISOString() },
        ],
      } as Analytics;
    },
    staleTime: 60 * 1000,
  });
}

// ─── ML ─────────────────────────────────────────────────────

export function usePredict() {
  return useMutation({
    mutationFn: (input: PredictionInput) => {
      if (isBackendUp()) {
        return mlService.predict(input);
      }
      return Promise.resolve({
        prediction: 0.85,
        model_version: "v1.0.0-local",
        confidence: 0.92,
        timestamp: new Date().toISOString(),
      } as PredictionOutput);
    },
  });
}
