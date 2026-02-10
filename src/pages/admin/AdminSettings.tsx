import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Save } from "lucide-react";

export default function AdminSettings() {
  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold">Paramètres</h1>

      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">Général</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Sécurité</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Informations de la plateforme</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Nom de la plateforme</Label>
                <Input defaultValue="DevOps & MLOps Academy" />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Input defaultValue="Plateforme d'apprentissage DevOps et MLOps" />
              </div>
              <Button size="sm" className="gap-2"><Save className="h-4 w-4" /> Enregistrer</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Préférences de notification</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Nouvelles inscriptions</p>
                  <p className="text-xs text-muted-foreground">Recevoir un email lors d'une nouvelle inscription</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Complétion de module</p>
                  <p className="text-xs text-muted-foreground">Notification quand un étudiant complète un module</p>
                </div>
                <Switch />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Rapport hebdomadaire</p>
                  <p className="text-xs text-muted-foreground">Résumé de la semaine par email</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Politique de sécurité</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Longueur minimum du mot de passe</Label>
                <Select defaultValue="8">
                  <SelectTrigger className="w-32"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="6">6 caractères</SelectItem>
                    <SelectItem value="8">8 caractères</SelectItem>
                    <SelectItem value="12">12 caractères</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Expiration de session</p>
                  <p className="text-xs text-muted-foreground">Déconnexion automatique après inactivité</p>
                </div>
                <Switch defaultChecked />
              </div>
              <Button size="sm" className="gap-2"><Save className="h-4 w-4" /> Enregistrer</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
