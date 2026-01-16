import { useState } from 'react';
import { ChevronDown, ChevronUp, Filter, X } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

interface FilterSection {
  title: string;
  items: string[];
  selected: Set<string>;
  onToggle: (item: string) => void;
  icon?: string;
}

interface FilterWidgetProps {
  publishers: string[];
  feedTitles: string[];
  sourceTypes: string[];
  sentiments: string[];
  selectedPublishers: Set<string>;
  selectedFeeds: Set<string>;
  selectedSourceTypes: Set<string>;
  selectedSentiments: Set<string>;
  onPublisherToggle: (publisher: string) => void;
  onFeedToggle: (feed: string) => void;
  onSourceTypeToggle: (sourceType: string) => void;
  onSentimentToggle: (sentiment: string) => void;
  onClearAll: () => void;
}

const FilterSectionContent = ({ title, items, selected, onToggle, icon }: FilterSection) => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger className="flex items-center justify-between w-full py-2 px-1 text-sm font-semibold text-foreground hover:text-primary transition-colors">
        <span className="flex items-center gap-2">
          {icon && <span>{icon}</span>}
          {title}
          {selected.size > 0 && (
            <Badge variant="secondary" className="text-[10px] px-1.5 py-0 h-4">
              {selected.size}
            </Badge>
          )}
        </span>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-muted-foreground" />
        ) : (
          <ChevronDown className="w-4 h-4 text-muted-foreground" />
        )}
      </CollapsibleTrigger>
      <CollapsibleContent className="space-y-1 pb-3">
        {items.map((item) => (
          <label
            key={item}
            className="flex items-center gap-2.5 py-1.5 px-1 rounded-md hover:bg-accent/10 cursor-pointer transition-colors group"
          >
            <Checkbox
              checked={selected.has(item)}
              onCheckedChange={() => onToggle(item)}
              className="border-muted-foreground/50 data-[state=checked]:bg-primary data-[state=checked]:border-primary"
            />
            <span className="text-xs sm:text-sm text-muted-foreground group-hover:text-foreground transition-colors truncate">
              {item}
            </span>
          </label>
        ))}
      </CollapsibleContent>
    </Collapsible>
  );
};

const FilterWidget = ({
  publishers,
  feedTitles,
  sourceTypes,
  sentiments,
  selectedPublishers,
  selectedFeeds,
  selectedSourceTypes,
  selectedSentiments,
  onPublisherToggle,
  onFeedToggle,
  onSourceTypeToggle,
  onSentimentToggle,
  onClearAll,
}: FilterWidgetProps) => {
  const totalSelected = selectedPublishers.size + selectedFeeds.size + selectedSourceTypes.size + selectedSentiments.size;

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className="h-10 sm:h-11 px-3 sm:px-4 gap-2 bg-card/50 border-border/50 hover:bg-accent/10 hover:border-primary/50 transition-all"
        >
          <Filter className="w-4 h-4 text-primary" />
          <span className="text-sm">Filters</span>
          {totalSelected > 0 && (
            <Badge className="bg-primary text-primary-foreground text-[10px] px-1.5 h-5 min-w-5 flex items-center justify-center">
              {totalSelected}
            </Badge>
          )}
          <ChevronDown className="w-4 h-4 text-muted-foreground ml-1" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-72 sm:w-80 p-0 bg-card border-border/50"
        align="start"
        sideOffset={8}
      >
        <div className="p-4 space-y-2 max-h-[60vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between pb-2 border-b border-border/30">
            <span className="flex items-center gap-2 text-sm font-semibold">
              <Filter className="w-4 h-4 text-primary" />
              Filters
            </span>
            {totalSelected > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onClearAll}
                className="h-7 px-2 text-xs text-muted-foreground hover:text-destructive"
              >
                <X className="w-3 h-3 mr-1" />
                Clear all
              </Button>
            )}
          </div>

          {/* Sentiment */}
          <FilterSectionContent
            title="Sentiment"
            icon="📊"
            items={sentiments}
            selected={selectedSentiments}
            onToggle={onSentimentToggle}
          />

          {/* Source Type */}
          <FilterSectionContent
            title="Source Type"
            icon="📡"
            items={sourceTypes}
            selected={selectedSourceTypes}
            onToggle={onSourceTypeToggle}
          />

          {/* Publishers */}
          <FilterSectionContent
            title="Publishers"
            icon="🏢"
            items={publishers}
            selected={selectedPublishers}
            onToggle={onPublisherToggle}
          />

          {/* Feeds */}
          <FilterSectionContent
            title="Feeds"
            icon="📰"
            items={feedTitles}
            selected={selectedFeeds}
            onToggle={onFeedToggle}
          />
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default FilterWidget;
