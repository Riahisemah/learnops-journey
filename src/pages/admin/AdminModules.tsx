import { useState } from "react";
import { modules as courseModules, type Module, type Lesson } from "@/data/course-data";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { BookOpen, Clock, Users, Copy, Trash2, Edit2, GripVertical, Plus, X } from "lucide-react";
import { toast } from "sonner";

interface ModuleFormData {
  title: string;
  description: string;
  week: number;
  lessons: { title: string; type: string; duration: number; description: string }[];
}

const emptyLesson = () => ({ title: "", type: "text", duration: 15, description: "" });
const emptyModule = (): ModuleFormData => ({ title: "", description: "", week: 1, lessons: [emptyLesson()] });

export default function AdminModules() {
  const [localModules, setLocalModules] = useState(courseModules);
  const [formOpen, setFormOpen] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Module | null>(null);
  const [form, setForm] = useState<ModuleFormData>(emptyModule());

  const openAdd = () => { setForm(emptyModule()); setEditId(null); setFormOpen(true); };

  const openEdit = (m: Module) => {
    setForm({
      title: m.title,
      description: m.description,
      week: m.week,
      lessons: m.lessons.map(l => ({ title: l.title, type: l.type, duration: l.duration, description: l.description })),
    });
    setEditId(m.id);
    setFormOpen(true);
  };

  const handleDuplicate = (m: Module) => {
    const dup: Module = {
      ...m,
      id: `${m.id}-copy-${Date.now()}`,
      title: `${m.title} (copie)`,
      lessons: m.lessons.map(l => ({ ...l, id: `${l.id}-copy-${Date.now()}` })),
    };
    setLocalModules(prev => [...prev, dup]);
    toast.success("Module dupliqué");
  };

  const handleDelete = () => {
    if (!deleteTarget) return;
    setLocalModules(prev => prev.filter(m => m.id !== deleteTarget.id));
    setDeleteTarget(null);
    toast.success("Module supprimé");
  };

  const handleSave = () => {
    if (!form.title || !form.description) {
      toast.error("Titre et description requis");
      return;
    }
    if (editId) {
      setLocalModules(prev => prev.map(m => m.id === editId ? {
        ...m,
        title: form.title,
        description: form.description,
        week: form.week,
        lessons: form.lessons.map((l, i) => ({
          id: m.lessons[i]?.id || `lesson-${Date.now()}-${i}`,
          title: l.title,
          type: l.type as Lesson["type"],
          duration: l.duration,
          description: l.description,
        })),
      } : m));
      toast.success("Module modifié");
    } else {
      const newModule: Module = {
        id: `module-${Date.now()}`,
        title: form.title,
        description: form.description,
        week: form.week,
        icon: "BookOpen",
        lessons: form.lessons.map((l, i) => ({
          id: `lesson-${Date.now()}-${i}`,
          title: l.title,
          type: l.type as Lesson["type"],
          duration: l.duration,
          description: l.description,
        })),
      };
      setLocalModules(prev => [...prev, newModule]);
      toast.success("Module créé");
    }
    setFormOpen(false);
  };

  const updateLesson = (idx: number, field: string, value: any) => {
    setForm(prev => ({
      ...prev,
      lessons: prev.lessons.map((l, i) => i === idx ? { ...l, [field]: value } : l),
    }));
  };

  const addLesson = () => setForm(prev => ({ ...prev, lessons: [...prev.lessons, emptyLesson()] }));
  const removeLesson = (idx: number) => setForm(prev => ({ ...prev, lessons: prev.lessons.filter((_, i) => i !== idx) }));

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des modules</h1>
        <Button size="sm" className="gap-2" onClick={openAdd}><BookOpen className="h-4 w-4" /> Ajouter un module</Button>
      </div>

      <div className="grid gap-4">
        {localModules.map(m => {
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
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => openEdit(m)}><Edit2 className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => handleDuplicate(m)}><Copy className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive" onClick={() => setDeleteTarget(m)}><Trash2 className="h-4 w-4" /></Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Add/Edit module dialog */}
      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader><DialogTitle>{editId ? "Modifier le module" : "Nouveau module"}</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2 col-span-2 sm:col-span-1">
                <Label>Titre du module</Label>
                <Input value={form.title} onChange={e => setForm(p => ({ ...p, title: e.target.value }))} />
              </div>
              <div className="space-y-2">
                <Label>Semaine</Label>
                <Select value={String(form.week)} onValueChange={v => setForm(p => ({ ...p, week: Number(v) }))}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {[1,2,3,4,5,6].map(w => <SelectItem key={w} value={String(w)}>Semaine {w}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-2">
              <Label>Description</Label>
              <Textarea value={form.description} onChange={e => setForm(p => ({ ...p, description: e.target.value }))} rows={2} />
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Label className="text-base font-semibold">Leçons</Label>
                <Button size="sm" variant="outline" onClick={addLesson} className="gap-1"><Plus className="h-3 w-3" /> Ajouter</Button>
              </div>
              {form.lessons.map((lesson, idx) => (
                <Card key={idx}>
                  <CardContent className="p-3 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-muted-foreground">Leçon {idx + 1}</span>
                      {form.lessons.length > 1 && (
                        <Button variant="ghost" size="icon" className="h-6 w-6 text-destructive" onClick={() => removeLesson(idx)}>
                          <X className="h-3 w-3" />
                        </Button>
                      )}
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <div className="col-span-2 space-y-1">
                        <Label className="text-xs">Titre</Label>
                        <Input value={lesson.title} onChange={e => updateLesson(idx, "title", e.target.value)} className="h-8 text-sm" />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">Type</Label>
                        <Select value={lesson.type} onValueChange={v => updateLesson(idx, "type", v)}>
                          <SelectTrigger className="h-8 text-sm"><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="text">Texte</SelectItem>
                            <SelectItem value="video">Vidéo</SelectItem>
                            <SelectItem value="quiz">Quiz</SelectItem>
                            <SelectItem value="practice">Pratique</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-2">
                      <div className="col-span-2 space-y-1">
                        <Label className="text-xs">Description</Label>
                        <Input value={lesson.description} onChange={e => updateLesson(idx, "description", e.target.value)} className="h-8 text-sm" />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">Durée (min)</Label>
                        <Input type="number" value={lesson.duration} onChange={e => updateLesson(idx, "duration", Number(e.target.value))} className="h-8 text-sm" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setFormOpen(false)}>Annuler</Button>
            <Button onClick={handleSave}>{editId ? "Enregistrer" : "Créer"}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirm */}
      <Dialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)}>
        <DialogContent className="max-w-sm">
          <DialogHeader><DialogTitle>Supprimer le module</DialogTitle></DialogHeader>
          <p className="text-sm text-muted-foreground">Supprimer « {deleteTarget?.title} » et toutes ses leçons ? Cette action est irréversible.</p>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setDeleteTarget(null)}>Annuler</Button>
            <Button variant="destructive" onClick={handleDelete}>Supprimer</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
