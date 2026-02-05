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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getModuleById, getLessonById, LessonType, modules } from "@/data/course-data";
import { useProgress } from "@/hooks/use-progress";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const lessonTypeConfig: Record<LessonType, { icon: React.ComponentType<{ className?: string }>; label: string; color: string }> = {
  video: { icon: Video, label: 'Vidéo', color: 'text-info' },
  text: { icon: FileText, label: 'Lecture', color: 'text-primary' },
  quiz: { icon: HelpCircle, label: 'Quiz', color: 'text-warning' },
  practice: { icon: Code, label: 'Pratique', color: 'text-accent' },
};

const LessonPage = () => {
  const { moduleId, lessonId } = useParams<{ moduleId: string; lessonId: string }>();
  const navigate = useNavigate();
  const { isLessonCompleted, completeLesson, uncompleteLesson, hasBadge } = useProgress();
  
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
  
  // Navigation
  const lessonIndex = module.lessons.findIndex(l => l.id === lesson.id);
  const prevLesson = module.lessons[lessonIndex - 1];
  const nextLesson = module.lessons[lessonIndex + 1];
  
  // If no next lesson, check for next module
  const currentModuleIndex = modules.findIndex(m => m.id === module.id);
  const nextModule = modules[currentModuleIndex + 1];

  const handleToggleComplete = () => {
    if (completed) {
      uncompleteLesson(module.id, lesson.id);
      toast.info("Leçon marquée comme non terminée");
    } else {
      completeLesson(module.id, lesson.id);
      
      // Check if badge was just earned
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

      {/* Content Placeholder */}
      <section className="py-8 px-6">
        <div className="max-w-4xl mx-auto">
          <Card className="min-h-[400px] flex items-center justify-center">
            <CardContent className="text-center py-16">
              <TypeIcon className={cn("h-16 w-16 mx-auto mb-4 opacity-50", typeConfig.color)} />
              <h2 className="text-xl font-semibold mb-2">Contenu de la leçon</h2>
              <p className="text-muted-foreground max-w-md mx-auto">
                Le contenu de cette leçon sera ajouté prochainement. 
                Pour l'instant, vous pouvez marquer cette leçon comme terminée pour tester la progression.
              </p>
              
              {lesson.type === 'video' && (
                <div className="mt-6 p-8 bg-secondary rounded-lg">
                  <Video className="h-12 w-12 mx-auto text-muted-foreground" />
                  <p className="text-sm text-muted-foreground mt-2">Emplacement vidéo</p>
                </div>
              )}
              
              {lesson.type === 'quiz' && (
                <div className="mt-6 p-8 bg-secondary rounded-lg">
                  <HelpCircle className="h-12 w-12 mx-auto text-muted-foreground" />
                  <p className="text-sm text-muted-foreground mt-2">Questions du quiz</p>
                </div>
              )}
              
              {lesson.type === 'practice' && (
                <div className="mt-6 p-8 bg-secondary rounded-lg font-mono text-sm text-left">
                  <Code className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground text-center">Zone de code interactif</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
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
