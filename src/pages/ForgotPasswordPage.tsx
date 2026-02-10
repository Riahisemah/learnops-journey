import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { BookOpen, Loader2, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [countdown, setCountdown] = useState(5);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;
    setLoading(true);
    await new Promise(r => setTimeout(r, 800));
    setLoading(false);
    setSent(true);
  };

  useEffect(() => {
    if (!sent) return;
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          navigate("/login");
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [sent, navigate]);

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
          {sent ? (
            <>
              <CardHeader className="text-center">
                <div className="mx-auto w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center mb-2">
                  <CheckCircle2 className="h-6 w-6 text-accent" />
                </div>
                <CardTitle>Email envoyé !</CardTitle>
                <CardDescription>
                  Un lien de réinitialisation a été envoyé à <strong>{email}</strong>
                </CardDescription>
              </CardHeader>
              <CardFooter className="flex-col gap-2">
                <p className="text-sm text-muted-foreground">Redirection dans {countdown}s...</p>
                <Button variant="outline" asChild className="w-full">
                  <Link to="/login">Retour à la connexion</Link>
                </Button>
              </CardFooter>
            </>
          ) : (
            <form onSubmit={handleSubmit}>
              <CardHeader>
                <CardTitle>Mot de passe oublié</CardTitle>
                <CardDescription>Entrez votre email pour recevoir un lien de réinitialisation</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="vous@example.com" />
                </div>
              </CardContent>
              <CardFooter className="flex-col gap-4">
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Envoi...</> : "Envoyer le lien"}
                </Button>
                <Link to="/login" className="text-sm text-accent hover:underline">Retour à la connexion</Link>
              </CardFooter>
            </form>
          )}
        </Card>
      </div>
    </div>
  );
}
