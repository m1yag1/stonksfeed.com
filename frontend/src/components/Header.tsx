import { Rocket, TrendingUp } from 'lucide-react';

const Header = () => {
  return (
    <header className="border-b border-border/50 bg-card/50 backdrop-blur-md sticky top-0 z-50">
      <div className="container py-3 sm:py-4">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="relative">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl gradient-stonks flex items-center justify-center glow-gains animate-pulse-glow">
              <Rocket className="w-5 h-5 sm:w-6 sm:h-6 text-primary-foreground" />
            </div>
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
              <span className="gradient-text-stonks">STONKS</span>
              <span className="text-foreground">FEED</span>
            </h1>
            <p className="text-[10px] sm:text-xs text-muted-foreground flex items-center gap-1">
              <TrendingUp className="w-2.5 h-2.5 sm:w-3 sm:h-3 text-gains" />
              Let's get those tendies 🍗
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;