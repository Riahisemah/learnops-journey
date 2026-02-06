import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { 
  GitBranch, 
  Brain, 
  Rocket, 
  Award, 
  Home,
  Trophy,
  BookOpen,
  Menu,
  X,
  BarChart3
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { modules } from "@/data/course-data";
import { useProgress } from "@/hooks/use-progress";
import { Progress } from "@/components/ui/progress";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  GitBranch,
  Brain,
  Rocket,
  Award,
};

interface SidebarContentProps {
  onNavigate?: () => void;
}

function SidebarContentInner({ onNavigate }: SidebarContentProps) {
  const location = useLocation();
  const { getModuleProgress, getOverallProgress, getBadgesCount, getCompletedLessonsCount } = useProgress();
  
  return (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="p-4 border-b border-sidebar-border">
        <Link to="/" className="flex items-center gap-2" onClick={onNavigate}>
          <BookOpen className="h-6 w-6 text-accent" />
          <span className="font-bold text-lg">DevOps & MLOps</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        <Link
          to="/"
          onClick={onNavigate}
          className={cn(
            "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
            location.pathname === "/" 
              ? "bg-sidebar-accent text-sidebar-accent-foreground" 
              : "hover:bg-sidebar-accent/50"
          )}
        >
          <Home className="h-5 w-5" />
          <span>Accueil</span>
        </Link>

        <Link
          to="/dashboard"
          onClick={onNavigate}
          className={cn(
            "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
            location.pathname === "/dashboard" 
              ? "bg-sidebar-accent text-sidebar-accent-foreground" 
              : "hover:bg-sidebar-accent/50"
          )}
        >
          <BarChart3 className="h-5 w-5" />
          <span>Tableau de bord</span>
        </Link>

        <div className="pt-4">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-3">
            Modules
          </span>
        </div>

        {modules.map((module) => {
          const IconComponent = iconMap[module.icon] || BookOpen;
          const progress = getModuleProgress(module.id);
          const isActive = location.pathname.includes(`/module/${module.id}`);
          
          return (
            <Link
              key={module.id}
              to={`/module/${module.id}`}
              onClick={onNavigate}
              className={cn(
                "flex flex-col gap-2 px-3 py-3 rounded-lg transition-colors",
                isActive 
                  ? "bg-sidebar-accent text-sidebar-accent-foreground" 
                  : "hover:bg-sidebar-accent/50"
              )}
            >
              <div className="flex items-center gap-3">
                <IconComponent className="h-5 w-5" />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Semaine {module.week}</span>
                    <span className="text-xs font-medium">{progress}%</span>
                  </div>
                  <span className="font-medium text-sm">{module.title}</span>
                </div>
              </div>
              <Progress value={progress} className="h-1.5" />
            </Link>
          );
        })}
      </nav>

      {/* Stats footer */}
      <div className="p-4 border-t border-sidebar-border space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">Progression globale</span>
          <span className="font-semibold">{getOverallProgress()}%</span>
        </div>
        <Progress value={getOverallProgress()} className="h-2" />
        
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-2 text-sm">
            <Trophy className="h-4 w-4 text-warning" />
            <span>{getBadgesCount()}/4 badges</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <BookOpen className="h-4 w-4" />
            <span>{getCompletedLessonsCount()} leçons</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export function AppSidebar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 h-14 bg-background border-b border-border z-50 flex items-center justify-between px-4">
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-72 p-0">
            <SidebarContentInner onNavigate={() => setOpen(false)} />
          </SheetContent>
        </Sheet>
        
        <span className="font-bold">DevOps & MLOps</span>
        
        <ThemeToggle />
      </header>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-72 min-h-screen bg-sidebar border-r border-sidebar-border">
        <SidebarContentInner />
        <div className="p-4 border-t border-sidebar-border">
          <ThemeToggle />
        </div>
      </aside>
    </>
  );
}
