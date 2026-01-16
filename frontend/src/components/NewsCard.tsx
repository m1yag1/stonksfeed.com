import { NewsItem } from '@/data/mockNews';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, Building2 } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface NewsCardProps {
  news: NewsItem;
  index: number;
}

const NewsCard = ({ news, index }: NewsCardProps) => {
  return (
    <Card 
      className="group border-border/50 bg-card/80 backdrop-blur-sm hover:border-primary/50 active:border-primary/50 transition-all duration-300 hover:glow-gains active:scale-[0.98] animate-slide-up"
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <CardHeader className="pb-2 sm:pb-3 px-4 sm:px-6 pt-4 sm:pt-6">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-base sm:text-lg leading-tight text-foreground group-hover:text-primary transition-colors">
              {news.title}
            </h3>
          </div>
          {news.ticker && (
            <Badge variant="outline" className="shrink-0 font-mono text-xs sm:text-sm border-accent/50 text-accent px-2 py-0.5">
              ${news.ticker}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3 sm:space-y-4 px-4 sm:px-6 pb-4 sm:pb-6">
        <p className="text-muted-foreground text-sm leading-relaxed line-clamp-3">
          {news.summary}
        </p>
        
        <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs">
          <div className="flex items-center gap-1.5 text-muted-foreground">
            <Building2 className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
            <span className="truncate max-w-[80px] sm:max-w-none">{news.publisher}</span>
          </div>
          
          <Badge variant="secondary" className="text-[10px] sm:text-xs px-1.5 sm:px-2.5">
            {news.feedTitle}
          </Badge>
          
          <div className="flex items-center gap-1.5 text-muted-foreground ml-auto">
            <Clock className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
            <span className="text-[10px] sm:text-xs">{formatDistanceToNow(news.date, { addSuffix: true })}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default NewsCard;