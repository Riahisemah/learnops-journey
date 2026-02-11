import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Play, Edit2, Trash2, Upload, Eye, Clock, Plus } from "lucide-react";
import { toast } from "sonner";

interface VideoItem {
  id: number;
  title: string;
  module: string;
  duration: string;
  views: number;
  completions: number;
  url: string;
}

const initialVideos: VideoItem[] = [
  { id: 1, title: "Introduction au DevOps", module: "DevOps Basics", duration: "3:24", views: 234, completions: 189, url: "" },
  { id: 2, title: "CI/CD avec GitHub Actions", module: "DevOps Basics", duration: "5:15", views: 198, completions: 156, url: "" },
  { id: 3, title: "Docker Fondamentaux", module: "DevOps Basics", duration: "4:30", views: 176, completions: 134, url: "" },
  { id: 4, title: "Versioning avec DVC", module: "MLOps Fundamentals", duration: "6:00", views: 145, completions: 112, url: "" },
  { id: 5, title: "MLflow Tracking", module: "MLOps Fundamentals", duration: "5:45", views: 132, completions: 98, url: "" },
  { id: 6, title: "FastAPI pour ML", module: "Déploiement & API", duration: "4:20", views: 120, completions: 89, url: "" },
  { id: 7, title: "Déploiement Cloud", module: "Déploiement & API", duration: "7:10", views: 98, completions: 67, url: "" },
  { id: 8, title: "Monitoring ML", module: "Déploiement & API", duration: "5:30", views: 87, completions: 56, url: "" },
];

const moduleOptions = ["DevOps Basics", "MLOps Fundamentals", "Déploiement & API", "Évaluation finale"];

export default function AdminVideos() {
  const [videos, setVideos] = useState<VideoItem[]>(initialVideos);
  const [formOpen, setFormOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<VideoItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<VideoItem | null>(null);
  const [form, setForm] = useState({ title: "", module: moduleOptions[0], duration: "", url: "" });

  const resetForm = () => setForm({ title: "", module: moduleOptions[0], duration: "", url: "" });

  const openAdd = () => { resetForm(); setEditTarget(null); setFormOpen(true); };
  const openEdit = (v: VideoItem) => {
    setForm({ title: v.title, module: v.module, duration: v.duration, url: v.url });
    setEditTarget(v);
    setFormOpen(true);
  };

  const handleSave = () => {
    if (!form.title || !form.duration) { toast.error("Titre et durée requis"); return; }
    if (editTarget) {
      setVideos(prev => prev.map(v => v.id === editTarget.id ? { ...v, title: form.title, module: form.module, duration: form.duration, url: form.url } : v));
      toast.success("Vidéo modifiée");
    } else {
      setVideos(prev => [...prev, { id: Date.now(), title: form.title, module: form.module, duration: form.duration, url: form.url, views: 0, completions: 0 }]);
      toast.success("Vidéo ajoutée");
    }
    setFormOpen(false);
  };

  const handleDelete = () => {
    if (!deleteTarget) return;
    setVideos(prev => prev.filter(v => v.id !== deleteTarget.id));
    setDeleteTarget(null);
    toast.success("Vidéo supprimée");
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion des vidéos</h1>
        <Button size="sm" className="gap-2" onClick={openAdd}><Upload className="h-4 w-4" /> Ajouter une vidéo</Button>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {videos.map(v => (
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
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => openEdit(v)}><Edit2 className="h-3.5 w-3.5" /></Button>
                <Button variant="ghost" size="icon" className="h-7 w-7 text-destructive" onClick={() => setDeleteTarget(v)}><Trash2 className="h-3.5 w-3.5" /></Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Add/Edit dialog */}
      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader><DialogTitle>{editTarget ? "Modifier la vidéo" : "Ajouter une vidéo"}</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2"><Label>Titre</Label><Input value={form.title} onChange={e => setForm(p => ({ ...p, title: e.target.value }))} /></div>
            <div className="space-y-2">
              <Label>Module</Label>
              <Select value={form.module} onValueChange={v => setForm(p => ({ ...p, module: v }))}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>{moduleOptions.map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <div className="space-y-2"><Label>Durée (ex: 5:30)</Label><Input value={form.duration} onChange={e => setForm(p => ({ ...p, duration: e.target.value }))} placeholder="3:24" /></div>
            <div className="space-y-2"><Label>URL de la vidéo</Label><Input value={form.url} onChange={e => setForm(p => ({ ...p, url: e.target.value }))} placeholder="https://..." /></div>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setFormOpen(false)}>Annuler</Button>
            <Button onClick={handleSave}>{editTarget ? "Enregistrer" : "Ajouter"}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirm */}
      <Dialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)}>
        <DialogContent className="max-w-sm">
          <DialogHeader><DialogTitle>Supprimer la vidéo</DialogTitle></DialogHeader>
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
