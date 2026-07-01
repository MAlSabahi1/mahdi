import React, { forwardRef, useImperativeHandle, useMemo, useRef, useCallback, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import {
  ModuleRegistry,
  AllCommunityModule,
  themeQuartz,
  themeBalham,
  themeAlpine,
  themeMaterial,
  colorSchemeDark,
  type ColDef,
  type ColGroupDef,
  type GridReadyEvent,
  type ExcelStyle,
} from "ag-grid-community";
import { AllEnterpriseModule, LicenseManager } from "ag-grid-enterprise";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  Download,
  Maximize2,
  Minimize2,
  Palette,
  FileSpreadsheet,
  FileText,
  Moon,
  Sun,
  Droplet,
  BookOpen,
  Snowflake,
  Eye,
  Zap,
  Settings2,
  FilterX,
  PinOff
} from "lucide-react";
import { GridSettingsDrawer, ColumnConfig, UserRole } from "./GridSettingsDrawer";
import { GridSkeleton } from "./GridSkeleton";

ModuleRegistry.registerModules([AllCommunityModule, AllEnterpriseModule]);
LicenseManager.setLicenseKey("");

export interface DataGridHandle {
  exportCsv: () => void;
  exportExcel: () => void;
  selectRowById: (id: string, idField: string) => void;
};

export type DataGridProps<T> = {
  rowData: T[];
  columnDefs: (ColDef<T> | ColGroupDef<T>)[];
  height?: string | number;
  fileName?: string;
  sheetName?: string;
  rtl?: boolean;
  showToolbar?: boolean;
  title?: string;
  gridId?: string;
  isLoading?: boolean;
  renderRowActions?: (row: T) => React.ReactNode;
  toolbarExtra?: React.ReactNode;
  searchTrigger?: React.ReactNode;
};

type ThemeKey = "quartz" | "balham" | "alpine" | "material";
type Density = "compact" | "normal" | "comfortable";

const THEME_MAP = { quartz: themeQuartz, balham: themeBalham, alpine: themeAlpine, material: themeMaterial };

const PRODUCTIVITY_COLORS = [
  { name: "الافتراضي (Default)", value: "default" },
  { name: "أزرق مؤسسي", value: "#2563eb" }, // Blue
  { name: "أخضر زمردي", value: "#059669" }, // Emerald
  { name: "بنفسجي هادئ", value: "#7c3aed" }, // Violet
  { name: "رمادي معدني", value: "#475569" }, // Slate
  { name: "نيلي احترافي", value: "#4f46e5" }, // Indigo
  { name: "أزرق محيطي", value: "#0284c7" }, // Sky/Ocean Blue
  { name: "فيروزي مريح", value: "#0d9488" }, // Teal
  { name: "وردي ناعم", value: "#e11d48" }, // Rose
  { name: "كهرماني دافئ", value: "#d97706" }, // Amber
];

const VIEW_MODES = [
  { id: "light", name: "الوضع الفاتح", icon: Sun, bg: "#FFFFFF", fg: "#0F172A", isDark: false },
  { id: "dark", name: "الوضع الليلي", icon: Moon, bg: "#020617", fg: "#F8FAFC", isDark: true },
  { id: "sepia", name: "حماية العين (ورقي)", icon: BookOpen, bg: "#F4ECD8", fg: "#433422", isDark: false },
  { id: "nord", name: "هادئ ثلجي", icon: Snowflake, bg: "#ECEFF4", fg: "#2E3440", isDark: false },
  { id: "solarized", name: "تركيز عميق", icon: Zap, bg: "#002B36", fg: "#839496", isDark: true },
];

// ===== Professional Excel styles =====
const THIN = (c = "#BFCBD9") => ({ color: c, lineStyle: "Continuous" as const, weight: 1 as const });
const THICK = (c = "#0B3D91") => ({ color: c, lineStyle: "Continuous" as const, weight: 3 as const });
const FONT = { fontName: "Calibri", size: 11, color: "#1F2937" };

const ALL_THIN = {
  borderTop: THIN(), borderBottom: THIN(), borderLeft: THIN(), borderRight: THIN(),
};
const ALL_THICK = {
  borderTop: THICK(), borderBottom: THICK(), borderLeft: THICK(), borderRight: THICK(),
};

