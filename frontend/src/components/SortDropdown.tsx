import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ArrowUpDown } from 'lucide-react';

export type SortOption = 'date' | 'publisher' | 'feedTitle';

interface SortDropdownProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
}

const SortDropdown = ({ value, onChange }: SortDropdownProps) => {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-full sm:w-[180px] h-11 sm:h-10 bg-secondary border-border">
        <ArrowUpDown className="w-4 h-4 mr-2 text-muted-foreground" />
        <SelectValue placeholder="Sort by..." />
      </SelectTrigger>
      <SelectContent className="bg-popover border-border">
        <SelectItem value="date">📅 Date</SelectItem>
        <SelectItem value="publisher">🏢 Publisher</SelectItem>
        <SelectItem value="feedTitle">📰 Feed Title</SelectItem>
      </SelectContent>
    </Select>
  );
};

export default SortDropdown;