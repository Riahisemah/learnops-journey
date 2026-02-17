import { useParams, Link, useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  ArrowRight,
  Video, 
  FileText, 
  HelpCircle, 
  Code,
  Clock,
  CheckCircle2,
  Circle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getModuleById, getLessonById, LessonType, modules } from "@/data/course-data";
import { getQuizByLesson } from "@/data/quiz-data";
import { getVideoByLesson } from "@/data/video-data";
import { getLessonContent } from "@/data/lesson-content";
import { useProgress } from "@/hooks/use-progress";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import VideoPlayer from "@/components/lesson/VideoPlayer";
import QuizSystem from "@/components/lesson/QuizSystem";
import MarkdownViewer from "@/components/lesson/MarkdownViewer";
import MLDashboard from "@/components/lesson/MLDashboard";

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
  
  const module = getModuleById(moduleId || '');
  const lesson = getLessonById(moduleId || '', lessonId || '');
  
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
  const typeConfig = lessonTypeConfig[lesson.type];
  const TypeIcon = typeConfig.icon;
  
  // Content data
  const quiz = getQuizByLesson(module.id, lesson.id);
  const video = getVideoByLesson(module.id, lesson.id);
  const lessonContent = getLessonContent(module.id, lesson.id);
  
  // Navigation
  const lessonIndex = module.lessons.findIndex(l => l.id === lesson.id);
  const prevLesson = module.lessons[lessonIndex - 1];
  const nextLesson = module.lessons[lessonIndex + 1];
  const currentModuleIndex = modules.findIndex(m => m.id === module.id);
  const nextModule = modules[currentModuleIndex + 1];

  // Check if this is the monitoring lesson (show ML dashboard)
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
          <p className="text-muted-foreground mt-1">{lesson.description}</p>
        </div>
      </header>

      {/* Content */}
      <section className="py-8 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Video lessons */}
          {lesson.type === 'video' && video && (
            <VideoPlayer
              video={video}
              completed={completed}
              onMarkWatched={handleToggleComplete}
            />
          )}

          {/* Quiz lessons */}
          {lesson.type === 'quiz' && quiz && (
            <QuizSystem
              quiz={quiz}
              onComplete={handleQuizComplete}
              completed={completed}
            />
          )}

          {/* Text lessons with markdown viewer */}
          {lesson.type === 'text' && lessonContent && (
            <MarkdownViewer
              theory={lessonContent.theory}
              practice={lessonContent.practice}
            />
          )}

          {/* Practice lessons */}
          {lesson.type === 'practice' && (
            <div className="space-y-6">
              {lessonContent && (
                <MarkdownViewer
                  theory={lessonContent.theory}
                  practice={lessonContent.practice}
                />
              )}
              
              {showMLDashboard && (
                <MLDashboard />
              )}

              {!lessonContent && !showMLDashboard && (
                <div className="text-center py-16 bg-card rounded-lg border border-border">
                  <Code className={cn("h-16 w-16 mx-auto mb-4 opacity-50", typeConfig.color)} />
                  <h2 className="text-xl font-semibold mb-2">Exercice pratique</h2>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Le contenu de cet exercice sera ajouté prochainement.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Fallback for lessons without specific content */}
          {lesson.type === 'video' && !video && (
            <div className="text-center py-16 bg-card rounded-lg border border-border">
              <Video className="h-16 w-16 mx-auto mb-4 opacity-50 text-info" />
              <h2 className="text-xl font-semibold mb-2">Vidéo à venir</h2>
              <p className="text-muted-foreground max-w-md mx-auto">
                La vidéo sera disponible prochainement.
              </p>
            </div>
          )}

          {lesson.type === 'text' && !lessonContent && (
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
                    Terminée - Cliquer pour annuler
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
