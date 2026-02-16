import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { moduleService } from '@/services/moduleService';
import { lessonService } from '@/services/lessonService';

interface ProgressState {
  completedLessons: string[]; // Array of "moduleId:lessonId"
  earnedBadges: string[]; // Array of moduleIds that have been fully completed
  startedAt: string | null;
}

const STORAGE_KEY = 'devops-mlops-progress';

export const useProgress = () => {
  const { user } = useAuth();
  const [progress, setProgress] = useState<ProgressState>({
    completedLessons: [],
    earnedBadges: [],
    startedAt: null
  });
  const [modules, setModules] = useState<any[]>([]);

  // Charger les modules depuis l'API
  useEffect(() => {
    const loadModules = async () => {
      try {
        const data = await moduleService.getAll();
        setModules(data);
      } catch (error) {
        console.error('Error loading modules:', error);
      }
    };
    loadModules();
  }, []);

  // Charger la progression
  useEffect(() => {
    const loadProgress = async () => {
      if (!user) {
        // Fallback au localStorage si pas d'utilisateur
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          try {
            setProgress(JSON.parse(stored));
          } catch {
            setProgress({ completedLessons: [], earnedBadges: [], startedAt: null });
          }
        }
        return;
      }

      try {
        const modules = await moduleService.getAll();
        
        // Convertir la progression API en format local
        const completedLessons: string[] = [];
        const earnedBadges: string[] = modules
          .filter(m => m.completion_rate === 100)
          .map(m => m.id);

        setProgress({
          completedLessons,
          earnedBadges,
          startedAt: new Date().toISOString(),
        });
      } catch (error) {
        console.error('Error loading progress:', error);
        // Fallback au localStorage
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          setProgress(JSON.parse(stored));
        }
      }
    };

    loadProgress();
  }, [user]);

  // Sauvegarder dans localStorage à chaque changement
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const isLessonCompleted = useCallback((moduleId: string, lessonId: string): boolean => {
    return progress.completedLessons.includes(`${moduleId}:${lessonId}`);
  }, [progress.completedLessons]);

  const completeLesson = useCallback(async (moduleId: string, lessonId: string) => {
    const lessonKey = `${moduleId}:${lessonId}`;
    
    if (progress.completedLessons.includes(lessonKey)) {
      return;
    }

    const newCompletedLessons = [...progress.completedLessons, lessonKey];
    
    // Vérifier si le module est complet
    const module = modules.find(m => m.id === moduleId);
    const moduleComplete = module?.lessons?.every((lesson: any) => 
      newCompletedLessons.includes(`${moduleId}:${lesson.id}`)
    );

    const newBadges = moduleComplete && !progress.earnedBadges.includes(moduleId)
      ? [...progress.earnedBadges, moduleId]
      : progress.earnedBadges;

    const newProgress = {
      completedLessons: newCompletedLessons,
      earnedBadges: newBadges,
      startedAt: progress.startedAt || new Date().toISOString(),
    };

    setProgress(newProgress);

    // Envoyer à l'API si utilisateur connecté
    if (user) {
      try {
        await lessonService.completeLesson(lessonId);
      } catch (error) {
        console.error('Error syncing lesson completion:', error);
      }
    }
  }, [progress, modules, user]);

  const getModuleProgress = useCallback((moduleId: string): number => {
    const module = modules.find(m => m.id === moduleId);
    if (!module || !module.lessons) return 0;

    const completedInModule = progress.completedLessons.filter(key => 
      key.startsWith(`${moduleId}:`)
    ).length;

    return Math.round((completedInModule / module.lessons.length) * 100);
  }, [progress.completedLessons, modules]);

  const getOverallProgress = useCallback((): number => {
    if (modules.length === 0) return 0;
    
    const totalLessons = modules.reduce((acc, m) => acc + (m.lessons?.length || 0), 0);
    if (totalLessons === 0) return 0;
    
    return Math.round((progress.completedLessons.length / totalLessons) * 100);
  }, [progress.completedLessons, modules]);

  const getCompletedLessonsCount = useCallback((): number => {
    return progress.completedLessons.length;
  }, [progress.completedLessons]);

  const getBadgesCount = useCallback((): number => {
    return progress.earnedBadges.length;
  }, [progress.earnedBadges]);

  const hasBadge = useCallback((moduleId: string): boolean => {
    return progress.earnedBadges.includes(moduleId);
  }, [progress.earnedBadges]);

  const resetProgress = useCallback(() => {
    setProgress({ completedLessons: [], earnedBadges: [], startedAt: null });
  }, []);

  return {
    isLessonCompleted,
    completeLesson,
    getModuleProgress,
    getOverallProgress,
    getCompletedLessonsCount,
    getBadgesCount,
    hasBadge,
    resetProgress,
    startedAt: progress.startedAt,
  };
}