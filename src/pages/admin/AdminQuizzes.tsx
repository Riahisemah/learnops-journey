import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Edit2, Trash2, HelpCircle } from "lucide-react";
import { modules } from "@/data/course-data";

const mockQuizzes = modules
  .flatMap(m => m.lessons.filter(l => l.type === "quiz").map(l => ({
    id: l.id,
    title: l.title,
    module: m.title,
    questions: 5,
    avgScore: Math.floor(Math.random() * 30 + 65),
    attempts: Math.floor(Math.random() * 100 + 20),
  })));

export default function AdminQuizzes() {
  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des quiz</h1>
        <Button size="sm" className="gap-2"><Plus className="h-4 w-4" /> Créer un quiz</Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Quiz</TableHead>
                <TableHead>Module</TableHead>
                <TableHead className="hidden md:table-cell">Questions</TableHead>
                <TableHead className="hidden md:table-cell">Score moyen</TableHead>
                <TableHead className="hidden lg:table-cell">Tentatives</TableHead>
                <TableHead className="w-10"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockQuizzes.map(q => (
                <TableRow key={q.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <HelpCircle className="h-4 w-4 text-accent" />
                      <span className="font-medium text-sm">{q.title}</span>
                    </div>
                  </TableCell>
                  <TableCell><Badge variant="outline" className="text-xs">{q.module}</Badge></TableCell>
                  <TableCell className="hidden md:table-cell text-sm">{q.questions}</TableCell>
                  <TableCell className="hidden md:table-cell">
                    <Badge className={q.avgScore >= 80 ? "bg-accent/10 text-accent" : q.avgScore >= 60 ? "bg-warning/10 text-warning" : "bg-destructive/10 text-destructive"}>
                      {q.avgScore}%
                    </Badge>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell text-sm text-muted-foreground">{q.attempts}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8"><Edit2 className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive"><Trash2 className="h-4 w-4" /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
