import { modules } from "@/data/course-data";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, Clock, Users, Copy, Trash2, Edit2, GripVertical } from "lucide-react";

export default function AdminModules() {
  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des modules</h1>
        <Button size="sm" className="gap-2"><BookOpen className="h-4 w-4" /> Ajouter un module</Button>
      </div>

      <div className="grid gap-4">
        {modules.map(m => {
          const totalMin = m.lessons.reduce((a, l) => a + l.duration, 0);
          return (
            <Card key={m.id} className="group hover:shadow-md transition-shadow">
              <CardContent className="p-5">
                <div className="flex items-start gap-4">
                  <div className="mt-1 text-muted-foreground cursor-grab"><GripVertical className="h-5 w-5" /></div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="outline" className="text-xs">Semaine {m.week}</Badge>
                      <Badge className="bg-accent/10 text-accent border-accent/20 text-xs">Publié</Badge>
                    </div>
                    <h3 className="font-semibold text-lg">{m.title}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{m.description}</p>
                    <div className="flex items-center gap-4 mt-3 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1"><BookOpen className="h-3.5 w-3.5" />{m.lessons.length} leçons</span>
                      <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" />{totalMin} min</span>
                      <span className="flex items-center gap-1"><Users className="h-3.5 w-3.5" />{Math.floor(Math.random() * 50 + 10)} étudiants</span>
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8"><Edit2 className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8"><Copy className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive"><Trash2 className="h-4 w-4" /></Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
