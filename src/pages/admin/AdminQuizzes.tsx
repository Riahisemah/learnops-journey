import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Plus, Edit2, Trash2, HelpCircle, X } from "lucide-react";
import { modules } from "@/data/course-data";
import { toast } from "sonner";

interface QuizQuestion {
  question: string;
  type: "single" | "multiple";
  options: string[];
  correctIndices: number[];
  explanation: string;
}

interface QuizItem {
  id: string;
  title: string;
  module: string;
  questions: QuizQuestion[];
  avgScore: number;
  attempts: number;
}

const initialQuizzes: QuizItem[] = modules
  .flatMap(m => m.lessons.filter(l => l.type === "quiz").map(l => ({
    id: l.id,
    title: l.title,
    module: m.title,
    questions: [
      { question: "Question exemple 1", type: "single" as const, options: ["Option A", "Option B", "Option C", "Option D"], correctIndices: [0], explanation: "Explication de la réponse" },
      { question: "Question exemple 2", type: "multiple" as const, options: ["Option A", "Option B", "Option C"], correctIndices: [0, 2], explanation: "" },
    ],
    avgScore: Math.floor(Math.random() * 30 + 65),
    attempts: Math.floor(Math.random() * 100 + 20),
  })));

const emptyQuestion = (): QuizQuestion => ({ question: "", type: "single", options: ["", "", "", ""], correctIndices: [0], explanation: "" });

const moduleOptions = modules.map(m => m.title);