const EXCEL_STYLES: ExcelStyle[] = [
  // Report title bar
  {
    id: "reportTitle",
    font: { ...FONT, bold: true, color: "#FFFFFF", size: 16 },
    interior: { color: "#0B3D91", pattern: "Solid" },
    alignment: { horizontal: "Center", vertical: "Center" },
    borders: ALL_THICK,
  },
  {
    id: "reportSubtitle",
    font: { ...FONT, italic: true, color: "#475569", size: 10 },
    interior: { color: "#F1F5F9", pattern: "Solid" },
    alignment: { horizontal: "Center", vertical: "Center" },
    borders: ALL_THIN,
  },
  // Group header (top tier) — thick navy bar
  {
    id: "headerGroup",
    font: { ...FONT, bold: true, color: "#FFFFFF", size: 12 },
    interior: { color: "#1E40AF", pattern: "Solid" },
    alignment: { horizontal: "Center", vertical: "Center", wrapText: true },
    borders: {
      borderTop: THICK(), borderBottom: THICK("#1E3A8A"),
      borderLeft: THIN("#1E3A8A"), borderRight: THIN("#1E3A8A"),
    },
  },
  // Column header — bold, light gray, thick bottom rule
  {
    id: "header",
    font: { ...FONT, bold: true, color: "#0F172A", size: 11 },
    interior: { color: "#E5EAF2", pattern: "Solid" },
    alignment: { horizontal: "Center", vertical: "Center", wrapText: true },
    borders: {
      borderTop: THIN("#94A3B8"), borderBottom: THICK("#0B3D91"),
      borderLeft: THIN("#94A3B8"), borderRight: THIN("#94A3B8"),
    },
  },
  // Default cell — thin grid lines on every cell
  {
    id: "cell",
    font: FONT,
    alignment: { vertical: "Center" },
    borders: ALL_THIN,
  },
  // Zebra striping
  {
    id: "oddRow",
    font: FONT,
    interior: { color: "#F8FAFC", pattern: "Solid" },
    alignment: { vertical: "Center" },
    borders: ALL_THIN,
  },
  // Currency cells — right aligned, thousands separator + $
  {
    id: "currency",
    font: FONT,
    numberFormat: { format: "_-* #,##0 \"$\"_-;-* #,##0 \"$\"_-;_-* \"-\"_-;_-@_-" },
    alignment: { horizontal: "Right", vertical: "Center" },
    borders: ALL_THIN,
  },
  {
    id: "number",
    font: FONT,
    numberFormat: { format: "#,##0" },
    alignment: { horizontal: "Right", vertical: "Center" },
    borders: ALL_THIN,
  },
  {
    id: "boolean",
    font: FONT,
    alignment: { horizontal: "Center", vertical: "Center" },
    borders: ALL_THIN,
  },
];





function buildDefaultColDef(density: Density): ColDef {
  return {
    sortable: true,
    resizable: true,
    floatingFilter: true,
    enableRowGroup: true,
    enableValue: true,
    enablePivot: true,
    editable: true,
    minWidth: 110,
    // Excel-grade filter: text/number/date + set + conditions, all combined
    filter: "agMultiColumnFilter",
    filterParams: {
      filters: [
        { filter: "agTextColumnFilter", display: "subMenu" },
        { filter: "agSetColumnFilter" },
      ],
    },
    menuTabs: ["filterMenuTab", "generalMenuTab", "columnsMenuTab"],
  };
}

