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
import { useAdminUsers } from "@/hooks/use-api";
import { adminService } from "@/services/adminService";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const roleBadge: Record<string, string> = {
  admin: "bg-warning/10 text-warning border-warning/20",
  instructor: "bg-info/10 text-info border-info/20",
  student: "bg-accent/10 text-accent border-accent/20",
};
const roleLabel: Record<string, string> = { admin: "Admin", instructor: "Formateur", student: "Étudiant" };

export default function AdminUsers() {
  const { data: users = [], refetch } = useAdminUsers();
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [selectedUser, setSelectedUser] = useState<any | null>(null);

  const filtered = users.filter((u: any) => {
    const name = `${u.first_name || ''} ${u.last_name || ''} ${u.email || ''}`.toLowerCase();
    const matchSearch = name.includes(search.toLowerCase());
    const matchRole = roleFilter === "all" || u.role === roleFilter;
    return matchSearch && matchRole;
  });

  const exportCSV = () => {
    const headers = "Nom,Email,Rôle,Statut\n";
    const rows = users.map((u: any) =>
      `${u.first_name || ''} ${u.last_name || ''},${u.email},${roleLabel[u.role] || u.role},${u.is_active ? 'Actif' : 'Inactif'}`
    ).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "utilisateurs.csv"; a.click();
    URL.revokeObjectURL(url);
    toast.success("Export CSV téléchargé");
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-7xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestion utilisateurs</h1>
        <div className="flex gap-2">
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
                <TableHead className="hidden lg:table-cell">Dernière connexion</TableHead>
                <TableHead className="hidden lg:table-cell">Statut</TableHead>
                <TableHead className="w-10"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((u: any) => (
                <TableRow key={u.id}>
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <div className="h-8 w-8 rounded-full bg-accent/20 flex items-center justify-center text-xs font-bold text-accent">
                        {(u.first_name || '?')[0]}{(u.last_name || '?')[0]}
                      </div>
                      <div>
                        <p className="font-medium text-sm">{u.first_name} {u.last_name}</p>
                        <p className="text-xs text-muted-foreground">{u.email}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    <Badge variant="outline" className={cn("text-xs", roleBadge[u.role])}>{roleLabel[u.role] || u.role}</Badge>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell text-sm text-muted-foreground">
                    {u.last_login ? new Date(u.last_login).toLocaleDateString("fr-FR") : "—"}
                  </TableCell>
                  <TableCell className="hidden lg:table-cell">
                    <Badge variant={u.is_active !== false ? "default" : "destructive"} className="text-xs">
                      {u.is_active !== false ? "Actif" : "Inactif"}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setSelectedUser(u)}>
                      <Eye className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {filtered.length === 0 && (
                <TableRow><TableCell colSpan={5} className="text-center py-8 text-muted-foreground">Aucun utilisateur trouvé</TableCell></TableRow>
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
                <DialogTitle>{selectedUser.first_name} {selectedUser.last_name}</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-full bg-accent/20 flex items-center justify-center text-accent font-bold">
                    {(selectedUser.first_name || '?')[0]}{(selectedUser.last_name || '?')[0]}
                  </div>
                  <div>
                    <p className="font-medium">{selectedUser.email}</p>
                    <Badge variant="outline" className={cn("text-xs mt-1", roleBadge[selectedUser.role])}>{roleLabel[selectedUser.role] || selectedUser.role}</Badge>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div><span className="text-muted-foreground">Inscrit le</span><p className="font-semibold">{selectedUser.created_at ? new Date(selectedUser.created_at).toLocaleDateString("fr-FR") : "—"}</p></div>
                  <div><span className="text-muted-foreground">Dernière connexion</span><p className="font-semibold">{selectedUser.last_login ? new Date(selectedUser.last_login).toLocaleDateString("fr-FR") : "—"}</p></div>
                  <div><span className="text-muted-foreground">Statut</span><p className="font-semibold">{selectedUser.is_active !== false ? "Actif" : "Inactif"}</p></div>
                  <div><span className="text-muted-foreground">Rôle</span><p className="font-semibold">{roleLabel[selectedUser.role] || selectedUser.role}</p></div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
