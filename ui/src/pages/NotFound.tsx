import { useLocation } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="text-center glass-card rounded-3xl p-12 max-w-md shadow-2xl">
        <h1 className="mb-4 text-6xl font-bold gradient-primary bg-clip-text text-transparent">404</h1>
        <p className="mb-6 text-2xl text-foreground font-semibold">Oops! Page not found</p>
        <p className="mb-8 text-muted-foreground">The page you're looking for doesn't exist.</p>
        <a 
          href="/" 
          className="inline-flex items-center justify-center gradient-primary text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity"
        >
          Return to Home
        </a>
      </div>
    </div>
  );
};

export default NotFound;
