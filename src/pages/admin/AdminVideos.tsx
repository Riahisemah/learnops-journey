import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Edit2, Trash2, Upload, Eye, Clock } from "lucide-react";

const mockVideos = [
  { id: 1, title: "Introduction au DevOps", module: "DevOps Basics", duration: "3:24", views: 234, completions: 189 },
  { id: 2, title: "CI/CD avec GitHub Actions", module: "DevOps Basics", duration: "5:15", views: 198, completions: 156 },
  { id: 3, title: "Docker Fondamentaux", module: "DevOps Basics", duration: "4:30", views: 176, completions: 134 },
  { id: 4, title: "Versioning avec DVC", module: "MLOps Fundamentals", duration: "6:00", views: 145, completions: 112 },
  { id: 5, title: "MLflow Tracking", module: "MLOps Fundamentals", duration: "5:45", views: 132, completions: 98 },
  { id: 6, title: "FastAPI pour ML", module: "Déploiement & API", duration: "4:20", views: 120, completions: 89 },
  { id: 7, title: "Déploiement Cloud", module: "Déploiement & API", duration: "7:10", views: 98, completions: 67 },
  { id: 8, title: "Monitoring ML", module: "Déploiement & API", duration: "5:30", views: 87, completions: 56 },
];

export default function AdminVideos() {
  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des vidéos</h1>
        <Button size="sm" className="gap-2"><Upload className="h-4 w-4" /> Uploader une vidéo</Button>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {mockVideos.map(v => (
          <Card key={v.id} className="group overflow-hidden hover:shadow-md transition-shadow">
            <div className="relative aspect-video bg-muted flex items-center justify-center">
              <Play className="h-10 w-10 text-muted-foreground/50" />
              <Badge className="absolute top-2 right-2 bg-background/80 text-foreground text-xs">{v.duration}</Badge>
            </div>
            <CardContent className="p-3 space-y-2">
              <h3 className="font-medium text-sm line-clamp-1">{v.title}</h3>
              <Badge variant="outline" className="text-xs">{v.module}</Badge>
              <div className="flex items-center gap-3 text-xs text-muted-foreground">
                <span className="flex items-center gap-1"><Eye className="h-3 w-3" />{v.views}</span>
                <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{v.completions} complétions</span>
              </div>
              <div className="flex gap-1 pt-1">
                <Button variant="ghost" size="icon" className="h-7 w-7"><Edit2 className="h-3.5 w-3.5" /></Button>
                <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive"><Trash2 className="h-3.5 w-3.5" /></Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
