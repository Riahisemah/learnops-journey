import { useParams, Link, useNavigate } from "react-router-dom";
import { 
  ArrowLeft, 
  Video, 
  FileText, 
  HelpCircle, 
  Code,
  Clock,
  CheckCircle2,
  Lock,
  ChevronRight,
  Trophy
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { getModuleById, LessonType, modules } from "@/data/course-data";
import { useProgress } from "@/hooks/use-progress";
import { cn } from "@/lib/utils";

const lessonTypeConfig: Record<LessonType, { icon: React.ComponentType<{ className?: string }>; label: string; color: string }> = {
  video: { icon: Video, label: 'Vidéo', color: 'text-info' },
  text: { icon: FileText, label: 'Lecture', color: 'text-primary' },
  quiz: { icon: HelpCircle, label: 'Quiz', color: 'text-warning' },
  practice: { icon: Code, label: 'Pratique', color: 'text-accent' },
};

const ModulePage = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const { getModuleProgress, isLessonCompleted, hasBadge } = useProgress();
  
  const module = getModuleById(moduleId || '');
  
  if (!module) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Module non trouvé</h1>
          <Button asChild>
            <Link to="/">Retour à l'accueil</Link>
          </Button>
        </div>
      </div>
    );
  }

  const progress = getModuleProgress(module.id);
  const hasModuleBadge = hasBadge(module.id);
  const totalDuration = module.lessons.reduce((acc, l) => acc + l.duration, 0);
  
  // Find next incomplete lesson
  const nextLesson = module.lessons.find(l => !isLessonCompleted(module.id, l.id));
  
  // Find current module index for navigation
  const currentModuleIndex = modules.findIndex(m => m.id === module.id);
  const nextModule = modules[currentModuleIndex + 1];

  return (
    <div className="min-h-screen animate-fade-in">
      {/* Header */}
      <header className="bg-gradient-to-br from-primary/5 via-background to-accent/5 py-8 px-6 border-b border-border">
        <div className="max-w-4xl mx-auto">
          <Button 
            variant="ghost" 
            size="sm" 
            className="mb-4 gap-2"
            onClick={() => navigate('/')}
          >
            <ArrowLeft className="h-4 w-4" />
            Retour
          </Button>
          
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <Badge variant="outline" className="mb-2">Semaine {module.week}</Badge>
              <h1 className="text-3xl font-bold">{module.title}</h1>
              <p className="text-muted-foreground mt-1">{module.description}</p>
            </div>
            
            <div className="flex items-center gap-4">
              {hasModuleBadge && (
                <Badge className="bg-warning text-warning-foreground gap-1 px-3 py-1.5">
                  <Trophy className="h-4 w-4" />
                  Badge obtenu !
                </Badge>
              )}
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">{progress}%</div>
                <div className="text-sm text-muted-foreground flex items-center gap-1 justify-end">
                  <Clock className="h-3 w-3" />
                  ~{totalDuration} min
                </div>
              </div>
            </div>
          </div>
          
          <Progress value={progress} className="h-2 mt-4" />
        </div>
      </header>

      {/* Lessons List */}
      <section className="py-8 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold">Leçons</h2>
            {nextLesson && (
              <Button asChild className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground">
                <Link to={`/module/${module.id}/lesson/${nextLesson.id}`}>
                  Continuer
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </Button>
            )}
          </div>

          <div className="space-y-3">
            {module.lessons.map((lesson, index) => {
              const typeConfig = lessonTypeConfig[lesson.type];
              const TypeIcon = typeConfig.icon;
              const completed = isLessonCompleted(module.id, lesson.id);
              const isFirstIncomplete = lesson.id === nextLesson?.id;
              
              return (
                <Link 
                  key={lesson.id} 
                  to={`/module/${module.id}/lesson/${lesson.id}`}
                >
                  <Card className={cn(
                    "group transition-all hover:shadow-md",
                    completed && "bg-accent/5 border-accent/30",
                    isFirstIncomplete && "ring-2 ring-accent ring-offset-2"
                  )}>
                    <CardContent className="p-4">
                      <div className="flex items-center gap-4">
                        <div className={cn(
                          "flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center",
                          completed ? "bg-accent text-accent-foreground" : "bg-secondary"
                        )}>
                          {completed ? (
                            <CheckCircle2 className="h-5 w-5" />
                          ) : (
                            <span className="text-sm font-medium">{index + 1}</span>
                          )}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-0.5">
                            <TypeIcon className={cn("h-4 w-4", typeConfig.color)} />
                            <span className={cn("text-xs", typeConfig.color)}>
                              {typeConfig.label}
                            </span>
                          </div>
                          <h3 className="font-medium group-hover:text-accent transition-colors">
                            {lesson.title}
                          </h3>
                          <p className="text-sm text-muted-foreground truncate">
                            {lesson.description}
                          </p>
                        </div>
                        
                        <div className="flex-shrink-0 flex items-center gap-3">
                          <span className="text-sm text-muted-foreground flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {lesson.duration} min
                          </span>
                          <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-accent transition-colors" />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>

          {/* Next Module */}
          {progress === 100 && nextModule && (
            <Card className="mt-8 bg-accent/5 border-accent/30">
              <CardContent className="p-6 flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Module suivant</p>
                  <h3 className="font-semibold">{nextModule.title}</h3>
                </div>
                <Button asChild className="bg-accent hover:bg-accent/90 text-accent-foreground">
                  <Link to={`/module/${nextModule.id}`}>
                    Continuer
                    <ChevronRight className="h-4 w-4 ml-1" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </div>
  );
};

export default ModulePage;
