import { 
  Trophy, 
  Download, 
  Clock, 
  BookOpen, 
  Award,
  CheckCircle2
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { modules } from "@/data/course-data";
import { useProgress } from "@/hooks/use-progress";
import { cn } from "@/lib/utils";

const ProgressDashboard = () => {
  const { 
    getOverallProgress, 
    getModuleProgress, 
    getCompletedLessonsCount,
    getBadgesCount,
    hasBadge,
    startedAt,
  } = useProgress();

  const overall = getOverallProgress();
  const totalLessons = modules.reduce((acc, m) => acc + m.lessons.length, 0);
  const completedCount = getCompletedLessonsCount();
  const badgesCount = getBadgesCount();

  const handleDownloadCertificate = () => {
    // Generate a simple text certificate (PDF generation would need a library)
    const certContent = `
╔══════════════════════════════════════════════════╗
║                                                  ║
║           CERTIFICAT DE COMPLÉTION               ║
║                                                  ║
║  Didacticiel DevOps & MLOps                      ║
║                                                  ║
║  Progression : ${overall}%                       ║
║  Leçons complétées : ${completedCount}/${totalLessons}            ║
║  Badges obtenus : ${badgesCount}/${modules.length}                ║
║                                                  ║
║  Date : ${new Date().toLocaleDateString('fr-FR')}                     ║
║                                                  ║
║  Modules complétés :                             ║
${modules.map(m => `║  ${hasBadge(m.id) ? '✅' : '⬜'} ${m.title.padEnd(40)}║`).join('\n')}
║                                                  ║
╚══════════════════════════════════════════════════╝
    `.trim();

    const blob = new Blob([certContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'certificat-devops-mlops.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Circular progress SVG
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference - (overall / 100) * circumference;

  return (
    <div className="space-y-6">
      {/* Overall Progress Circle */}
      <Card>
        <CardContent className="p-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            {/* SVG Circle */}
            <div className="relative flex-shrink-0">
              <svg width="180" height="180" className="transform -rotate-90">
                <circle
                  cx="90"
                  cy="90"
                  r={radius}
                  fill="none"
                  stroke="hsl(var(--secondary))"
                  strokeWidth="12"
                />
                <circle
                  cx="90"
                  cy="90"
                  r={radius}
                  fill="none"
                  stroke="hsl(var(--accent))"
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={dashOffset}
                  className="transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-primary">{overall}%</span>
                <span className="text-xs text-muted-foreground">Progression</span>
              </div>
            </div>

            {/* Stats */}
            <div className="flex-1 grid grid-cols-2 gap-4 w-full">
              <div className="text-center p-4 rounded-lg bg-secondary">
                <BookOpen className="h-6 w-6 mx-auto mb-1 text-primary" />
                <div className="text-2xl font-bold">{completedCount}</div>
                <div className="text-xs text-muted-foreground">/ {totalLessons} leçons</div>
              </div>
              <div className="text-center p-4 rounded-lg bg-secondary">
                <Trophy className="h-6 w-6 mx-auto mb-1 text-warning" />
                <div className="text-2xl font-bold">{badgesCount}</div>
                <div className="text-xs text-muted-foreground">/ {modules.length} badges</div>
              </div>
              <div className="text-center p-4 rounded-lg bg-secondary">
                <Clock className="h-6 w-6 mx-auto mb-1 text-info" />
                <div className="text-2xl font-bold">
                  {startedAt 
                    ? Math.ceil((Date.now() - new Date(startedAt).getTime()) / (1000 * 60 * 60 * 24))
                    : 0
                  }
                </div>
                <div className="text-xs text-muted-foreground">jours depuis le début</div>
              </div>
              <div className="text-center p-4 rounded-lg bg-secondary">
                <Award className="h-6 w-6 mx-auto mb-1 text-accent" />
                <div className="text-2xl font-bold">
                  {overall === 100 ? '🎓' : `${Math.round(overall / 25)}/4`}
                </div>
                <div className="text-xs text-muted-foreground">
                  {overall === 100 ? 'Terminé !' : 'modules maîtrisés'}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Module Progress */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Progression par module</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {modules.map((module) => {
            const moduleProgress = getModuleProgress(module.id);
            const hasModuleBadge = hasBadge(module.id);
            
            return (
              <div key={module.id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {hasModuleBadge ? (
                      <CheckCircle2 className="h-4 w-4 text-accent" />
                    ) : (
                      <div className="h-4 w-4 rounded-full border-2 border-muted-foreground/30" />
                    )}
                    <span className="text-sm font-medium">{module.title}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {hasModuleBadge && (
                      <Badge className="bg-warning text-warning-foreground text-xs gap-1">
                        <Trophy className="h-3 w-3" />
                      </Badge>
                    )}
                    <span className="text-sm text-muted-foreground">{moduleProgress}%</span>
                  </div>
                </div>
                <Progress value={moduleProgress} className="h-2" />
              </div>
            );
          })}
        </CardContent>
      </Card>

      {/* Badges */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Trophy className="h-5 w-5 text-warning" />
            Badges & Accomplissements
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {modules.map((module) => {
              const hasModuleBadge = hasBadge(module.id);
              return (
                <div
                  key={module.id}
                  className={cn(
                    "text-center p-4 rounded-xl border-2 transition-all",
                    hasModuleBadge 
                      ? "border-warning bg-warning/10" 
                      : "border-border bg-muted/30 opacity-50"
                  )}
                >
                  <div className="text-3xl mb-2">
                    {hasModuleBadge ? '🏆' : '🔒'}
                  </div>
                  <p className="text-xs font-medium">{module.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Semaine {module.week}
                  </p>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Certificate */}
      {overall >= 80 && (
        <Card className="border-accent/30 bg-accent/5">
          <CardContent className="p-6 text-center">
            <Award className="h-12 w-12 mx-auto text-accent mb-3" />
            <h3 className="text-lg font-bold mb-1">
              {overall === 100 ? 'Félicitations ! 🎉' : 'Presque terminé !'}
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              {overall === 100 
                ? 'Vous avez complété le parcours DevOps & MLOps. Téléchargez votre certificat !'
                : `Encore ${100 - overall}% pour obtenir votre certificat de complétion.`
              }
            </p>
            <Button 
              onClick={handleDownloadCertificate}
              className="gap-2 bg-accent hover:bg-accent/90 text-accent-foreground"
              disabled={overall < 100}
            >
              <Download className="h-4 w-4" />
              Télécharger le certificat
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ProgressDashboard;
