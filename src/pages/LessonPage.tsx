import { useParams, Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { 
  ArrowLeft, 
  ArrowRight,
  Video, 
  FileText, 
  HelpCircle, 
  Code,
  Clock,
  CheckCircle2,
  Circle,
  Loader2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { moduleService, type Module, type Lesson } from "@/services/moduleService";
import { lessonService, type LessonContent } from "@/services/lessonService";
import { useProgress } from "@/hooks/use-progress";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import VideoPlayer from "@/components/lesson/VideoPlayer";
import QuizSystem from "@/components/lesson/QuizSystem";
import MarkdownViewer from "@/components/lesson/MarkdownViewer";
import MLDashboard from "@/components/lesson/MLDashboard";

type LessonType = 'video' | 'text' | 'quiz' | 'practice';

const lessonTypeConfig: Record<LessonType, { icon: React.ComponentType<{ className?: string }>; label: string; color: string }> = {
  video: { icon: Video, label: 'Vidéo', color: 'text-info' },
  text: { icon: FileText, label: 'Lecture', color: 'text-primary' },
  quiz: { icon: HelpCircle, label: 'Quiz', color: 'text-warning' },
  practice: { icon: Code, label: 'Pratique', color: 'text-accent' },
};

const LessonPage = () => {
  const { moduleId, lessonId } = useParams<{ moduleId: string; lessonId: string }>();
  const navigate = useNavigate();
  const { isLessonCompleted, completeLesson, hasBadge } = useProgress();
  
  const [module, setModule] = useState<Module | null>(null);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [lessonContent, setLessonContent] = useState<LessonContent | null>(null);
  const [allModules, setAllModules] = useState<Module[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!moduleId || !lessonId) return;
      setIsLoading(true);
      try {
        const [moduleData, lessons, modules] = await Promise.all([
          moduleService.getById(moduleId),
          moduleService.getLessons(moduleId),
          moduleService.getAll(),
        ]);
        setModule(moduleData);
        setAllModules(modules);
        const foundLesson = lessons.find(l => l.id === lessonId) || null;
        setLesson(foundLesson);

        // Try to fetch lesson content
        try {
          const content = await lessonService.getLessonContent(moduleId, lessonId);
          setLessonContent(content);
        } catch {
          setLessonContent(null);
        }
      } catch (err) {
        console.error('Error fetching lesson data:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [moduleId, lessonId]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Chargement de la leçon...</p>
        </div>
      </div>
    );
  }

  if (!module || !lesson) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Leçon non trouvée</h1>
          <Button asChild>
            <Link to="/">Retour à l'accueil</Link>
          </Button>
        </div>
      </div>
    );
  }

  const completed = isLessonCompleted(module.id, lesson.id);
  const typeConfig = lessonTypeConfig[lesson.type as LessonType] || lessonTypeConfig.text;
  const TypeIcon = typeConfig.icon;
  
  // Navigation
  const lessons = module.lessons || [];
  const lessonIndex = lessons.findIndex(l => l.id === lesson.id);
  const prevLesson = lessons[lessonIndex - 1];
  const nextLesson = lessons[lessonIndex + 1];
  const currentModuleIndex = allModules.findIndex(m => m.id === module.id);
  const nextModule = allModules[currentModuleIndex + 1];

  const showMLDashboard = lesson.id === 'monitoring' || lesson.id === 'project-recap';

  const handleToggleComplete = () => {
    if (completed) {
      toast.info("Leçon déjà terminée");
    } else {
      completeLesson(module.id, lesson.id);
      const hadBadge = hasBadge(module.id);
      setTimeout(() => {
        if (!hadBadge && hasBadge(module.id)) {
          toast.success(`🏆 Félicitations ! Badge "${module.title}" obtenu !`);
        } else {
          toast.success("Leçon terminée !");
        }
      }, 100);
    }
  };

  const handleQuizComplete = () => {
    if (!completed) {
      completeLesson(module.id, lesson.id);
      const hadBadge = hasBadge(module.id);
      setTimeout(() => {
        if (!hadBadge && hasBadge(module.id)) {
          toast.success(`🏆 Badge "${module.title}" obtenu !`);
        }
      }, 100);
    }
  };

  const handleNext = () => {
    if (nextLesson) {
      navigate(`/module/${module.id}/lesson/${nextLesson.id}`);
    } else if (nextModule) {
      navigate(`/module/${nextModule.id}`);
    } else {
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen animate-fade-in">
      {/* Header */}
      <header className="bg-gradient-to-br from-primary/5 via-background to-accent/5 py-6 px-6 border-b border-border">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <Button 
              variant="ghost" 
              size="sm" 
              className="gap-2"
              onClick={() => navigate(`/module/${module.id}`)}
            >
              <ArrowLeft className="h-4 w-4" />
              {module.title}
            </Button>
            
            <div className="flex items-center gap-2">
              <Badge variant="outline" className={cn("gap-1", typeConfig.color)}>
                <TypeIcon className="h-3 w-3" />
                {typeConfig.label}
              </Badge>
              <Badge variant="secondary" className="gap-1">
                <Clock className="h-3 w-3" />
                {lesson.duration} min
              </Badge>
            </div>
          </div>
          
          <h1 className="text-2xl lg:text-3xl font-bold">{lesson.title}</h1>
          {lesson.content && <p className="text-muted-foreground mt-1">{lesson.content}</p>}
        </div>
      </header>

      {/* Content */}
      <section className="py-8 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Text/Practice lessons with markdown viewer */}
          {(lesson.type === 'text' || lesson.type === 'practice') && lessonContent && (
            <MarkdownViewer
              theory={lessonContent.theory}
              practice={lessonContent.practice}
            />
          )}

          {/* Practice with ML Dashboard */}
          {lesson.type === 'practice' && showMLDashboard && (
            <MLDashboard />
          )}

          {/* Fallback for lessons without specific content */}
          {lesson.type === 'video' && (
            <div className="text-center py-16 bg-card rounded-lg border border-border">
              <Video className="h-16 w-16 mx-auto mb-4 opacity-50 text-info" />
              <h2 className="text-xl font-semibold mb-2">Vidéo</h2>
              <p className="text-muted-foreground max-w-md mx-auto">
                {lesson.url ? 'Lecteur vidéo' : 'La vidéo sera disponible prochainement.'}
              </p>
            </div>
          )}

          {lesson.type === 'quiz' && (
            <div className="text-center py-16 bg-card rounded-lg border border-border">
              <HelpCircle className="h-16 w-16 mx-auto mb-4 opacity-50 text-warning" />
              <h2 className="text-xl font-semibold mb-2">Quiz</h2>
              <p className="text-muted-foreground max-w-md mx-auto">
                Le quiz sera chargé depuis le backend.
              </p>
            </div>
          )}

          {(lesson.type === 'text' || lesson.type === 'practice') && !lessonContent && !showMLDashboard && (
            <div className="text-center py-16 bg-card rounded-lg border border-border">
              <FileText className="h-16 w-16 mx-auto mb-4 opacity-50 text-primary" />
              <h2 className="text-xl font-semibold mb-2">Contenu à venir</h2>
              <p className="text-muted-foreground max-w-md mx-auto">
                Le contenu de cette leçon sera ajouté prochainement.
              </p>
            </div>
          )}

          {/* Actions */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            {lesson.type !== 'quiz' && (
              <Button
                variant={completed ? "outline" : "default"}
                size="lg"
                onClick={handleToggleComplete}
                className={cn(
                  "gap-2 w-full sm:w-auto",
                  !completed && "bg-accent hover:bg-accent/90 text-accent-foreground"
                )}
              >
                {completed ? (
                  <>
                    <CheckCircle2 className="h-5 w-5 text-accent" />
                    Terminée
                  </>
                ) : (
                  <>
                    <Circle className="h-5 w-5" />
                    Marquer comme terminée
                  </>
                )}
              </Button>
            )}

            {lesson.type === 'quiz' && (
              <div className="w-full sm:w-auto">
                {completed && (
                  <Badge variant="outline" className="gap-1 text-accent border-accent">
                    <CheckCircle2 className="h-4 w-4" />
                    Quiz complété
                  </Badge>
                )}
              </div>
            )}

            <div className="flex gap-2 w-full sm:w-auto">
              {prevLesson && (
                <Button
                  variant="outline"
                  onClick={() => navigate(`/module/${module.id}/lesson/${prevLesson.id}`)}
                  className="flex-1 sm:flex-none gap-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Précédent
                </Button>
              )}
              
              <Button
                onClick={handleNext}
                className="flex-1 sm:flex-none gap-2"
              >
                {nextLesson ? 'Suivant' : nextModule ? 'Module suivant' : 'Terminer'}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LessonPage;
