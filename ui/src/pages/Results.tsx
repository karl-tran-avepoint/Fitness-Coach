import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, RotateCcw, CheckCircle2, XCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { toast } from "sonner";

// TypeScript interface for the analysis response
interface AnalysisItem {
  image_base64: string;
  posture: {
    errors: string[];
    suggestions: string[];
  };
}

interface AnalysisResponse {
  analysis: AnalysisItem[];
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const Results = () => {
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    // Fetch the analysis data from your backend API
    // For now, we'll load the example data
    const fetchAnalysisData = async () => {
      try {
        // Replace this with your actual API endpoint
        const response = await fetch('/example_output.json');
        const data: AnalysisResponse = await response.json();
        setAnalysisData(data);
      } catch (error) {
        console.error('Error fetching analysis data:', error);
        // Fallback to empty data
        setAnalysisData({ analysis: [] });
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysisData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
        </div>
        <div className="relative z-10 text-center">
          <p className="text-white/60 text-lg">Loading results...</p>
        </div>
      </div>
    );
  }

  const handleDownloadReport = async () => {
    try {
      setDownloading(true);
      const response = await fetch(`${API_BASE_URL}/download-report/`);

      if (!response.ok) {
        throw new Error(`Unexpected status: ${response.status}`);
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "analysis_report.json";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast.success("Report downloaded");
    } catch (error) {
      console.error("Error downloading report:", error);
      toast.error("Failed to download report");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden py-8 px-4">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto space-y-6 animate-fade-in-up">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="hero-title text-5xl mb-2">Results & Feedback</h1>
          <p className="text-white/60">Your analysis is complete</p>
          {analysisData && (
            <Badge variant="outline" className="mt-4 text-base px-4 py-2">
              {analysisData.analysis.length} Frame{analysisData.analysis.length !== 1 ? 's' : ''} Analyzed
            </Badge>
          )}
        </div>

        {/* Analysis Results - Dynamic rendering */}
        {analysisData && analysisData.analysis.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {analysisData.analysis.map((item, index) => (
              <Card key={index} className="glass-card border-0 shadow-xl">
                <CardContent className="p-6">
                  <div className="mb-4 flex items-center justify-between">
                    <h2 className="text-xl font-bold">Frame {index + 1}</h2>
                    {item.posture.errors.length > 0 && (
                      <Badge variant="destructive">
                        {item.posture.errors.length} Issue{item.posture.errors.length !== 1 ? 's' : ''}
                      </Badge>
                    )}
                  </div>

                  {/* Image from base64 */}
                  <div className="relative bg-slate-950 rounded-lg mb-4 overflow-hidden">
                    <img
                      src={`data:image/jpeg;base64,${item.image_base64}`}
                      alt={`Analysis frame ${index + 1}`}
                      className="w-full h-auto object-contain"
                    />
                  </div>

                  {/* Errors Section */}
                  {item.posture.errors.length > 0 && (
                    <div className="mb-4">
                      <div className="flex items-center gap-2 mb-3">
                        <XCircle className="text-red-400 w-5 h-5" />
                        <h3 className="font-semibold text-red-400">Issues Detected</h3>
                      </div>
                      <div className="space-y-2">
                        {item.posture.errors.map((error, errorIdx) => (
                          <div
                            key={errorIdx}
                            className="bg-red-500/10 border-l-4 border-red-400 rounded px-3 py-2"
                          >
                            <p className="text-sm text-red-300">{error}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Suggestions Section */}
                  {item.posture.suggestions.length > 0 && (
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <CheckCircle2 className="text-green-400 w-5 h-5" />
                        <h3 className="font-semibold text-green-400">Recommendations</h3>
                      </div>
                      <div className="space-y-2">
                        {item.posture.suggestions.map((suggestion, suggestionIdx) => (
                          <div
                            key={suggestionIdx}
                            className="bg-green-500/10 border-l-4 border-green-400 rounded px-3 py-2"
                          >
                            <p className="text-sm text-green-300">{suggestion}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="glass-card border-0 shadow-xl">
            <CardContent className="p-6 text-center">
              <AlertCircle className="w-12 h-12 mx-auto mb-4 text-yellow-400" />
              <p className="text-white/60">No analysis data available</p>
            </CardContent>
          </Card>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
          <Button
            variant="outline"
            className="h-12 text-base font-semibold border-2 border-white/20 text-white hover:bg-white/10"
            onClick={() => navigate("/")}
          >
            <RotateCcw className="mr-2 w-5 h-5" />
            Analyze Another
          </Button>

          <Button
            className="bg-primary hover:bg-primary/90 text-white h-12 text-base font-semibold"
            onClick={handleDownloadReport}
            disabled={downloading}
          >
            {downloading ? "Preparing..." : "Download Report"}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Results;
