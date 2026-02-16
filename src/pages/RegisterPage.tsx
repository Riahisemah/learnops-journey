import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen, Loader2, Check, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/contexts/AuthContext";
import { cn } from "@/lib/utils";

function getPasswordStrength(pw: string) {
  let score = 0;
  if (pw.length >= 8) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;
  return score;
}

const strengthLabels = ["Très faible", "Faible", "Moyen", "Bon", "Fort"];
const strengthColors = ["bg-destructive", "bg-destructive", "bg-warning", "bg-info", "bg-accent"];

export default function RegisterPage() {
  const [first_name, setfirst_name] = useState("");
  const [last_name, setlast_name] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState<"student" | "instructor" | "admin">("student");
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [error, setError] = useState("");
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();

  const strength = getPasswordStrength(password);
  const passwordChecks = [
    { label: "8 caractères minimum", valid: password.length >= 8 },
    { label: "1 majuscule", valid: /[A-Z]/.test(password) },
    { label: "1 chiffre", valid: /[0-9]/.test(password) },
    { label: "1 caractère spécial", valid: /[^A-Za-z0-9]/.test(password) },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!first_name || !last_name || !email || !password || !confirmPassword) {
      setError("Veuillez remplir tous les champs");
      return;
    }
    if (password !== confirmPassword) {
      setError("Les mots de passe ne correspondent pas");
      return;
    }
    if (strength < 3) {
      setError("Le mot de passe n'est pas assez fort");
      return;
    }
    if (!acceptTerms) {
      setError("Vous devez accepter les conditions d'utilisation");
      return;
    }
    const result = await register({ first_name, last_name, email, password, role });
    if (result.success) {
      navigate("/");
    } else {
      setError(result.error || "Erreur lors de l'inscription");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-4">
            <BookOpen className="h-8 w-8 text-accent" />
            <span className="text-2xl font-bold">DevOps & MLOps</span>
          </Link>
        </div>

        <Card>
          <form onSubmit={handleSubmit}>
            <CardHeader>
              <CardTitle>Créer un compte</CardTitle>
              <CardDescription>Remplissez les informations ci-dessous</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {error && (
                <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-lg border border-destructive/20">{error}</div>
              )}
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label htmlFor="first_name">Prénom</Label>
                  <Input id="first_name" value={first_name} onChange={e => setfirst_name(e.target.value)} placeholder="Marie" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="last_name">Nom</Label>
                  <Input id="last_name" value={last_name} onChange={e => setlast_name(e.target.value)} placeholder="Dupont" />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="vous@example.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Mot de passe</Label>
                <Input id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" />
                {password && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Progress value={(strength / 4) * 100} className={cn("h-1.5 flex-1", strengthColors[strength])} />
                      <span className="text-xs text-muted-foreground">{strengthLabels[strength]}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-1">
                      {passwordChecks.map(c => (
                        <span key={c.label} className={cn("text-xs flex items-center gap-1", c.valid ? "text-accent" : "text-muted-foreground")}>
                          {c.valid ? <Check className="h-3 w-3" /> : <X className="h-3 w-3" />}
                          {c.label}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirm">Confirmer le mot de passe</Label>
                <Input id="confirm" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="••••••••" />
                {confirmPassword && password !== confirmPassword && (
                  <p className="text-xs text-destructive">Les mots de passe ne correspondent pas</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>Rôle</Label>
                <Select value={role} onValueChange={(v: any) => setRole(v)}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="student">Étudiant</SelectItem>
                    <SelectItem value="instructor">Formateur</SelectItem>
                    <SelectItem value="admin">Administrateur</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-start gap-2">
                <Checkbox id="terms" checked={acceptTerms} onCheckedChange={(v) => setAcceptTerms(v === true)} className="mt-0.5" />
                <Label htmlFor="terms" className="text-sm font-normal cursor-pointer leading-snug">
                  J'accepte les <span className="text-accent hover:underline">conditions d'utilisation</span> et la <span className="text-accent hover:underline">politique de confidentialité</span>
                </Label>
              </div>
            </CardContent>
            <CardFooter className="flex-col gap-4">
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? <><Loader2 className="h-4 w-4 animate-spin" /> Création...</> : "Créer mon compte"}
              </Button>
              <p className="text-sm text-muted-foreground">
                Déjà un compte ?{" "}
                <Link to="/login" className="text-accent hover:underline font-medium">Se connecter</Link>
              </p>
            </CardFooter>
          </form>
        </Card>
      </div>
    </div>
  );
}
