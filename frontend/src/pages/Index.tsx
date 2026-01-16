import { useState, useMemo } from 'react';
import { useArticles } from '@/hooks/useArticles';
import Header from '@/components/Header';
import NewsCard from '@/components/NewsCard';
import SearchBar from '@/components/SearchBar';
import SortDropdown, { SortOption } from '@/components/SortDropdown';
import StatsBar from '@/components/StatsBar';
import { Skeleton } from '@/components/ui/skeleton';

const Index = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('date');

  const { data: articles = [], isLoading, error } = useArticles(200);

  const filteredAndSortedNews = useMemo(() => {
    let result = [...articles];

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (news) =>
          news.title.toLowerCase().includes(query) ||
          news.publisher.toLowerCase().includes(query) ||
          news.feedTitle.toLowerCase().includes(query)
      );
    }

    // Sort
    result.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return b.date.getTime() - a.date.getTime();
        case 'publisher':
          return a.publisher.localeCompare(b.publisher);
        case 'feedTitle':
          return a.feedTitle.localeCompare(b.feedTitle);
        default:
          return 0;
      }
    });

    return result;
  }, [articles, searchQuery, sortBy]);

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container px-4 sm:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8">
        {/* Stats */}
        <StatsBar news={articles} filteredCount={filteredAndSortedNews.length} />

        {/* Controls */}
        <div className="flex flex-col gap-3 sm:flex-row sm:gap-4 sm:items-center">
          <SearchBar value={searchQuery} onChange={setSearchQuery} />
          <SortDropdown value={sortBy} onChange={setSortBy} />
        </div>

        {/* Results count */}
        <div className="flex items-center gap-2 text-xs sm:text-sm text-muted-foreground">
          <span>Showing</span>
          <span className="font-mono text-primary font-semibold">{filteredAndSortedNews.length}</span>
          <span>of</span>
          <span className="font-mono">{articles.length}</span>
          <span className="hidden sm:inline">stonks updates</span>
          {searchQuery && (
            <span className="text-accent truncate max-w-[120px] sm:max-w-none">
              for "{searchQuery}"
            </span>
          )}
        </div>

        {/* Loading state */}
        {isLoading && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-48 rounded-lg" />
            ))}
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="text-center py-12 sm:py-16">
            <p className="text-4xl sm:text-5xl mb-4">😵</p>
            <p className="text-lg sm:text-xl font-semibold text-foreground mb-2">
              Failed to load stonks
            </p>
            <p className="text-sm sm:text-base text-muted-foreground">
              {error.message}
            </p>
          </div>
        )}

        {/* News Grid */}
        {!isLoading && !error && filteredAndSortedNews.length > 0 && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {filteredAndSortedNews.map((news, index) => (
              <NewsCard key={news.id} news={news} index={index} />
            ))}
          </div>
        )}

        {/* Empty state */}
        {!isLoading && !error && filteredAndSortedNews.length === 0 && (
          <div className="text-center py-12 sm:py-16">
            <p className="text-4xl sm:text-5xl mb-4">📭</p>
            <p className="text-lg sm:text-xl font-semibold text-foreground mb-2">
              No stonks found
            </p>
            <p className="text-sm sm:text-base text-muted-foreground">
              Try adjusting your search or check back later for more tendies
            </p>
          </div>
        )}

        {/* Footer */}
        <footer className="text-center py-6 sm:py-8 border-t border-border/50">
          <p className="text-muted-foreground text-xs sm:text-sm">
            Not financial advice - Always DYOR
          </p>
          <p className="text-[10px] sm:text-xs text-muted-foreground/50 mt-2">
            stonksfeed.com
          </p>
        </footer>
      </main>
    </div>
  );
};

export default Index;
