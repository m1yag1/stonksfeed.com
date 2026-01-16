import { Newspaper, Zap, Building2, Rss } from 'lucide-react';
import { NewsItem } from '@/data/mockNews';

interface StatsBarProps {
  news: NewsItem[];
  filteredCount: number;
}

const StatsBar = ({ news, filteredCount }: StatsBarProps) => {
  const uniquePublishers = new Set(news.map(n => n.publisher)).size;
  const uniqueFeeds = new Set(news.map(n => n.feedTitle)).size;

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
      <div className="bg-secondary/50 rounded-lg p-3 sm:p-4 border border-border/50">
        <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground text-xs sm:text-sm mb-1">
          <Newspaper className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          <span>Total</span>
        </div>
        <p className="text-xl sm:text-2xl font-bold text-foreground">{filteredCount}</p>
      </div>
      
      <div className="bg-secondary/50 rounded-lg p-3 sm:p-4 border border-border/50">
        <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground text-xs sm:text-sm mb-1">
          <Zap className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-accent" />
          <span>Tickers</span>
        </div>
        <p className="text-xl sm:text-2xl font-bold text-accent">{news.filter(n => n.ticker).length}</p>
      </div>
      
      <div className="bg-secondary/50 rounded-lg p-3 sm:p-4 border border-border/50">
        <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground text-xs sm:text-sm mb-1">
          <Building2 className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          <span>Publishers</span>
        </div>
        <p className="text-xl sm:text-2xl font-bold text-foreground">{uniquePublishers}</p>
      </div>
      
      <div className="bg-secondary/50 rounded-lg p-3 sm:p-4 border border-border/50">
        <div className="flex items-center gap-1.5 sm:gap-2 text-muted-foreground text-xs sm:text-sm mb-1">
          <Rss className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
          <span>Feeds</span>
        </div>
        <p className="text-xl sm:text-2xl font-bold text-foreground">{uniqueFeeds}</p>
      </div>
    </div>
  );
};

export default StatsBar;