export const DataGrid = forwardRef(function DataGrid<T>(
  {
    rowData,
    columnDefs,
    height = "100%",
    fileName = "data-export",
    sheetName = "البيانات",
    rtl = true,
    showToolbar = true,
    title,
    gridId,
    isLoading = false,
    renderRowActions,
    toolbarExtra,
    searchTrigger,
  }: DataGridProps<T>,
  ref: React.Ref<DataGridHandle>,
) {
  const gridRef = useRef<AgGridReact<T>>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const [themeKey, setThemeKey] = useState<ThemeKey>("quartz");
  const [density, setDensity] = useState<Density>("normal");
  const [fullscreen, setFullscreen] = useState(false);
  const [viewModeId, setViewModeId] = useState<string>("light");
  const [accentColor, setAccentColor] = useState<string>(PRODUCTIVITY_COLORS[0].value);

  // Configuration State for Settings Engine
  const extractColumns = useCallback((defs: any[]): ColumnConfig[] => {
    let cols: ColumnConfig[] = [];
    defs.forEach(def => {
      if (def.children) {
        cols = cols.concat(extractColumns(def.children));
      } else if (def.field) {
        cols.push({
          field: def.field,
          headerName: def.headerName || def.field,
          isVisible: true,
          isExportable: true,
          isEditable: def.editable !== false,
        });
      }
    });
    return cols;
  }, []);

  const [currentUserRole, setCurrentUserRole] = useState<UserRole>("admin");
  const [columnConfigs, setColumnConfigs] = useState<ColumnConfig[]>(() => {
    if (gridId) {
      try {
        const saved = localStorage.getItem(`lovable-grid-settings-${gridId}`);
        if (saved) return JSON.parse(saved);
      } catch (e) {
        console.error("Failed to load grid settings", e);
      }
    }
    return [];
  });

  // Sync configs dynamically when columnDefs from parent changes (API data, generic reuse)
  React.useEffect(() => {
    setColumnConfigs((prev) => {
      const newCols = extractColumns(columnDefs);
      // Merge new cols with prev config to preserve user settings if the column already existed
      return newCols.map(newCol => {
        const existing = prev.find(p => p.field === newCol.field);
        if (existing) {
          return { 
            ...newCol, 
            isVisible: existing.isVisible, 
            isExportable: existing.isExportable, 
            isEditable: existing.isEditable,
            pinned: existing.pinned,
          };
        }
        return newCol;
      });
    });
  }, [columnDefs, extractColumns]);

  // Save configs to localStorage whenever they change
  React.useEffect(() => {
    if (gridId && columnConfigs.length > 0) {
      localStorage.setItem(`lovable-grid-settings-${gridId}`, JSON.stringify(columnConfigs));
    }
  }, [gridId, columnConfigs]);

  // Middleware to apply configuration on the fly
  const processedColumnDefs = useMemo(() => {
    const processDefs = (defs: any[]): any[] => {
      return defs.map(def => {
        if (def.children) {
          return { ...def, children: processDefs(def.children) };
        }
        const config = columnConfigs.find(c => c.field === def.field);
        if (config) {
          return {
            ...def,
            hide: !config.isVisible,
            suppressColumnsToolPanel: !config.isVisible,
            editable: config.isEditable && (currentUserRole === "admin" || currentUserRole === "hr"),
            pinned: config.pinned || def.pinned, // Apply user setting or default
          };
        }
        return def;
      });
    };
    
    let processed = processDefs(columnDefs);

    // Dynamic Actions Column Integration
    if (renderRowActions) {
      processed = [
        ...processed,
        {
          headerName: "الإجراءات",
          field: "actions",
          pinned: rtl ? "left" : "right",
          width: 120,
          minWidth: 120,
          suppressMenu: true,
          suppressHeaderMenuButton: true,
          suppressMovable: true,
          lockPosition: "left",
          sortable: false,
          filter: false,
          resizable: false,
          editable: false,
          cellRenderer: (params: any) => {
            if (!params.data) return null;
            return renderRowActions(params.data);
          }
        }
      ];
    }
    
    // Inject Skeleton Renderer into all columns when loading
    if (isLoading) {
      const applySkeleton = (defs: any[]): any[] => {
        return defs.map(def => {
          if (def.children) {
            return { ...def, children: applySkeleton(def.children) };
          }
          // Skip skeleton for action columns, render them as disabled/dimmed
          if (def.headerName === "الإجراءات" || def.field === "actions") {
            return {
              ...def,
              cellRenderer: (params: any) => (
                <div className="opacity-30 pointer-events-none grayscale flex h-full w-full">
                  {typeof def.cellRenderer === 'function' ? def.cellRenderer(params) : null}
                </div>
              )
            };
          }
          return {
            ...def,
            cellRenderer: () => (
              <div className="flex items-center h-full w-full py-1">
                <div className="h-5 w-[80%] bg-slate-200 dark:bg-slate-800 animate-pulse rounded-sm"></div>
              </div>
            )
          };
        });
      };
      processed = applySkeleton(processed);
    }
    
    return processed;
  }, [columnDefs, columnConfigs, currentUserRole, renderRowActions, rtl, isLoading]);

  const fakeRowData = useMemo(() => Array.from({ length: 15 }).map((_, i) => ({ _id: `skeleton-${i}` }) as unknown as T), []);

  const handleConfigChange = (field: string, key: keyof ColumnConfig, value: any) => {
    setColumnConfigs(prev => prev.map(c => c.field === field ? { ...c, [key]: value } : c));
  };

  const defaultColDef = useMemo<ColDef>(() => buildDefaultColDef(density), [density]);

  const currentMode = useMemo(() => VIEW_MODES.find(m => m.id === viewModeId) || VIEW_MODES[0], [viewModeId]);

  // Sync with HTML class for Tailwind
  React.useEffect(() => {
    const root = document.documentElement;
    // Remove all theme classes and dark
    root.classList.remove("dark", "theme-sepia", "theme-nord", "theme-solarized");
    
    if (currentMode.isDark) {
      root.classList.add("dark");
    }
    if (currentMode.id !== "light" && currentMode.id !== "dark") {
      root.classList.add(`theme-${currentMode.id}`);
    }
  }, [currentMode]);

  const theme = useMemo(() => {
    let params: any = {
      fontFamily: "'Cairo', system-ui, -apple-system, sans-serif",
      ...(accentColor !== "default" ? { accentColor } : {}),
    };

    let baseTheme = THEME_MAP[themeKey].withParams(params);
    
    // Add dark mode part if the mode is dark
    if (currentMode.isDark) {
      baseTheme = baseTheme.withPart(colorSchemeDark);
    }
    
    return baseTheme;
  }, [themeKey, currentMode, accentColor]);

  const sideBar = useMemo(
    () => ({
      toolPanels: [
        {
          id: "columns",
          labelDefault: "أعمدة",
          labelKey: "columns",
          iconKey: "columns",
          toolPanel: "agColumnsToolPanel",
          toolPanelParams: { suppressRowGroups: false, suppressValues: false, suppressPivots: false },
        },
        {
          id: "filters",
          labelDefault: "المرشحات",
          labelKey: "filters",
          iconKey: "filter",
          toolPanel: "agFiltersToolPanel",
        },
      ],
    }),
    [],
  );

  const localeText = useMemo(
    () => ({
      page: "صفحة", to: "إلى", of: "من",
      rowGroupColumnsEmptyMessage: "اسحب هنا لتعيين مجموعات الصفوف",
      valueColumnsEmptyMessage: "اسحب هنا لتجميع القيم",
      pivotColumnsEmptyMessage: "اسحب هنا لتعيين أعمدة المحور",
      pivotMode: "وضع المحور", groups: "مجموعات الصفوف",
      values: "قيم", pivots: "المحور",
      noRowsToShow: "لا توجد صفوف لعرضها",
      filterOoo: "فلتر...", searchOoo: "بحث...", blanks: "(فارغ)",
      selectAll: "تحديد الكل", selectAllSearchResults: "تحديد نتائج البحث",
      applyFilter: "تطبيق", resetFilter: "إعادة تعيين", clearFilter: "مسح", cancelFilter: "إلغاء",
      equals: "يساوي", notEqual: "لا يساوي", lessThan: "أقل من", greaterThan: "أكبر من",
      lessThanOrEqual: "أقل من أو يساوي", greaterThanOrEqual: "أكبر من أو يساوي",
      inRange: "بين", contains: "يحتوي", notContains: "لا يحتوي",
      startsWith: "يبدأ بـ", endsWith: "ينتهي بـ",
      andCondition: "و", orCondition: "أو",
      sum: "مجموع", avg: "متوسط", min: "أدنى", max: "أعلى",
      count: "عدد", totalRows: "صفوف", filteredRows: "مفلتر", selectedRows: "محدد",
      columns: "أعمدة", filters: "المرشحات", export: "تصدير", csvExport: "تصدير CSV", excelExport: "تصدير Excel",
      pinColumn: "تثبيت العمود", pinLeft: "تثبيت لليسار", pinRight: "تثبيت لليمين", noPin: "إلغاء التثبيت",
      autosizeThiscolumn: "تكبير هذا العمود تلقائياً", autosizeAllColumns: "تكبير كل الأعمدة تلقائياً",
      groupBy: "تجميع حسب", ungroupBy: "إلغاء التجميع",
      resetColumns: "إعادة تعيين الأعمدة",
      expandAll: "توسيع الكل", collapseAll: "طي الكل",
      copy: "نسخ", copyWithHeaders: "نسخ مع العناوين", paste: "لصق",
    }),
    [],
  );

  const onGridReady = useCallback((_e: GridReadyEvent<T>) => { }, []);

  const exportCsv = useCallback(() => {
    gridRef.current?.api?.exportDataAsCsv({
      fileName: `${fileName}.csv`,
      processCellCallback: (params) => params.value ?? "",
    });
  }, [fileName]);

  const exportExcel = useCallback(() => {
    if (!gridRef.current?.api) return;
    
    // Filter columns that are marked as exportable in our settings engine
    const exportableColumns = columnConfigs
      .filter(config => config.isExportable)
      .map(config => config.field);

    const colCount = gridRef.current.api.getColumns()?.length ?? 1;
    gridRef.current.api.exportDataAsExcel({
      columnKeys: exportableColumns,
      fileName: `${fileName}.xlsx`,
      sheetName,
      author: "Lovable DataGrid",
      headerRowHeight: 36,
      rowHeight: 22,
      freezeRows: "headersAndPinnedRows",
      freezeColumns: "pinned",
      addImageToCell: undefined,
      prependContent: [
        {
          cells: [
            {
              data: { value: title ?? "تقرير البيانات", type: "String" },
              mergeAcross: Math.max(0, colCount - 1),
              styleId: "reportTitle",
            },
          ],
        },
        {
          cells: [
            {
              data: {
                value: `تم التصدير في: ${new Date().toLocaleString("ar-EG")}  •  ${rowData.length.toLocaleString("ar-EG")} صف`,
                type: "String",
              },
              mergeAcross: Math.max(0, colCount - 1),
              styleId: "reportSubtitle",
            },
          ],
        },
        { cells: [] },
      ],
      processCellCallback: (params) => {
        const v = params.value;
        if (v == null) return "";
        if (typeof v === "boolean") return v ? "نعم" : "لا";
        if (typeof v === "object") return JSON.stringify(v);
        return v;
      },
      processRowGroupCallback: (p) => p.node.key ?? "",
    });
  }, [columnConfigs, fileName, sheetName, title, rowData.length]);

  useImperativeHandle(ref, () => ({ 
    exportCsv, 
    exportExcel,
    selectRowById: (id: string, idField: string) => {
      let foundNode: any = null;
      gridRef.current?.api.forEachNode((node) => {
        if (node.data && String((node.data as any)[idField]) === String(id)) {
          foundNode = node;
        }
      });
      if (foundNode) {
        gridRef.current?.api.ensureNodeVisible(foundNode, 'middle');
        foundNode.setSelected(true, true);
        // Add a temporary flash effect if possible, or just selecting is enough
      }
    }
  }), [exportCsv, exportExcel]);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      wrapRef.current?.requestFullscreen?.();
      setFullscreen(true);
    } else {
      document.exitFullscreen?.();
      setFullscreen(false);
    }
  };

  const clearFilters = useCallback(() => {
    gridRef.current?.api?.setFilterModel(null);
  }, []);

  const clearPins = useCallback(() => {
    if (!gridRef.current?.api) return;
    const currentState = gridRef.current.api.getColumnState();
    const newState = currentState.map(col => {
      const column = gridRef.current!.api.getColumn(col.colId);
      const colDef = column?.getColDef();
      
      // لا نلغي التثبيت عن أعمدة النظام (مثل الإجراءات أو الترقيم)
      if (col.colId === "actions" || colDef?.lockPosition || colDef?.suppressMovable) {
        return col;
      }
      return { ...col, pinned: null };
    });
    gridRef.current.api.applyColumnState({ state: newState });
  }, []);

  return (
    <div ref={wrapRef} className="flex h-full w-full flex-col gap-3 bg-background" dir={rtl ? "rtl" : "ltr"}>
      {showToolbar && (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border bg-card px-4 py-2.5 shadow-sm">
          <div className="flex items-center gap-3 flex-1">
            <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary/10 text-primary">
              <FileSpreadsheet className="h-4 w-4" />
            </div>
            <div className="mr-2">
              <h2 className="text-sm font-semibold text-foreground">{title ?? "جدول البيانات"}</h2>
              <p className="text-xs text-muted-foreground">
                {rowData.length.toLocaleString("ar-EG")} صف
              </p>
            </div>
            {toolbarExtra && <div className="mx-4 flex-1">{toolbarExtra}</div>}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            
            {/* Eye Care Modes Picker */}
            <TooltipProvider delayDuration={200}>
              <div className="flex items-center gap-1.5 mr-2">
                <Eye className="h-4 w-4 text-muted-foreground" />
                <Select value={viewModeId} onValueChange={setViewModeId}>
                  <SelectTrigger className="h-8 w-44 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {VIEW_MODES.map(mode => {
                      const Icon = mode.icon;
                      return (
                        <SelectItem key={mode.id} value={mode.id}>
                          <div className="flex items-center gap-2">
                            <Icon className="h-4 w-4" />
                            <span>{mode.name}</span>
                          </div>
                        </SelectItem>
                      );
                    })}
                  </SelectContent>
                </Select>
              </div>
            </TooltipProvider>

            {/* Grid Settings Engine */}
            <GridSettingsDrawer 
              configs={columnConfigs} 
              onConfigChange={handleConfigChange} 
              currentUserRole={currentUserRole}
              onRoleChange={setCurrentUserRole}
            />

            {/* Accent Color Picker */}
            <TooltipProvider delayDuration={200}>
              <div className="flex items-center gap-1.5 mr-2">
                <Droplet className="h-4 w-4 text-muted-foreground" />
                <Select value={accentColor} onValueChange={setAccentColor}>
                  <SelectTrigger className="h-8 w-36 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {PRODUCTIVITY_COLORS.map(c => (
                      <SelectItem key={c.value} value={c.value}>
                        <div className="flex items-center gap-2">
                          {c.value !== "default" ? (
                            <div className="h-3 w-3 rounded-full" style={{ backgroundColor: c.value }}></div>
                          ) : (
                            <div className="h-3 w-3 rounded-full border border-gray-300 dark:border-gray-600 bg-transparent"></div>
                          )}
                          <span>{c.name}</span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </TooltipProvider>

            <TooltipProvider delayDuration={200}>
              <div className="flex items-center gap-1.5 mr-2">
                <Palette className="h-4 w-4 text-muted-foreground" />
                <Select value={themeKey} onValueChange={(v: string) => setThemeKey(v as ThemeKey)}>
                  <SelectTrigger className="h-8 w-32 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="quartz">Quartz</SelectItem>
                    <SelectItem value="balham">Balham</SelectItem>
                    <SelectItem value="alpine">Alpine</SelectItem>
                    <SelectItem value="material">Material</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </TooltipProvider>

            <Select value={density} onValueChange={(v: string) => setDensity(v as Density)}>
              <SelectTrigger className="h-8 w-28 text-xs">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="compact">مضغوط</SelectItem>
                <SelectItem value="normal">عادي</SelectItem>
                <SelectItem value="comfortable">مريح</SelectItem>
              </SelectContent>
            </Select>

            <TooltipProvider delayDuration={200}>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={exportCsv} className="text-blue-600 hover:bg-blue-50 hover:text-blue-700">
                  <FileText className="h-5 w-5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>تصدير CSV</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={exportExcel} className="text-green-600 hover:bg-green-50 hover:text-green-700">
                  <FileSpreadsheet className="h-5 w-5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>تصدير Excel</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={toggleFullscreen} aria-label="تكبير الشاشة">
                  {fullscreen ? <Minimize2 className="h-5 w-5" /> : <Maximize2 className="h-5 w-5" />}
                </Button>
              </TooltipTrigger>
              <TooltipContent>{fullscreen ? "تصغير" : "تكبير الشاشة"}</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={clearFilters} className="text-orange-600 hover:bg-orange-50 hover:text-orange-700">
                  <FilterX className="h-5 w-5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>مسح جميع المرشحات</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" onClick={clearPins} className="text-purple-600 hover:bg-purple-50 hover:text-purple-700">
                  <PinOff className="h-5 w-5" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>إلغاء تثبيت جميع الأعمدة</TooltipContent>
            </Tooltip>
            </TooltipProvider>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-hidden rounded-lg border bg-card shadow-sm relative" style={{ height }}>
        {searchTrigger && (
          <div className={`absolute top-[4px] ${rtl ? 'left-[16px]' : 'right-[16px]'} z-10`}>
            {searchTrigger}
          </div>
        )}
        <AgGridReact<T>
          ref={gridRef}
          theme={theme}
          rowData={isLoading ? fakeRowData : rowData}
          columnDefs={processedColumnDefs}
          defaultColDef={defaultColDef}
          sideBar={sideBar}
          enableRangeSelection
          enableCharts
          enableFillHandle
          allowContextMenuWithControlKey
          rowGroupPanelShow="always"
          pivotPanelShow="always"
          rowSelection="multiple"
          suppressRowClickSelection
          animateRows
          tooltipShowDelay={400}
          excelStyles={EXCEL_STYLES}
          localeText={localeText}
          enableRtl={rtl}
          onGridReady={onGridReady}
          pagination={true}
          paginationPageSizeSelector={[20, 50, 100, 200, 500]}
          paginationPageSize={50}
          statusBar={{
            statusPanels: [
              { statusPanel: "agSelectedRowCountComponent", align: "center" },
              { statusPanel: "agAggregationComponent", align: "right" },
            ],
          }}
        />
      </div>
    </div>
  );
}) as <T>(p: DataGridProps<T> & { ref?: React.Ref<DataGridHandle> }) => React.ReactElement;
