import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Play, RotateCcw } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Results = () => {
  const navigate = useNavigate();

  const scoreData = [
    { label: "Total Reps", value: "10", color: "text-primary" },
    { label: "Clean Reps", value: "8", color: "text-success" },
    { label: "Form Score", value: "85%", color: "text-primary" },
    { label: "Balance", value: "Good", color: "text-success" },
    { label: "Range of Motion", value: "Fair", color: "text-warning" },
  ];

  const issues = [
    {
      frame: "Rep 3, 0:08",
      issue: "Knees caving in at bottom",
      emoji: "🦵"
    },
    {
      frame: "Rep 7, 0:18",
      issue: "Forward lean on descent",
      emoji: "🏃"
    }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden py-8 px-4">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
      </div>

      <div className="relative z-10 max-w-2xl mx-auto space-y-6 animate-fade-in-up">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="hero-title text-5xl mb-2">Results & Feedback</h1>
          <p className="text-white/60">Your analysis is complete</p>
        </div>

        {/* Scorecard */}
        <Card className="glass-card border-0 shadow-xl">
          <CardContent className="p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              📊 Performance Scorecard
            </h2>
            <div className="space-y-3">
              {scoreData.map((score, idx) => (
                <div 
                  key={idx}
                  className="flex justify-between items-center py-3 border-b border-white/10 last:border-0"
                >
                  <span className="text-white/60 font-medium">{score.label}</span>
                  <span className={`text-xl font-bold ${score.color}`}>{score.value}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Issues Found */}
        <Card className="glass-card border-0 shadow-xl">
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle className="text-red-400 w-5 h-5" />
              <h2 className="text-xl font-bold">Issues Found</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {issues.map((issue, idx) => (
                <div 
                  key={idx}
                  className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 overflow-hidden"
                >
                  {/* Frame Preview */}
                  <div className="relative bg-slate-950 rounded-lg h-32 flex items-center justify-center mb-3">
                    <span className="text-5xl">{issue.emoji}</span>
                    <Badge 
                      variant="destructive" 
                      className="absolute top-2 right-2 animate-blink"
                    >
                      ⚠️
                    </Badge>
                  </div>
                  
                  {/* Annotation */}
                  <div className="bg-red-500/10 border-l-4 border-red-400 rounded px-3 py-2">
                    <p className="text-xs text-white/40 mb-1">{issue.frame}</p>
                    <p className="text-sm text-red-400 font-semibold">{issue.issue}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Coach Feedback */}
        <Card className="glass-card shadow-xl bg-primary/20 border-primary/30 text-white">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <span className="text-3xl">🎯</span>
              <div>
                <h3 className="font-bold text-lg mb-2">Key Fix</h3>
                <p className="leading-relaxed">
                  Focus on maintaining proper form throughout the full range of motion. 
                  Your overall technique is solid, but pay attention to alignment and 
                  control during the most challenging parts of the movement. Consider 
                  reducing weight or reps to maintain better form consistency.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Timeline */}
        <div className="flex justify-center gap-2 py-4">
          {[...Array(10)].map((_, idx) => (
            <div 
              key={idx}
              className="w-3 h-3 rounded-full bg-primary/60 hover:bg-primary transition-colors cursor-pointer"
            />
          ))}
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-4">
          <Button 
            className="bg-primary hover:bg-primary/90 text-white h-12 text-base font-semibold"
            onClick={() => {/* Replay video logic */}}
          >
            <Play className="mr-2 w-5 h-5" />
            Replay with Comments
          </Button>
          
          <Button 
            variant="outline" 
            className="h-12 text-base font-semibold border-2 border-white/20 text-white hover:bg-white/10"
            onClick={() => navigate("/")}
          >
            <RotateCcw className="mr-2 w-5 h-5" />
            Analyze Another
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Results;
