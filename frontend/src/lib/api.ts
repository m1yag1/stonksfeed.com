/** API response types */
export interface Article {
  headline: string;
  publisher: string;
  feed_title: string;
  pubdate: number;
  link: string;
  source_type: string;
  author?: string;
}

export interface ArticlesResponse {
  articles: Article[];
}

/** Frontend-friendly article type */
export interface NewsItem {
  id: string;
  title: string;
  publisher: string;
  feedTitle: string;
  date: Date;
  link: string;
  sourceType: string;
}

/**
 * Fetch articles from the API.
 */
export async function fetchArticles(limit: number = 100): Promise<NewsItem[]> {
  const response = await fetch(`/api/articles?limit=${limit}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch articles: ${response.statusText}`);
  }

  const data: ArticlesResponse = await response.json();

  return data.articles.map((article, index) => ({
    id: `${article.pubdate}-${index}`,
    title: article.headline,
    publisher: article.publisher,
    feedTitle: article.feed_title,
    date: new Date(article.pubdate * 1000),
    link: article.link,
    sourceType: article.source_type,
  }));
}
