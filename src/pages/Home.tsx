import { Link } from "react-router-dom";
import { 
  ArrowRight, 
  BookOpen, 
  Clock, 
  Trophy, 
  CheckCircle2,
  GitBranch,
  Brain,
  Rocket,
  Award
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { useProgress } from "@/hooks/use-progress";
import { useModules } from "@/hooks/use-api";
import { cn } from "@/lib/utils";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  GitBranch,
  Brain,
  Rocket,
  Award,
};

const Home = () => {
  const { 
    getOverallProgress, 
    getCompletedLessonsCount, 
    getBadgesCount,
    getModuleProgress,
    hasBadge
  } = useProgress();

  const { data: modules = [], isLoading } = useModules();

  const totalLessons = modules.reduce((acc: number, module: any) => acc + (module.lessons?.length || 0), 0);
  const totalMinutes = modules.reduce((acc: number, module: any) => acc + (module.total_duration || 0), 0);
  const totalHours = Math.floor(totalMinutes / 60);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Chargement du parcours...</p>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen animate-fade-in">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/5 via-background to-accent/5 py-16 px-6 lg:py-24">
        <div className="absolute inset-0 bg-grid-pattern opacity-5" />
        <div className="relative max-w-4xl mx-auto text-center space-y-6">
          <Badge variant="secondary" className="px-4 py-1.5">
            🚀 Parcours complet en 4 semaines
          </Badge>
          
          <h1 className="text-4xl lg:text-6xl font-bold tracking-tight">
            Didacticiel{" "}
            <span className="text-primary">DevOps</span> &{" "}
            <span className="text-accent">MLOps</span>
          </h1>
          
          <p className="text-lg lg:text-xl text-muted-foreground max-w-2xl mx-auto">
            Maîtrisez les pratiques DevOps et MLOps modernes. De Docker à MLflow, 
            apprenez à déployer et maintenir des modèles ML en production.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Button asChild size="lg" className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground">
              <Link to={modules.length > 0 ? `/module/${modules[0].id}` : "/"}>
                Commencer le parcours
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <span className="flex items-center gap-1.5">
                <BookOpen className="h-4 w-4" />
                {totalLessons} leçons
              </span>
              <span className="flex items-center gap-1.5">
                <Clock className="h-4 w-4" />
                ~{totalHours}h de contenu
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 px-6 border-b border-border">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-3xl font-bold text-primary">{getOverallProgress()}%</div>
                <div className="text-sm text-muted-foreground">Progression</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-3xl font-bold text-accent">{getCompletedLessonsCount()}</div>
                <div className="text-sm text-muted-foreground">Leçons terminées</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-3xl font-bold text-warning">{getBadgesCount()}</div>
                <div className="text-sm text-muted-foreground">Badges gagnés</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-3xl font-bold">{totalLessons}</div>
                <div className="text-sm text-muted-foreground">Leçons totales</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl lg:text-3xl font-bold mb-3">Parcours en {modules.length} semaines</h2>
            <p className="text-muted-foreground">
              Un programme structuré pour maîtriser DevOps et MLOps
            </p>
          </div>

          <div className="space-y-6">
            {modules.map((module: any, index: number) => {
              const IconComponent = iconMap[module.icon] || BookOpen;
              const progress = getModuleProgress(module.id);
              const hasBadgeForModule = hasBadge(module.id);
              const isCompleted = progress === 100;
              
              return (
                <Link key={module.id} to={`/module/${module.id}`}>
                  <Card className={cn(
                    "group transition-all duration-300 hover:shadow-lg hover:border-accent/50",
                    isCompleted && "border-accent/30 bg-accent/5"
                  )}>
                    <CardHeader className="pb-3">
                      <div className="flex items-start gap-4">
                        <div className={cn(
                          "flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-colors",
                          isCompleted 
                            ? "bg-accent text-accent-foreground" 
                            : "bg-secondary text-secondary-foreground group-hover:bg-accent/20"
                        )}>
                          {isCompleted ? (
                            <CheckCircle2 className="h-6 w-6" />
                          ) : (
                            <IconComponent className="h-6 w-6" />
                          )}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <Badge variant="outline" className="text-xs">
                              Semaine {module.week}
                            </Badge>
                            {hasBadgeForModule && (
                              <Badge className="bg-warning text-warning-foreground text-xs gap-1">
                                <Trophy className="h-3 w-3" />
                                Badge obtenu
                              </Badge>
                            )}
                          </div>
                          <CardTitle className="text-lg group-hover:text-accent transition-colors">
                            {module.title}
                          </CardTitle>
                          <CardDescription className="mt-1">
                            {module.description}
                          </CardDescription>
                        </div>
                        
                        <div className="flex-shrink-0 text-right">
                          <div className="text-2xl font-bold text-primary">{progress}%</div>
                          <div className="text-xs text-muted-foreground">
                            {module.lessons?.length || 0} leçons
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    
                    <CardContent className="pt-0">
                      <Progress value={progress} className="h-2" />
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
