import { useState } from "react";
import { 
  Play, 
  BarChart3, 
  Activity, 
  Cpu,
  TrendingUp,
  Info
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface PredictionResult {
  prediction: string;
  confidence: number;
  class_probabilities: { label: string; probability: number }[];
}

interface ModelLog {
  version: string;
  accuracy: number;
  framework: string;
  lastTrained: string;
  features: number;
}

const modelLog: ModelLog = {
  version: 'v1.3.2',
  accuracy: 0.945,
  framework: 'scikit-learn (RandomForest)',
  lastTrained: '2025-01-15',
  features: 4,
};

const MLDashboard = () => {
  const [features, setFeatures] = useState({
    sepalLength: 5.1,
    sepalWidth: 3.5,
    petalLength: 1.4,
    petalWidth: 0.2,
  });
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    
    // Simulated prediction based on feature values
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const { petalLength, petalWidth } = features;
    let prediction: string;
    let probs: { label: string; probability: number }[];

    if (petalLength < 2.5 && petalWidth < 0.8) {
      prediction = 'Iris Setosa';
      probs = [
        { label: 'Iris Setosa', probability: 0.96 },
        { label: 'Iris Versicolor', probability: 0.03 },
        { label: 'Iris Virginica', probability: 0.01 },
      ];
    } else if (petalLength < 5 && petalWidth < 1.8) {
      prediction = 'Iris Versicolor';
      probs = [
        { label: 'Iris Setosa', probability: 0.02 },
        { label: 'Iris Versicolor', probability: 0.89 },
        { label: 'Iris Virginica', probability: 0.09 },
      ];
    } else {
      prediction = 'Iris Virginica';
      probs = [
        { label: 'Iris Setosa', probability: 0.01 },
        { label: 'Iris Versicolor', probability: 0.12 },
        { label: 'Iris Virginica', probability: 0.87 },
      ];
    }

    setResult({
      prediction,
      confidence: probs[0].probability > probs[1].probability && probs[0].probability > probs[2].probability 
        ? probs[0].probability 
        : probs[1].probability > probs[2].probability 
          ? probs[1].probability 
          : probs[2].probability,
      class_probabilities: probs,
    });
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-2">
        <Badge variant="secondary" className="gap-1">
          <Cpu className="h-3 w-3" />
          Démo ML Interactive
        </Badge>
        <Badge variant="outline" className="gap-1 text-xs">
          <Info className="h-3 w-3" />
          Iris Dataset Classification
        </Badge>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Input Features */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-primary" />
              Features du modèle
            </CardTitle>
            <CardDescription>Ajustez les paramètres pour obtenir une prédiction</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <FeatureSlider
              label="Longueur sépale (cm)"
              value={features.sepalLength}
              min={4}
              max={8}
              step={0.1}
              onChange={(v) => setFeatures(prev => ({ ...prev, sepalLength: v }))}
            />
            <FeatureSlider
              label="Largeur sépale (cm)"
              value={features.sepalWidth}
              min={2}
              max={4.5}
              step={0.1}
              onChange={(v) => setFeatures(prev => ({ ...prev, sepalWidth: v }))}
            />
            <FeatureSlider
              label="Longueur pétale (cm)"
              value={features.petalLength}
              min={1}
              max={7}
              step={0.1}
              onChange={(v) => setFeatures(prev => ({ ...prev, petalLength: v }))}
            />
            <FeatureSlider
              label="Largeur pétale (cm)"
              value={features.petalWidth}
              min={0.1}
              max={2.5}
              step={0.1}
              onChange={(v) => setFeatures(prev => ({ ...prev, petalWidth: v }))}
            />

            <Button 
              onClick={handlePredict} 
              disabled={loading}
              className="w-full gap-2 bg-accent hover:bg-accent/90 text-accent-foreground"
            >
              <Play className="h-4 w-4" />
              {loading ? 'Prédiction...' : 'Prédire'}
            </Button>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="space-y-4">
          {result ? (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-accent" />
                    Résultat
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-4">
                    <div className="text-3xl font-bold text-primary mb-1">{result.prediction}</div>
                    <div className="text-sm text-muted-foreground">
                      Confiance : {(result.confidence * 100).toFixed(1)}%
                    </div>
                  </div>

                  <div className="space-y-3">
                    {result.class_probabilities.map((cp) => (
                      <div key={cp.label} className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span>{cp.label}</span>
                          <span className="font-mono">{(cp.probability * 100).toFixed(1)}%</span>
                        </div>
                        <Progress value={cp.probability * 100} className="h-2" />
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Model Logs */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm flex items-center gap-2">
                    <Activity className="h-4 w-4 text-info" />
                    Logs du modèle
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="font-mono text-xs space-y-1 bg-muted/50 rounded-lg p-3">
                    <div className="text-muted-foreground">[INFO] Model version: <span className="text-accent">{modelLog.version}</span></div>
                    <div className="text-muted-foreground">[INFO] Framework: <span className="text-foreground">{modelLog.framework}</span></div>
                    <div className="text-muted-foreground">[INFO] Accuracy: <span className="text-accent">{(modelLog.accuracy * 100).toFixed(1)}%</span></div>
                    <div className="text-muted-foreground">[INFO] Last trained: <span className="text-foreground">{modelLog.lastTrained}</span></div>
                    <div className="text-muted-foreground">[INFO] Features used: <span className="text-foreground">{modelLog.features}</span></div>
                    <div className="text-muted-foreground">[INFO] Prediction: <span className="text-primary font-bold">{result.prediction}</span></div>
                    <div className="text-muted-foreground">[INFO] Confidence: <span className="text-accent">{(result.confidence * 100).toFixed(1)}%</span></div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="h-full flex items-center justify-center min-h-[300px]">
              <CardContent className="text-center">
                <Cpu className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
                <p className="text-muted-foreground">
                  Ajustez les features et cliquez sur "Prédire" pour voir les résultats
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

const FeatureSlider = ({ 
  label, value, min, max, step, onChange 
}: { 
  label: string; value: number; min: number; max: number; step: number; onChange: (v: number) => void 
}) => (
  <div className="space-y-2">
    <div className="flex justify-between items-center">
      <Label className="text-sm">{label}</Label>
      <span className="text-sm font-mono text-primary">{value.toFixed(1)}</span>
    </div>
    <Slider
      value={[value]}
      min={min}
      max={max}
      step={step}
      onValueChange={([v]) => onChange(v)}
    />
  </div>
);

export default MLDashboard;
