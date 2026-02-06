import { useState, useMemo } from "react";
import { 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  RotateCcw, 
  Download, 
  HelpCircle,
  Trophy
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";
import { Quiz, QuizQuestion } from "@/data/quiz-data";

interface QuizSystemProps {
  quiz: Quiz;
  onComplete: () => void;
  completed: boolean;
}

interface QuizAnswer {
  questionId: string;
  selectedAnswers: number[];
  isCorrect: boolean;
}

const QuizSystem = ({ quiz, onComplete, completed: alreadyCompleted }: QuizSystemProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswer[]>([]);
  const [selectedOptions, setSelectedOptions] = useState<number[]>([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [quizFinished, setQuizFinished] = useState(false);

  const currentQuestion = quiz.questions[currentIndex];
  const progress = ((currentIndex) / quiz.questions.length) * 100;

  const score = useMemo(() => {
    if (answers.length === 0) return 0;
    const correct = answers.filter(a => a.isCorrect).length;
    return Math.round((correct / quiz.questions.length) * 100);
  }, [answers, quiz.questions.length]);

  const handleSelectSingle = (optionIndex: string) => {
    setSelectedOptions([parseInt(optionIndex)]);
  };

  const handleSelectMultiple = (optionIndex: number, checked: boolean) => {
    setSelectedOptions(prev => 
      checked 
        ? [...prev, optionIndex] 
        : prev.filter(i => i !== optionIndex)
    );
  };

  const handleSubmitAnswer = () => {
    const isCorrect = arraysEqual(
      [...selectedOptions].sort(), 
      [...currentQuestion.correctAnswers].sort()
    );
    
    setAnswers(prev => [...prev, {
      questionId: currentQuestion.id,
      selectedAnswers: selectedOptions,
      isCorrect,
    }]);
    setShowFeedback(true);
  };

  const handleNext = () => {
    if (currentIndex < quiz.questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedOptions([]);
      setShowFeedback(false);
    } else {
      setQuizFinished(true);
      onComplete();
    }
  };

  const handleRetry = () => {
    setCurrentIndex(0);
    setAnswers([]);
    setSelectedOptions([]);
    setShowFeedback(false);
    setQuizFinished(false);
  };

  const handleExportResults = () => {
    const results = {
      quiz: quiz.title,
      date: new Date().toISOString(),
      score,
      totalQuestions: quiz.questions.length,
      correctAnswers: answers.filter(a => a.isCorrect).length,
      details: answers.map((answer, i) => ({
        question: quiz.questions[i].question,
        selectedAnswers: answer.selectedAnswers.map(idx => quiz.questions[i].options[idx]),
        correctAnswers: quiz.questions[i].correctAnswers.map(idx => quiz.questions[i].options[idx]),
        isCorrect: answer.isCorrect,
      })),
    };

    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `quiz-results-${quiz.moduleId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Score screen
  if (quizFinished) {
    const correctCount = answers.filter(a => a.isCorrect).length;
    return (
      <Card>
        <CardContent className="p-8 text-center space-y-6">
          <div className={cn(
            "w-24 h-24 rounded-full mx-auto flex items-center justify-center",
            score >= 80 ? "bg-accent/20 text-accent" : score >= 50 ? "bg-warning/20 text-warning" : "bg-destructive/20 text-destructive"
          )}>
            <Trophy className="h-12 w-12" />
          </div>
          
          <div>
            <h2 className="text-2xl font-bold mb-1">
              {score >= 80 ? "Excellent !" : score >= 50 ? "Pas mal !" : "Continuez d'apprendre !"}
            </h2>
            <p className="text-muted-foreground">
              Vous avez obtenu {correctCount} sur {quiz.questions.length} questions correctes
            </p>
          </div>

          <div className="text-5xl font-bold text-primary">{score}%</div>

          <Progress value={score} className="h-3 max-w-xs mx-auto" />

          <div className="text-sm text-muted-foreground space-y-1">
            {score >= 80 && <p>🎉 Vous maîtrisez ce module !</p>}
            {score >= 50 && score < 80 && <p>📚 Revoyez les leçons pour améliorer votre score.</p>}
            {score < 50 && <p>💪 N'hésitez pas à revoir les leçons et réessayer le quiz.</p>}
          </div>

          {/* Review answers */}
          <div className="text-left space-y-3 max-w-lg mx-auto">
            <h3 className="font-semibold text-center">Récapitulatif</h3>
            {quiz.questions.map((q, i) => (
              <div key={q.id} className={cn(
                "p-3 rounded-lg border text-sm",
                answers[i]?.isCorrect ? "border-accent/30 bg-accent/5" : "border-destructive/30 bg-destructive/5"
              )}>
                <div className="flex items-start gap-2">
                  {answers[i]?.isCorrect 
                    ? <CheckCircle2 className="h-4 w-4 text-accent mt-0.5 flex-shrink-0" />
                    : <XCircle className="h-4 w-4 text-destructive mt-0.5 flex-shrink-0" />
                  }
                  <span>{q.question}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <Button variant="outline" onClick={handleRetry} className="gap-2">
              <RotateCcw className="h-4 w-4" />
              Recommencer
            </Button>
            <Button variant="outline" onClick={handleExportResults} className="gap-2">
              <Download className="h-4 w-4" />
              Exporter (JSON)
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Question screen
  const currentAnswer = answers[currentIndex];
  const isAnswered = showFeedback;

  return (
    <div className="space-y-4">
      {/* Progress */}
      <div className="flex items-center gap-3">
        <Progress value={progress} className="h-2 flex-1" />
        <Badge variant="secondary" className="text-xs">
          {currentIndex + 1} / {quiz.questions.length}
        </Badge>
      </div>

      {/* Question Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="outline" className="text-xs">
              {currentQuestion.type === 'single' && 'Choix unique'}
              {currentQuestion.type === 'multiple' && 'Choix multiples'}
              {currentQuestion.type === 'boolean' && 'Vrai / Faux'}
            </Badge>
          </div>
          <CardTitle className="text-lg flex items-start gap-2">
            <HelpCircle className="h-5 w-5 text-warning mt-0.5 flex-shrink-0" />
            {currentQuestion.question}
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Options */}
          {currentQuestion.type === 'single' || currentQuestion.type === 'boolean' ? (
            <RadioGroup
              value={selectedOptions[0]?.toString() || ''}
              onValueChange={handleSelectSingle}
              disabled={isAnswered}
            >
              {currentQuestion.options.map((option, idx) => (
                <label
                  key={idx}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors",
                    !isAnswered && "hover:bg-secondary",
                    isAnswered && currentQuestion.correctAnswers.includes(idx) && "border-accent bg-accent/10",
                    isAnswered && selectedOptions.includes(idx) && !currentQuestion.correctAnswers.includes(idx) && "border-destructive bg-destructive/10"
                  )}
                >
                  <RadioGroupItem value={idx.toString()} />
                  <span className="text-sm flex-1">{option}</span>
                  {isAnswered && currentQuestion.correctAnswers.includes(idx) && (
                    <CheckCircle2 className="h-4 w-4 text-accent" />
                  )}
                  {isAnswered && selectedOptions.includes(idx) && !currentQuestion.correctAnswers.includes(idx) && (
                    <XCircle className="h-4 w-4 text-destructive" />
                  )}
                </label>
              ))}
            </RadioGroup>
          ) : (
            <div className="space-y-2">
              {currentQuestion.options.map((option, idx) => (
                <label
                  key={idx}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors",
                    !isAnswered && "hover:bg-secondary",
                    isAnswered && currentQuestion.correctAnswers.includes(idx) && "border-accent bg-accent/10",
                    isAnswered && selectedOptions.includes(idx) && !currentQuestion.correctAnswers.includes(idx) && "border-destructive bg-destructive/10"
                  )}
                >
                  <Checkbox
                    checked={selectedOptions.includes(idx)}
                    onCheckedChange={(checked) => handleSelectMultiple(idx, checked as boolean)}
                    disabled={isAnswered}
                  />
                  <span className="text-sm flex-1">{option}</span>
                  {isAnswered && currentQuestion.correctAnswers.includes(idx) && (
                    <CheckCircle2 className="h-4 w-4 text-accent" />
                  )}
                  {isAnswered && selectedOptions.includes(idx) && !currentQuestion.correctAnswers.includes(idx) && (
                    <XCircle className="h-4 w-4 text-destructive" />
                  )}
                </label>
              ))}
            </div>
          )}

          {/* Feedback */}
          {isAnswered && (
            <div className={cn(
              "p-4 rounded-lg border",
              currentAnswer?.isCorrect ? "border-accent/30 bg-accent/5" : "border-destructive/30 bg-destructive/5"
            )}>
              <div className="flex items-center gap-2 mb-1">
                {currentAnswer?.isCorrect ? (
                  <>
                    <CheckCircle2 className="h-5 w-5 text-accent" />
                    <span className="font-semibold text-accent">Correct !</span>
                  </>
                ) : (
                  <>
                    <XCircle className="h-5 w-5 text-destructive" />
                    <span className="font-semibold text-destructive">Incorrect</span>
                  </>
                )}
              </div>
              <p className="text-sm text-muted-foreground">{currentQuestion.explanation}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-2 pt-2">
            {!isAnswered ? (
              <Button
                onClick={handleSubmitAnswer}
                disabled={selectedOptions.length === 0}
                className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2"
              >
                Valider
              </Button>
            ) : (
              <Button onClick={handleNext} className="gap-2">
                {currentIndex < quiz.questions.length - 1 ? (
                  <>
                    Suivant
                    <ArrowRight className="h-4 w-4" />
                  </>
                ) : (
                  'Voir les résultats'
                )}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

function arraysEqual(a: number[], b: number[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((val, index) => val === b[index]);
}

export default QuizSystem;
