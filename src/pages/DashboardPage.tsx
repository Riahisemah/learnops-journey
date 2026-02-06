import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import ProgressDashboard from "@/components/lesson/ProgressDashboard";

const DashboardPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen animate-fade-in">
      <header className="bg-gradient-to-br from-primary/5 via-background to-accent/5 py-8 px-6 border-b border-border">
        <div className="max-w-4xl mx-auto">
          <Button 
            variant="ghost" 
            size="sm" 
            className="mb-4 gap-2"
            onClick={() => navigate('/')}
          >
            <ArrowLeft className="h-4 w-4" />
            Retour
          </Button>
          <h1 className="text-3xl font-bold">Tableau de bord</h1>
          <p className="text-muted-foreground mt-1">Suivez votre progression et vos accomplissements</p>
        </div>
      </header>

      <section className="py-8 px-6">
        <div className="max-w-4xl mx-auto">
          <ProgressDashboard />
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
