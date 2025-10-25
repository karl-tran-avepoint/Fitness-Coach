import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Video, Upload, CheckCircle, Sparkles } from "lucide-react";
import { toast } from "sonner";

const Record = () => {
  const navigate = useNavigate();
  const [showRecording, setShowRecording] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideo, setRecordedVideo] = useState<string | null>(null);
  const [uploadedVideo, setUploadedVideo] = useState<string | null>(null);
  const [timer, setTimer] = useState(0);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const timerIntervalRef = useRef<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: "user" }, 
        audio: false 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      const chunks: Blob[] = [];

      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        const url = URL.createObjectURL(blob);
        setRecordedVideo(url);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setTimer(0);
      
      timerIntervalRef.current = window.setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);

      toast.success("Recording started!");
    } catch (error) {
      toast.error("Could not access camera");
      console.error(error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
      toast.success("Recording stopped!");
    }
  };

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setUploadedVideo(url);
      setRecordedVideo(null);
      toast.success("Video uploaded!");
    }
  };

  const handleSubmit = () => {
    if (recordedVideo || uploadedVideo) {
      toast.success("Submitting video for analysis...");
      setTimeout(() => {
        navigate("/analyze");
      }, 500);
    } else {
      toast.error("Please record or upload a video first");
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!showRecording) {
    return (
      <div className="min-h-screen relative overflow-hidden flex items-center justify-center">
        {/* Background with overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-20" />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent" />
        </div>

        {/* Hero Content */}
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto animate-fade-in-up">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card mb-8">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium">AI-Powered Analysis</span>
          </div>

          {/* Headline */}
          <h1 className="hero-title text-6xl md:text-8xl mb-6 leading-tight">
            <span className="text-white">Perfect</span>{" "}
            <span className="italic text-primary">your</span>{" "}
            <span className="text-white">form</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-white/70 mb-12 max-w-2xl mx-auto leading-relaxed">
            Get instant AI feedback on your exercise technique. 
            Record or upload, and we'll analyze your form in seconds.
          </p>

          {/* CTA Button */}
          <Button 
            onClick={() => setShowRecording(true)}
            size="lg"
            className="h-16 px-12 text-lg font-semibold bg-primary hover:bg-primary/90 text-white shadow-2xl shadow-primary/20 transition-all duration-300 hover:scale-105"
          >
            Get Started
          </Button>

          {/* Features */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="font-semibold mb-2">Instant Analysis</h3>
              <p className="text-sm text-white/60">Get feedback in seconds</p>
            </div>
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-3xl mb-3">🤖</div>
              <h3 className="font-semibold mb-2">AI-Powered</h3>
              <p className="text-sm text-white/60">Advanced motion tracking</p>
            </div>
            <div className="glass-card p-6 rounded-2xl">
              <div className="text-3xl mb-3">💪</div>
              <h3 className="font-semibold mb-2">Improve Form</h3>
              <p className="text-sm text-white/60">Prevent injuries, lift better</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden flex items-center justify-center p-4">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=2831&auto=format&fit=crop')] bg-cover bg-center opacity-10" />
      </div>

      {/* Recording Interface */}
      <div className="relative z-10 glass-card rounded-3xl shadow-2xl w-full max-w-md p-8 animate-fade-in-up">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold mb-2">Record Your Exercise</h2>
          <p className="text-white/60">Record or upload your video</p>
        </div>

        {/* Video Preview Area */}
        <div className="relative bg-black/50 rounded-2xl aspect-video mb-6 overflow-hidden flex items-center justify-center">
          {(recordedVideo || uploadedVideo) ? (
            <video 
              src={recordedVideo || uploadedVideo || undefined} 
              controls 
              className="w-full h-full object-cover"
            />
          ) : isRecording ? (
            <video 
              ref={videoRef} 
              autoPlay 
              muted 
              playsInline
              className="w-full h-full object-cover"
            />
          ) : (
            <Video className="w-20 h-20 text-white/30" />
          )}
          
          {isRecording && (
            <div className="absolute top-4 right-4 flex items-center gap-2 bg-red-500 text-white px-3 py-1 rounded-full">
              <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
              <span className="text-sm font-semibold">REC</span>
            </div>
          )}
        </div>

        {/* Timer */}
        {isRecording && (
          <div className="text-center mb-4">
            <span className="text-2xl font-bold text-primary">{formatTime(timer)}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="space-y-3">
          {!isRecording && !recordedVideo && !uploadedVideo && (
            <Button 
              onClick={startRecording}
              className="w-full bg-primary hover:bg-primary/90 text-white h-14 text-lg font-semibold"
            >
              <Video className="mr-2" />
              Start Recording
            </Button>
          )}

          {isRecording && (
            <Button 
              onClick={stopRecording}
              className="w-full bg-red-500 hover:bg-red-600 text-white h-14 text-lg font-semibold"
            >
              Stop & Save
            </Button>
          )}

          {!isRecording && (
            <>
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-white/10" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-card px-2 text-white/60">Or</span>
                </div>
              </div>

              <Button 
                onClick={() => fileInputRef.current?.click()}
                variant="outline"
                className="w-full h-14 text-lg font-semibold glass-button"
              >
                <Upload className="mr-2" />
                Upload Video
              </Button>
              <input 
                ref={fileInputRef}
                type="file" 
                accept="video/*" 
                onChange={handleUpload}
                className="hidden"
              />
            </>
          )}

          {(recordedVideo || uploadedVideo) && !isRecording && (
            <Button 
              onClick={handleSubmit}
              className="w-full bg-primary hover:bg-primary/90 text-white h-14 text-lg font-semibold"
            >
              <CheckCircle className="mr-2" />
              Submit for Analysis
            </Button>
          )}
        </div>

        {/* Instructions */}
        <div className="mt-6 glass-card rounded-xl p-4">
          <h3 className="font-semibold text-sm mb-2">Tips:</h3>
          <ul className="text-sm text-white/60 space-y-1">
            <li>• Perform your exercise in 20-30 seconds</li>
            <li>• Ensure good lighting and full body visible</li>
            <li>• Record from the side for best results</li>
          </ul>
        </div>

        {/* Back button */}
        <button 
          onClick={() => setShowRecording(false)}
          className="mt-4 text-sm text-white/40 hover:text-white/60 transition-colors w-full text-center"
        >
          ← Back to home
        </button>
      </div>
    </div>
  );
};

export default Record;
