import React, { useMemo, useState, useRef, useEffect } from "react";
import { ColDef } from "ag-grid-community";
import { Search } from "lucide-react";
import { DataGrid, DataGridHandle } from "./DataGrid";
import { SmartSearchPalette, SearchResultItem } from "./SmartSearchPalette";

export interface SuperDataGridProps<T> {
  data: T[];
  columnDefs?: ColDef<T>[];
  title?: string;
  gridId?: string;
  idField?: keyof T;
  titleField?: keyof T;
  subtitleField?: keyof T;
  imageField?: keyof T;
  isLoading?: boolean;
  searchPlaceholder?: string;
}

export function SuperDataGrid<T extends Record<string, any>>({
  data,
  columnDefs: userColumnDefs,
  title = "البيانات",
  gridId = "super-grid",
  idField,
  titleField,
  subtitleField,
  imageField,
  isLoading = false,
  searchPlaceholder = "البحث الشامل...",
}: SuperDataGridProps<T>) {
  const gridRef = useRef<DataGridHandle>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);

  // Auto-generate columns if not provided
  const columnDefs = useMemo<ColDef<T>[]>(() => {
    if (userColumnDefs && userColumnDefs.length > 0) return userColumnDefs;
    if (!data || data.length === 0) return [];

    const sample = data[0];
    return Object.keys(sample).map((key) => {
      const val = sample[key];
      const isNumber = typeof val === "number";
      const isBoolean = typeof val === "boolean";
      
      return {
        headerName: key,
        field: key as any,
        filter: isNumber ? "agNumberColumnFilter" : "agTextColumnFilter",
        width: 150,
      };
    });
  }, [data, userColumnDefs]);

  // Guess the fields if not provided
  const actualIdField = useMemo(() => {
    if (idField) return idField;
    if (data.length === 0) return "" as keyof T;
    const keys = Object.keys(data[0]);
    return (keys.find(k => k.toLowerCase().includes('id') || k.includes('رقم')) || keys[0]) as keyof T;
  }, [data, idField]);

  const actualTitleField = useMemo(() => {
    if (titleField) return titleField;
    if (data.length === 0) return "" as keyof T;
    const keys = Object.keys(data[0]);
    return (keys.find(k => k.toLowerCase().includes('name') || k.toLowerCase().includes('title') || k.includes('اسم')) || keys[1] || keys[0]) as keyof T;
  }, [data, titleField]);

  const actualSubtitleField = useMemo(() => {
    if (subtitleField) return subtitleField;
    if (data.length === 0) return undefined;
    const keys = Object.keys(data[0]);
    return keys.find(k => k.toLowerCase().includes('job') || k.toLowerCase().includes('role') || k.toLowerCase().includes('email') || k.includes('منصب') || k.includes('رتبة')) as keyof T;
  }, [data, subtitleField]);

  // Handle Search Keyboard Shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "f" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setSearchOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Filter Search Results
  const searchResults = useMemo(() => {
    if (!searchQuery || !data) return [];
    const lowerQuery = searchQuery.toLowerCase();
    
    const filtered = data.filter(r => 
      Object.values(r).some(val => 
        val !== null && val !== undefined && String(val).toLowerCase().includes(lowerQuery)
      )
    );
    
    return filtered.slice(0, 50).map((r: any) => ({
      id: String(r[actualIdField]),
      title: String(r[actualTitleField] || "بدون عنوان"),
      subtitle: actualSubtitleField ? String(r[actualSubtitleField]) : undefined,
      image: imageField ? String(r[imageField]) : undefined,
      rawData: r
    }));
  }, [data, searchQuery, actualIdField, actualTitleField, actualSubtitleField, imageField]);

  return (
    <div className="flex h-screen w-full flex-col">
      <DataGrid 
        ref={gridRef}
        rowData={data} 
        columnDefs={columnDefs as any} 
        title={title} 
        gridId={gridId}
        isLoading={isLoading}
        searchTrigger={
          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground bg-muted/50 hover:bg-muted border border-border rounded-md transition-colors w-64 shadow-sm"
          >
            <Search className="w-4 h-4" />
            <span className="flex-1 text-right">{searchPlaceholder}</span>
            <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-70">
              <span className="text-xs">⌘</span>F
            </kbd>
          </button>
        }
      />
      
      <SmartSearchPalette 
        open={searchOpen} 
        onOpenChange={setSearchOpen}
        query={searchQuery}
        results={searchResults}
        onSearch={setSearchQuery}
        placeholder={searchPlaceholder}
        onSelectResult={(item: SearchResultItem) => {
          setSearchOpen(false);
          if (gridRef.current && actualIdField) {
            gridRef.current.selectRowById(item.id, String(actualIdField));
          }
        }}
      />
    </div>
  );
}
