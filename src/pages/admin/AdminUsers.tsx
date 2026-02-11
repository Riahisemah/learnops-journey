import { useState } from "react";
import { Search, MoreHorizontal, Eye, Edit2, Trash2, Ban, Download, UserPlus } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/contexts/AuthContext";
import type { User } from "@/data/mock-users";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const roleBadge: Record<string, string> = {
  admin: "bg-warning/10 text-warning border-warning/20",
  instructor: "bg-info/10 text-info border-info/20",
  student: "bg-accent/10 text-accent border-accent/20",
};
const roleLabel: Record<string, string> = { admin: "Admin", instructor: "Formateur", student: "Étudiant" };

export default function AdminUsers() {
  const { users, updateUserById, deleteUser, addUser } = useAuth();
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<User | null>(null);
  const [addOpen, setAddOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<User | null>(null);

  // Add user form state
  const [formData, setFormData] = useState({ firstName: "", lastName: "", email: "", password: "", role: "student" as User["role"] });

  const resetForm = () => setFormData({ firstName: "", lastName: "", email: "", password: "", role: "student" });

  const filtered = users.filter(u => {
    const matchSearch = `${u.firstName} ${u.lastName} ${u.email}`.toLowerCase().includes(search.toLowerCase());
    const matchRole = roleFilter === "all" || u.role === roleFilter;
    return matchSearch && matchRole;
  });

  const exportCSV = () => {
    const headers = "Nom,Email,Rôle,Progression,Statut,Dernière connexion\n";
    const rows = users.map(u =>
      `${u.firstName} ${u.lastName},${u.email},${roleLabel[u.role]},${u.progression}%,${u.status},${new Date(u.lastLogin).toLocaleDateString("fr-FR")}`
    ).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "utilisateurs.csv"; a.click();
    URL.revokeObjectURL(url);
    toast.success("Export CSV téléchargé");
  };

  const handleAddUser = () => {
    if (!formData.firstName || !formData.lastName || !formData.email || !formData.password) {
      toast.error("Veuillez remplir tous les champs");
      return;
    }
    if (users.some(u => u.email === formData.email.toLowerCase())) {
      toast.error("Un utilisateur avec cet email existe déjà");
      return;
    }
    addUser({
      firstName: formData.firstName,
      lastName: formData.lastName,
      email: formData.email.toLowerCase(),
      password: formData.password,
      role: formData.role,
      status: "active",
      progression: 0,
      modulesCompleted: [],
      badges: [],
      avatar: "",
    });
    setAddOpen(false);
    resetForm();
    toast.success("Utilisateur ajouté avec succès");
  };

  const handleEditUser = () => {
    if (!editTarget) return;
    updateUserById(editTarget.id, {
      firstName: formData.firstName,
      lastName: formData.lastName,
      email: formData.email.toLowerCase(),
      role: formData.role,
    });
    setEditTarget(null);
    resetForm();
    toast.success("Utilisateur modifié avec succès");
  };

  const openEdit = (u: User) => {
    setFormData({ firstName: u.firstName, lastName: u.lastName, email: u.email, password: "", role: u.role });
    setEditTarget(u);
  };

  const handleToggleBlock = (u: User) => {
    const newStatus = u.status === "active" ? "blocked" : "active";
    updateUserById(u.id, { status: newStatus });
    toast.success(newStatus === "blocked" ? `${u.firstName} a été bloqué` : `${u.firstName} a été débloqué`);
  };

  const handleDelete = () => {
    if (!deleteTarget) return;
    deleteUser(deleteTarget.id);
    setDeleteTarget(null);
    toast.success("Utilisateur supprimé");
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion utilisateurs</h1>
        <div className="flex gap-2">
          <Button size="sm" onClick={() => { resetForm(); setAddOpen(true); }} className="gap-2">
            <UserPlus className="h-4 w-4" /> Ajouter
          </Button>
          <Button size="sm" onClick={exportCSV} variant="outline" className="gap-2">
            <Download className="h-4 w-4" /> CSV
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Rechercher par nom ou email..." value={search} onChange={e => setSearch(e.target.value)} className="pl-9" />
          </div>
          <Select value={roleFilter} onValueChange={setRoleFilter}>
            <SelectTrigger className="w-full sm:w-40"><SelectValue placeholder="Rôle" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tous les rôles</SelectItem>
              <SelectItem value="student">Étudiants</SelectItem>
              <SelectItem value="instructor">Formateurs</SelectItem>
              <SelectItem value="admin">Admins</SelectItem>
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Utilisateur</TableHead>
                <TableHead className="hidden md:table-cell">Rôle</TableHead>
                <TableHead className="hidden md:table-cell">Progression</TableHead>
                <TableHead className="hidden lg:table-cell">Dernière connexion</TableHead>
                <TableHead className="hidden lg:table-cell">Statut</TableHead>
                <TableHead className="w-10"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map(u => (
                <TableRow key={u.id}>
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">
                        {u.firstName[0]}{u.lastName[0]}
                      </div>
                      <div>
                        <p className="font-medium text-sm">{u.firstName} {u.lastName}</p>
                        <p className="text-xs text-muted-foreground">{u.email}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    <Badge variant="outline" className={cn("text-xs", roleBadge[u.role])}>{roleLabel[u.role]}</Badge>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    <div className="flex items-center gap-2 w-24">
                      <Progress value={u.progression} className="h-1.5 flex-1" />
                      <span className="text-xs text-muted-foreground">{u.progression}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell text-sm text-muted-foreground">
                    {new Date(u.lastLogin).toLocaleDateString("fr-FR")}
                  </TableCell>
                  <TableCell className="hidden lg:table-cell">
                    <Badge variant={u.status === "active" ? "default" : "destructive"} className="text-xs">
                      {u.status === "active" ? "Actif" : "Bloqué"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8"><MoreHorizontal className="h-4 w-4" /></Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => setSelectedUser(u)} className="gap-2"><Eye className="h-4 w-4" /> Voir détails</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => openEdit(u)} className="gap-2"><Edit2 className="h-4 w-4" /> Modifier</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleToggleBlock(u)} className="gap-2">
                          <Ban className="h-4 w-4" /> {u.status === "active" ? "Bloquer" : "Débloquer"}
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => setDeleteTarget(u)} className="gap-2 text-destructive"><Trash2 className="h-4 w-4" /> Supprimer</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
              {filtered.length === 0 && (
                <TableRow><TableCell colSpan={6} className="text-center py-8 text-muted-foreground">Aucun utilisateur trouvé</TableCell></TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Detail dialog */}
      <Dialog open={!!selectedUser} onOpenChange={() => setSelectedUser(null)}>
        <DialogContent className="max-w-md">
          {selectedUser && (
            <>
              <DialogHeader>
                <DialogTitle>{selectedUser.firstName} {selectedUser.lastName}</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold">
                    {selectedUser.firstName[0]}{selectedUser.lastName[0]}
                  </div>
                  <div>
                    <p className="font-medium">{selectedUser.email}</p>
                    <Badge variant="outline" className={cn("text-xs mt-1", roleBadge[selectedUser.role])}>{roleLabel[selectedUser.role]}</Badge>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div><span className="text-muted-foreground">Progression</span><p className="font-semibold">{selectedUser.progression}%</p></div>
                  <div><span className="text-muted-foreground">Badges</span><p className="font-semibold">{selectedUser.badges.length}</p></div>
                  <div><span className="text-muted-foreground">Inscrit le</span><p className="font-semibold">{new Date(selectedUser.createdAt).toLocaleDateString("fr-FR")}</p></div>
                  <div><span className="text-muted-foreground">Dernière connexion</span><p className="font-semibold">{new Date(selectedUser.lastLogin).toLocaleDateString("fr-FR")}</p></div>
                  <div><span className="text-muted-foreground">Modules complétés</span><p className="font-semibold">{selectedUser.modulesCompleted.length}</p></div>
                  <div><span className="text-muted-foreground">Statut</span><p className="font-semibold">{selectedUser.status === "active" ? "Actif" : "Bloqué"}</p></div>
                </div>
                {selectedUser.badges.length > 0 && (
                  <div>
                    <span className="text-sm text-muted-foreground">Badges</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {selectedUser.badges.map(b => (
                        <Badge key={b} variant="secondary" className="text-xs">{b}</Badge>
                      ))}
                    </div>
                  </div>
                )}
                <div>
                  <span className="text-sm text-muted-foreground">Progression globale</span>
                  <Progress value={selectedUser.progression} className="h-2 mt-1" />
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>

      {/* Add user dialog */}
      <Dialog open={addOpen} onOpenChange={setAddOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader><DialogTitle>Ajouter un utilisateur</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <Label>Prénom</Label>
                <Input value={formData.firstName} onChange={e => setFormData(p => ({ ...p, firstName: e.target.value }))} />
              </div>
              <div className="space-y-2">
                <Label>Nom</Label>
                <Input value={formData.lastName} onChange={e => setFormData(p => ({ ...p, lastName: e.target.value }))} />
              </div>
            </div>
            <div className="space-y-2">
              <Label>Email</Label>
              <Input type="email" value={formData.email} onChange={e => setFormData(p => ({ ...p, email: e.target.value }))} />
            </div>
            <div className="space-y-2">
              <Label>Mot de passe</Label>
              <Input type="password" value={formData.password} onChange={e => setFormData(p => ({ ...p, password: e.target.value }))} />
            </div>
            <div className="space-y-2">
              <Label>Rôle</Label>
              <Select value={formData.role} onValueChange={v => setFormData(p => ({ ...p, role: v as User["role"] }))}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="student">Étudiant</SelectItem>
                  <SelectItem value="instructor">Formateur</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setAddOpen(false)}>Annuler</Button>
            <Button onClick={handleAddUser}>Ajouter</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit user dialog */}
      <Dialog open={!!editTarget} onOpenChange={() => setEditTarget(null)}>
        <DialogContent className="max-w-md">
          <DialogHeader><DialogTitle>Modifier l'utilisateur</DialogTitle></DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <Label>Prénom</Label>
                <Input value={formData.firstName} onChange={e => setFormData(p => ({ ...p, firstName: e.target.value }))} />
              </div>
              <div className="space-y-2">
                <Label>Nom</Label>
                <Input value={formData.lastName} onChange={e => setFormData(p => ({ ...p, lastName: e.target.value }))} />
              </div>
            </div>
            <div className="space-y-2">
              <Label>Email</Label>
              <Input type="email" value={formData.email} onChange={e => setFormData(p => ({ ...p, email: e.target.value }))} />
            </div>
            <div className="space-y-2">
              <Label>Rôle</Label>
              <Select value={formData.role} onValueChange={v => setFormData(p => ({ ...p, role: v as User["role"] }))}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="student">Étudiant</SelectItem>
                  <SelectItem value="instructor">Formateur</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setEditTarget(null)}>Annuler</Button>
            <Button onClick={handleEditUser}>Enregistrer</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete confirm */}
      <Dialog open={!!deleteTarget} onOpenChange={() => setDeleteTarget(null)}>
        <DialogContent className="max-w-sm">
          <DialogHeader><DialogTitle>Confirmer la suppression</DialogTitle></DialogHeader>
          <p className="text-sm text-muted-foreground">Supprimer {deleteTarget?.firstName} {deleteTarget?.lastName} ? Cette action est irréversible.</p>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={() => setDeleteTarget(null)}>Annuler</Button>
            <Button variant="destructive" onClick={handleDelete}>Supprimer</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
