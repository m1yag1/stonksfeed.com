import { NewsItem } from '@/lib/api';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Clock, Building2, ExternalLink, TrendingUp, TrendingDown } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface NewsCardProps {
  news: NewsItem;
  index: number;
}

const NewsCard = ({ news, index }: NewsCardProps) => {
  return (
    <a
      href={news.link}
      target="_blank"
      rel="noopener noreferrer"
      className="block"
    >
      <Card
        className="group h-full border-border/50 bg-card/80 backdrop-blur-sm hover:border-primary/50 active:border-primary/50 transition-all duration-300 hover:glow-gains active:scale-[0.98] animate-slide-up cursor-pointer"
        style={{ animationDelay: `${index * 50}ms` }}
      >
        <CardHeader className="pb-2 sm:pb-3 px-4 sm:px-6 pt-4 sm:pt-6">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0 flex items-start gap-2">
              {news.sentimentLabel === 'bullish' && (
                <TrendingUp className="w-4 h-4 sm:w-5 sm:h-5 text-gains shrink-0 mt-0.5" />
              )}
              {news.sentimentLabel === 'bearish' && (
                <TrendingDown className="w-4 h-4 sm:w-5 sm:h-5 text-losses shrink-0 mt-0.5" />
              )}
              <h3 className="font-semibold text-base sm:text-lg leading-tight text-foreground group-hover:text-primary transition-colors line-clamp-2">
                {news.title}
              </h3>
            </div>
            <ExternalLink className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
          </div>
        </CardHeader>
        <CardContent className="space-y-3 sm:space-y-4 px-4 sm:px-6 pb-4 sm:pb-6">
          <div className="flex flex-wrap items-center gap-2 sm:gap-3 text-xs">
            <div className="flex items-center gap-1.5 text-muted-foreground">
              <Building2 className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
              <span className="truncate max-w-[100px] sm:max-w-none">{news.publisher}</span>
            </div>

            <Badge variant="secondary" className="text-[10px] sm:text-xs px-1.5 sm:px-2.5 truncate max-w-[120px] sm:max-w-none">
              {news.feedTitle}
            </Badge>

            <div className="flex items-center gap-1.5 text-muted-foreground ml-auto">
              <Clock className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
              <span className="text-[10px] sm:text-xs">{formatDistanceToNow(news.date, { addSuffix: true })}</span>
            </div>
          </div>

          {news.sourceType && (
            <Badge variant="outline" className="text-[10px] px-1.5 border-accent/30 text-accent/70">
              {news.sourceType}
            </Badge>
          )}
        </CardContent>
      </Card>
    </a>
  );
};

export default NewsCard;
