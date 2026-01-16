export interface NewsItem {
  id: string;
  title: string;
  publisher: string;
  feedTitle: string;
  date: Date;
  summary: string;
  ticker?: string;
}

export const mockNews: NewsItem[] = [
  {
    id: '1',
    title: 'GME to the Moon: Retail Traders Rally Again 🚀',
    publisher: 'Bloomberg',
    feedTitle: 'Market Watch',
    date: new Date('2026-01-15T10:30:00'),
    summary: 'Diamond hands are back as GameStop sees unusual trading volume. Apes together strong.',
    ticker: 'GME',
  },
  {
    id: '2',
    title: 'Fed Signals Rate Cut: Markets React',
    publisher: 'Reuters',
    feedTitle: 'Fed News',
    date: new Date('2026-01-15T09:15:00'),
    summary: 'Federal Reserve hints at potential rate cuts in upcoming meetings, sending markets higher.',
  },
  {
    id: '3',
    title: 'NVDA Earnings Beat Expectations Again',
    publisher: 'CNBC',
    feedTitle: 'Tech Stocks',
    date: new Date('2026-01-14T16:00:00'),
    summary: 'NVIDIA reports record quarterly revenue driven by AI chip demand. Stock pumps AH.',
    ticker: 'NVDA',
  },
  {
    id: '4',
    title: 'Crypto Market Sees Red: BTC Dips Below Key Level',
    publisher: 'CoinDesk',
    feedTitle: 'Crypto Watch',
    date: new Date('2026-01-14T14:20:00'),
    summary: 'Bitcoin falls 5% as whale wallets move coins to exchanges. HODL or fold?',
    ticker: 'BTC',
  },
  {
    id: '5',
    title: 'TSLA Cybertruck Production Ramps Up',
    publisher: 'WSJ',
    feedTitle: 'Auto Industry',
    date: new Date('2026-01-14T11:45:00'),
    summary: 'Tesla announces increased Cybertruck production capacity at Giga Texas.',
    ticker: 'TSLA',
  },
  {
    id: '6',
    title: 'Meme Stocks 2.0: New Retail Wave Incoming',
    publisher: 'MarketWatch',
    feedTitle: 'Market Watch',
    date: new Date('2026-01-13T15:30:00'),
    summary: 'Social media buzz indicates renewed interest in meme stocks. WSB activity surges.',
  },
  {
    id: '7',
    title: 'Apple Vision Pro Sales Disappoint Analysts',
    publisher: 'Bloomberg',
    feedTitle: 'Tech Stocks',
    date: new Date('2026-01-13T12:00:00'),
    summary: 'AAPL mixed reality headset sees slower than expected adoption.',
    ticker: 'AAPL',
  },
  {
    id: '8',
    title: 'SPY Hits All-Time High as Bulls Dominate',
    publisher: 'Reuters',
    feedTitle: 'Index Tracking',
    date: new Date('2026-01-13T09:30:00'),
    summary: 'S&P 500 breaks records in strongest January rally in years. Tendies for everyone.',
    ticker: 'SPY',
  },
  {
    id: '9',
    title: 'Oil Prices Surge on Supply Concerns',
    publisher: 'CNBC',
    feedTitle: 'Commodities',
    date: new Date('2026-01-12T14:15:00'),
    summary: 'Crude oil jumps 3% amid geopolitical tensions. Energy sector leads gains.',
  },
  {
    id: '10',
    title: 'AMD vs NVDA: The AI Chip War Heats Up',
    publisher: 'The Verge',
    feedTitle: 'Tech Stocks',
    date: new Date('2026-01-12T10:00:00'),
    summary: 'AMD announces new AI accelerator to compete with NVIDIA dominance. Wen moon?',
    ticker: 'AMD',
  },
];

export const publishers = [...new Set(mockNews.map(n => n.publisher))];
export const feedTitles = [...new Set(mockNews.map(n => n.feedTitle))];