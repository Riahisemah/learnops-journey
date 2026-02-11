import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Save, Copy, Eye, EyeOff } from "lucide-react";
import { toast } from "sonner";

export default function AdminSettings() {
  const [platformName, setPlatformName] = useState("DevOps & MLOps Academy");
  const [platformDesc, setPlatformDesc] = useState("Plateforme d'apprentissage DevOps et MLOps");
  const [minPwdLength, setMinPwdLength] = useState("8");
  const [sessionExpiry, setSessionExpiry] = useState(true);
  const [notifSignup, setNotifSignup] = useState(true);
  const [notifCompletion, setNotifCompletion] = useState(false);
  const [notifWeekly, setNotifWeekly] = useState(true);
  const [apiKey] = useState("sk_live_devops_mlops_2025_xxxx");
  const [showApiKey, setShowApiKey] = useState(false);
  const [webhookUrl, setWebhookUrl] = useState("");

  const handleSaveGeneral = () => {
    toast.success("Paramètres généraux enregistrés");
  };

  const handleSaveNotifications = () => {
    toast.success("Préférences de notifications enregistrées");
  };

  const handleSaveSecurity = () => {
    toast.success("Politique de sécurité enregistrée");
  };

  const handleSaveIntegrations = () => {
    toast.success("Intégrations enregistrées");
  };

  const copyApiKey = () => {
    navigator.clipboard.writeText(apiKey);
    toast.success("Clé API copiée");
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold">Paramètres</h1>

      <Tabs defaultValue="general">
        <TabsList>
          <TabsTrigger value="general">Général</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Sécurité</TabsTrigger>
          <TabsTrigger value="integrations">Intégrations</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Informations de la plateforme</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Nom de la plateforme</Label>
                <Input value={platformName} onChange={e => setPlatformName(e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Input value={platformDesc} onChange={e => setPlatformDesc(e.target.value)} />
              </div>
              <Button size="sm" className="gap-2" onClick={handleSaveGeneral}><Save className="h-4 w-4" /> Enregistrer</Button>
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
                <Switch checked={notifSignup} onCheckedChange={setNotifSignup} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Complétion de module</p>
                  <p className="text-xs text-muted-foreground">Notification quand un étudiant complète un module</p>
                </div>
                <Switch checked={notifCompletion} onCheckedChange={setNotifCompletion} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-sm">Rapport hebdomadaire</p>
                  <p className="text-xs text-muted-foreground">Résumé de la semaine par email</p>
                </div>
                <Switch checked={notifWeekly} onCheckedChange={setNotifWeekly} />
              </div>
              <Button size="sm" className="gap-2" onClick={handleSaveNotifications}><Save className="h-4 w-4" /> Enregistrer</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Politique de sécurité</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Longueur minimum du mot de passe</Label>
                <Select value={minPwdLength} onValueChange={setMinPwdLength}>
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
                <Switch checked={sessionExpiry} onCheckedChange={setSessionExpiry} />
              </div>
              <Button size="sm" className="gap-2" onClick={handleSaveSecurity}><Save className="h-4 w-4" /> Enregistrer</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-4 mt-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Clé API</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Clé API de la plateforme</Label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      value={showApiKey ? apiKey : "•".repeat(apiKey.length)}
                      readOnly
                      className="pr-10 font-mono text-sm"
                    />
                    <Button variant="ghost" size="icon" className="absolute right-0 top-0 h-full" onClick={() => setShowApiKey(!showApiKey)}>
                      {showApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                  <Button variant="outline" size="icon" onClick={copyApiKey}><Copy className="h-4 w-4" /></Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-base">Webhook</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>URL du webhook</Label>
                <Input value={webhookUrl} onChange={e => setWebhookUrl(e.target.value)} placeholder="https://votre-service.com/webhook" />
                <p className="text-xs text-muted-foreground">Les événements (inscription, complétion, quiz) seront envoyés à cette URL</p>
              </div>
              <Button size="sm" className="gap-2" onClick={handleSaveIntegrations}><Save className="h-4 w-4" /> Enregistrer</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
