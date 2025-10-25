import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Progress } from "@/components/ui/progress";
import { Loader2 } from "lucide-react";

const Analyze = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Simulate AI analysis duration
    const timer = setTimeout(() => {
      navigate("/results");
    }, 4000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
      </div>

      <div className="relative z-10 glass-card rounded-3xl shadow-2xl w-full max-w-md p-12 text-center animate-fade-in-up">
        <div className="mb-8">
          <Loader2 className="w-20 h-20 mx-auto text-primary animate-spin" />
        </div>
        
        <h2 className="text-3xl font-bold mb-4">
          Analyzing Your Form
        </h2>
        
        <p className="text-white/60 mb-8 text-lg">
          AI is reviewing your video...
        </p>
        
        <div className="space-y-3 mb-8">
          <Progress value={65} className="h-2" />
          <p className="text-sm text-white/60">Processing video frames</p>
        </div>

        <div className="space-y-2 text-left bg-white/5 border border-white/10 rounded-xl p-6">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-success rounded-full" />
            <span className="text-sm">Video uploaded ✓</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-success rounded-full" />
            <span className="text-sm">Frames extracted ✓</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            <span className="text-sm">Analyzing movement patterns...</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-white/20 rounded-full" />
            <span className="text-sm text-white/40">Generating feedback</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analyze;
