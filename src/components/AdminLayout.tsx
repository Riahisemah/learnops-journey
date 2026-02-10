import { Link, Outlet, useLocation } from "react-router-dom";
import { useState } from "react";
import {
  BarChart3, Users, BookOpen, Video, HelpCircle, TrendingUp,
  Settings, Menu, LogOut, ChevronLeft
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useAuth } from "@/contexts/AuthContext";

const adminNav = [
  { label: "Vue d'ensemble", icon: BarChart3, path: "/admin" },
  { label: "Utilisateurs", icon: Users, path: "/admin/users" },
  { label: "Modules", icon: BookOpen, path: "/admin/modules" },
  { label: "Vidéos", icon: Video, path: "/admin/videos" },
  { label: "Quiz", icon: HelpCircle, path: "/admin/quizzes" },
  { label: "Statistiques", icon: TrendingUp, path: "/admin/analytics" },
  { label: "Paramètres", icon: Settings, path: "/admin/settings" },
];

function AdminNav({ onNavigate }: { onNavigate?: () => void }) {
  const location = useLocation();
  const { user, logout } = useAuth();

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-sidebar-border">
        <Link to="/admin" className="flex items-center gap-2" onClick={onNavigate}>
          <Settings className="h-6 w-6 text-accent" />
          <span className="font-bold text-lg">Admin Panel</span>
        </Link>
      </div>
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {adminNav.map(item => {
          const isActive = location.pathname === item.path || (item.path !== "/admin" && location.pathname.startsWith(item.path));
          const isExactAdmin = item.path === "/admin" && location.pathname === "/admin";
          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={onNavigate}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors",
                (isExactAdmin || (item.path !== "/admin" && isActive))
                  ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                  : "hover:bg-sidebar-accent/50 text-muted-foreground"
              )}
            >
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-sidebar-border space-y-2">
        <div className="flex items-center gap-2 text-sm">
          <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold text-xs">
            {user?.firstName?.[0]}{user?.lastName?.[0]}
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium truncate">{user?.firstName} {user?.lastName}</p>
            <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" asChild className="flex-1 justify-start gap-2">
            <Link to="/"><ChevronLeft className="h-3 w-3" /> Retour au site</Link>
          </Button>
          <ThemeToggle />
        </div>
      </div>
    </div>
  );
}

export default function AdminLayout() {
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen flex w-full">
      {/* Mobile header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 h-14 bg-background border-b border-border z-50 flex items-center justify-between px-4">
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon"><Menu className="h-5 w-5" /></Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-72 p-0">
            <AdminNav onNavigate={() => setOpen(false)} />
          </SheetContent>
        </Sheet>
        <span className="font-bold">Admin Panel</span>
        <ThemeToggle />
      </header>

      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-64 min-h-screen bg-sidebar border-r border-sidebar-border">
        <AdminNav />
      </aside>

      <main className="flex-1 pt-14 lg:pt-0 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
