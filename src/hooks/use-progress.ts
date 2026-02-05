import { useState, useEffect, useCallback } from 'react';
import { modules } from '@/data/course-data';

interface ProgressState {
  completedLessons: string[]; // Array of "moduleId:lessonId"
  earnedBadges: string[]; // Array of moduleIds that have been fully completed
  startedAt: string | null;
}

const STORAGE_KEY = 'devops-mlops-progress';

const getInitialState = (): ProgressState => {
  if (typeof window === 'undefined') {
    return { completedLessons: [], earnedBadges: [], startedAt: null };
  }
  
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return { completedLessons: [], earnedBadges: [], startedAt: null };
    }
  }
  return { completedLessons: [], earnedBadges: [], startedAt: null };
};

export const useProgress = () => {
  const [progress, setProgress] = useState<ProgressState>(getInitialState);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const isLessonCompleted = useCallback((moduleId: string, lessonId: string): boolean => {
    return progress.completedLessons.includes(`${moduleId}:${lessonId}`);
  }, [progress.completedLessons]);

  const completeLesson = useCallback((moduleId: string, lessonId: string) => {
    setProgress(prev => {
      const lessonKey = `${moduleId}:${lessonId}`;
      if (prev.completedLessons.includes(lessonKey)) {
        return prev;
      }

      const newCompletedLessons = [...prev.completedLessons, lessonKey];
      
      // Check if module is now complete
      const module = modules.find(m => m.id === moduleId);
      const moduleComplete = module?.lessons.every(lesson => 
        newCompletedLessons.includes(`${moduleId}:${lesson.id}`)
      );

      const newBadges = moduleComplete && !prev.earnedBadges.includes(moduleId)
        ? [...prev.earnedBadges, moduleId]
        : prev.earnedBadges;

      return {
        completedLessons: newCompletedLessons,
        earnedBadges: newBadges,
        startedAt: prev.startedAt || new Date().toISOString(),
      };
    });
  }, []);

  const uncompleteLesson = useCallback((moduleId: string, lessonId: string) => {
    setProgress(prev => {
      const lessonKey = `${moduleId}:${lessonId}`;
      return {
        ...prev,
        completedLessons: prev.completedLessons.filter(key => key !== lessonKey),
        // Remove badge if module is no longer complete
        earnedBadges: prev.earnedBadges.filter(id => id !== moduleId),
      };
    });
  }, []);

  const getModuleProgress = useCallback((moduleId: string): number => {
    const module = modules.find(m => m.id === moduleId);
    if (!module) return 0;

    const completedInModule = progress.completedLessons.filter(key => 
      key.startsWith(`${moduleId}:`)
    ).length;

    return Math.round((completedInModule / module.lessons.length) * 100);
  }, [progress.completedLessons]);

  const getOverallProgress = useCallback((): number => {
    const totalLessons = modules.reduce((acc, m) => acc + m.lessons.length, 0);
    if (totalLessons === 0) return 0;
    return Math.round((progress.completedLessons.length / totalLessons) * 100);
  }, [progress.completedLessons]);

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
    uncompleteLesson,
    getModuleProgress,
    getOverallProgress,
    getCompletedLessonsCount,
    getBadgesCount,
    hasBadge,
    resetProgress,
    startedAt: progress.startedAt,
  };
};
