import { useQuery } from '@tanstack/react-query';
import { fetchArticles, NewsItem } from '@/lib/api';

export function useArticles(limit: number = 200) {
  return useQuery<NewsItem[], Error>({
    queryKey: ['articles', limit],
    queryFn: () => fetchArticles(limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: false,
  });
}
