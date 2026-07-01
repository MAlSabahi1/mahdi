import React, { useState, useEffect, useRef } from "react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { ChevronLeft, Search, User, X, Info } from "lucide-react";

export interface SearchResultItem {
  id: string;
  title: string;
  subtitle?: string;
  image?: string;
  rawData: any;
}

interface SmartSearchPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  placeholder?: string;
  query: string;
  results: SearchResultItem[];
  onSearch: (query: string) => void;
  renderPreview?: (item: SearchResultItem) => React.ReactNode;
  onSelectResult?: (item: SearchResultItem) => void;
}

export function GenericPreviewRenderer({ item }: { item: SearchResultItem }) {
  const data = item.rawData || {};
  const entries = Object.entries(data).filter(([k, v]) => {
    if (v === null || v === undefined || v === "") return false;
    if (typeof v === "object") return false;
    return true;
  });

  return (
    <div className="flex flex-col h-full w-full bg-background pt-8 pb-6 px-8 overflow-y-auto">
      <div className="flex flex-col items-center text-center">
        {item.image ? (
          <img src={item.image} alt={item.title} className="w-20 h-20 rounded-full object-cover mb-4 ring-2 ring-border/50 shadow-sm" />
        ) : (
          <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-4 ring-2 ring-border/50 shadow-sm text-muted-foreground">
            <User className="w-8 h-8 opacity-70" />
          </div>
        )}
        <h2 className="text-[17px] font-bold text-foreground">{item.title}</h2>
        {item.subtitle && <p className="text-[13px] text-muted-foreground mt-0.5">{item.subtitle}</p>}
      </div>
      
      <div className="w-full pt-6 border-t border-border mt-6">
        <div className="grid grid-cols-2 gap-x-8 gap-y-4">
          {entries.map(([key, value]) => (
            <div key={key} className="flex flex-col gap-1 border-b border-border/40 pb-2">
              <div className="flex items-center gap-2">
                <Info className="w-3.5 h-3.5 text-primary/70" />
                <span className="text-[12px] font-semibold text-muted-foreground">{key}</span>
              </div>
              <span className="text-[14px] font-medium text-foreground pr-5 break-words">
                {String(value)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function SmartSearchPalette({
  open,
  onOpenChange,
  placeholder = "ابحث بالاسم أو الرقم...",
  query,
  results,
  onSearch,
  renderPreview,
  onSelectResult
}: SmartSearchPaletteProps) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) setHoveredId(null);
  }, [open]);

  const activeItem = hoveredId ? results.find(r => r.id === hoveredId) : results[0];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent aria-describedby={undefined} className="max-w-[850px] p-0 overflow-hidden bg-background rounded-xl border-border shadow-2xl [&>button]:hidden" dir="rtl">
        <DialogTitle className="sr-only">البحث الشامل</DialogTitle>
        <DialogDescription className="sr-only">نافذة البحث عن الموظفين والملفات</DialogDescription>
        
        <Command shouldFilter={false} className="flex flex-col w-full bg-transparent">
          
          {/* Top Search Bar */}
          <div className="flex items-center border-b border-border pl-4 pr-2 py-1.5 bg-background w-full">
            <div className="flex-1 flex items-center relative">
              <CommandInput 
                ref={inputRef}
                value={query}
                placeholder={placeholder} 
                onValueChange={onSearch}
                className="border-none focus:ring-0 shadow-none outline-none h-12 w-full text-[15px] bg-transparent [&_[cmdk-input]]:px-4 flex-1" 
              />
              {query && (
                <button 
                  onClick={() => onSearch("")}
                  className="absolute left-4 p-1.5 rounded-full hover:bg-muted text-muted-foreground transition-colors"
                  title="مسح البحث"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Main Dialog Close Button (Far Left) */}
            <div className="mr-auto flex items-center pr-4 border-r border-border/50 h-8">
              <button 
                onClick={() => onOpenChange(false)}
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-accent text-muted-foreground transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
                title="إغلاق النافذة"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="flex h-[450px] w-full">
            {/* Left Pane: Results List */}
            <div className="w-[40%] flex flex-col border-l border-border bg-card">
              <CommandList className="flex-1 max-h-none overflow-y-auto px-2 py-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
                <CommandEmpty className="py-12 text-center">
                  <div className="flex flex-col items-center justify-center text-muted-foreground">
                    <Search className="h-8 w-8 opacity-20 mb-4" />
                    <p className="text-[15px] font-medium">لا توجد نتائج</p>
                  </div>
                </CommandEmpty>
                <CommandGroup heading="نتائج البحث" className="[&_[cmdk-group-heading]]:text-muted-foreground [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-semibold [&_[cmdk-group-heading]]:mb-2 [&_[cmdk-group-heading]]:px-3">
                  {results.map((item) => {
                    const isActive = activeItem?.id === item.id;
                    return (
                      <CommandItem
                        key={item.id}
                        value={item.id} // use ID as value so it's unique
                        onSelect={() => {
                          onOpenChange(false);
                          if (onSelectResult) onSelectResult(item);
                        }}
                        onMouseEnter={() => setHoveredId(item.id)}
                        className={`flex items-center justify-between px-3 py-2.5 rounded-lg mb-1 cursor-pointer transition-colors border-r-4 ${isActive ? "bg-muted border-r-primary text-foreground" : "border-r-transparent text-muted-foreground hover:bg-muted/50 hover:text-foreground hover:border-r-border"}`}
                      >
                        <div className="flex items-center gap-3">
                          {item.image ? (
                            <img src={item.image} alt={item.title} className="w-8 h-8 rounded-full object-cover shadow-sm border border-border/50" />
                          ) : (
                            <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center border border-border/50 text-muted-foreground">
                              <User className="w-4 h-4 opacity-70" />
                            </div>
                          )}
                          <span className={`text-[15px] ${isActive ? "font-semibold" : "font-medium"}`}>{item.title}</span>
                        </div>
                        {isActive && <ChevronLeft className="w-4 h-4 opacity-50" />}
                      </CommandItem>
                    );
                  })}
                </CommandGroup>
              </CommandList>
            </div>

            {/* Right Pane: Preview Pane */}
            <div className="w-[60%] flex flex-col bg-background">
              {activeItem ? (
                renderPreview ? renderPreview(activeItem) : <GenericPreviewRenderer item={activeItem} />
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-30">
                  <User className="h-16 w-16 mb-4" />
                </div>
              )}
            </div>
          </div>
        </Command>
      </DialogContent>
    </Dialog>
  );
}