export default function AdminQuizzes() {
  const [quizzes, setQuizzes] = useState<QuizItem[]>(initialQuizzes);
  const [formOpen, setFormOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<QuizItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<QuizItem | null>(null);

  const [title, setTitle] = useState("");
  const [module_, setModule] = useState(moduleOptions[0] || "");
  const [questions, setQuestions] = useState<QuizQuestion[]>([emptyQuestion()]);

  const openAdd = () => {
    setTitle(""); setModule(moduleOptions[0] || ""); setQuestions([emptyQuestion()]);
    setEditTarget(null); setFormOpen(true);
  };

  const openEdit = (q: QuizItem) => {
    setTitle(q.title); setModule(q.module); setQuestions(q.questions.length > 0 ? q.questions : [emptyQuestion()]);
    setEditTarget(q); setFormOpen(true);
  };

  const handleSave = () => {
    if (!title) { toast.error("Titre requis"); return; }
    if (editTarget) {
      setQuizzes(prev => prev.map(q => q.id === editTarget.id ? { ...q, title, module: module_, questions } : q));
      toast.success("Quiz modifié");
    } else {
      setQuizzes(prev => [...prev, { id: `quiz-${Date.now()}`, title, module: module_, questions, avgScore: 0, attempts: 0 }]);
      toast.success("Quiz créé");
    }
    setFormOpen(false);
  };

  const handleDelete = () => {
    if (!deleteTarget) return;
    setQuizzes(prev => prev.filter(q => q.id !== deleteTarget.id));
    setDeleteTarget(null);
    toast.success("Quiz supprimé");
  };

  const updateQuestion = (idx: number, field: string, value: any) => {
    setQuestions(prev => prev.map((q, i) => i === idx ? { ...q, [field]: value } : q));
  };

  const updateOption = (qIdx: number, oIdx: number, value: string) => {
    setQuestions(prev => prev.map((q, i) => i === qIdx ? { ...q, options: q.options.map((o, j) => j === oIdx ? value : o) } : q));
  };

  const toggleCorrect = (qIdx: number, oIdx: number) => {
    setQuestions(prev => prev.map((q, i) => {
      if (i !== qIdx) return q;
      if (q.type === "single") return { ...q, correctIndices: [oIdx] };
      const has = q.correctIndices.includes(oIdx);
      return { ...q, correctIndices: has ? q.correctIndices.filter(c => c !== oIdx) : [...q.correctIndices, oIdx] };
    }));
  };

  const addOption = (qIdx: number) => {
    setQuestions(prev => prev.map((q, i) => i === qIdx ? { ...q, options: [...q.options, ""] } : q));
  };

  const removeOption = (qIdx: number, oIdx: number) => {
    setQuestions(prev => prev.map((q, i) => {
      if (i !== qIdx || q.options.length <= 2) return q;
      return { ...q, options: q.options.filter((_, j) => j !== oIdx), correctIndices: q.correctIndices.filter(c => c !== oIdx).map(c => c > oIdx ? c - 1 : c) };
    }));
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des quiz</h1>
        <Button size="sm" className="gap-2" onClick={openAdd}><Plus className="h-4 w-4" /> Créer un quiz</Button>
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
              {quizzes.map(q => (
                <TableRow key={q.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <HelpCircle className="h-4 w-4 text-accent" />
                      <span className="font-medium text-sm">{q.title}</span>
                    </div>
                  </TableCell>
                  <TableCell><Badge variant="outline" className="text-xs">{q.module}</Badge></TableCell>
                  <TableCell className="hidden md:table-cell text-sm">{q.questions.length}</TableCell>
                  <TableCell className="hidden md:table-cell">
                    <Badge className={q.avgScore >= 80 ? "bg-accent/10 text-accent" : q.avgScore >= 60 ? "bg-warning/10 text-warning" : "bg-destructive/10 text-destructive"}>
                      {q.avgScore}%
                    </Badge>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell text-sm text-muted-foreground">{q.attempts}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => openEdit(q)}><Edit2 className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => setDeleteTarget(q)}><Trash2 className="h-4 w-4" /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Quiz editor dialog */}
      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editTarget ? "Modifier le quiz" : "Créer un quiz"}</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <Label>Titre du quiz</Label>
                <Input value={title} onChange={e => setTitle(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label>Module</Label>
                <Select value={module_} onValueChange={setModule}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>{moduleOptions.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label className="text-base font-semibold">Questions</Label>
                <Button size="sm" variant="outline" onClick={() => setQuestions(p => [...p, emptyQuestion()])} className="gap-1">
                  <Plus className="h-3 w-3" /> Ajouter
                </Button>
              </div>

              {questions.map((q, qIdx) => (
                <Card key={qIdx}>
                  <CardContent className="p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-muted-foreground">Question {qIdx + 1}</span>
                      <div className="flex items-center gap-2">
                        <Select value={q.type} onValueChange={v => updateQuestion(qIdx, "type", v)}>
                          <SelectTrigger className="h-7 text-xs w-32"><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="single">Choix unique</SelectItem>
                            <SelectItem value="multiple">Choix multiples</SelectItem>
                          </SelectContent>
                        </Select>
                        {questions.length > 1 && (
                          <Button variant="ghost" size="icon" className="h-6 w-6 text-destructive" onClick={() => setQuestions(p => p.filter((_, i) => i !== qIdx))}>
                            <X className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs">Énoncé</Label>
                      <Textarea value={q.question} onChange={e => updateQuestion(qIdx, "question", e.target.value)} rows={2} className="text-sm" />
                    </div>

                    <div className="space-y-2">
                      <Label className="text-xs">Réponses (cocher les correctes)</Label>
                      {q.options.map((opt, oIdx) => (
                        <div key={oIdx} className="flex items-center gap-2">
                          <Checkbox
                            checked={q.correctIndices.includes(oIdx)}
                            onCheckedChange={() => toggleCorrect(qIdx, oIdx)}
                          />
                          <Input
                            value={opt}
                            onChange={e => updateOption(qIdx, oIdx, e.target.value)}
                            placeholder={`Option ${oIdx + 1}`}
                            className="h-8 text-sm flex-1"
                          />
                          {q.options.length > 2 && (
                            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => removeOption(qIdx, oIdx)}>
                              <X className="h-3 w-3" />
                            </Button>
                          )}
                        </div>
                      ))}
                      <Button size="sm" variant="ghost" onClick={() => addOption(qIdx)} className="text-xs gap-1">
                        <Plus className="h-3 w-3" /> Option
                      </Button>
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs">Explication (optionnel)</Label>
                      <Input value={q.explanation} onChange={e => updateQuestion(qIdx, "explanation", e.target.value)} className="h-8 text-sm" />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setFormOpen(false)}>Annuler</Button>
            <Button onClick={handleSave}>{editTarget ? "Enregistrer" : "Créer"}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirm */}
      <Dialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)}>
        <DialogContent className="max-w-sm">
          <DialogHeader><DialogTitle>Supprimer le quiz</DialogTitle></DialogHeader>
          <p className="text-sm text-muted-foreground">Supprimer « {deleteTarget?.title} » ?</p>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setDeleteTarget(null)}>Annuler</Button>
            <Button variant="destructive" onClick={handleDelete}>Supprimer</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
