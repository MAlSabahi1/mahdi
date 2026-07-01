import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState, useRef, useEffect } from "react";
import type { ColDef, ColGroupDef } from "ag-grid-community";
import { DataGrid, DataGridHandle } from "@/components/data-grid/DataGrid";
import testDataRaw from "../test_data.json";
import { Search, Eye, Edit, Trash2, User, IdCard, MapPin, ShieldCheck, ArrowLeft, Star, Building, Phone, Briefcase, Layers, MoreHorizontal } from "lucide-react";
import { SmartSearchPalette, SearchResultItem } from "@/components/data-grid/SmartSearchPalette";


export const Route = createFileRoute("/")({
  component: Index,
});

type Row = typeof testDataRaw[0];

const StatusBadge = (p: { value: string }) => {
  if (!p.value) return null;
  const val = String(p.value);

  let textColorClass = "text-slate-600 dark:text-slate-300"; // Default Normal

  if (val === "قوة عاملة فعلية" || val === "موجود" || val === "نعم") {
    textColorClass = "text-emerald-600 dark:text-emerald-400 font-semibold"; // Clear comfortable green
  } else if (val.includes("قوة عاملة غير فعلية") || val.includes("غير فعلية")) {
    textColorClass = "text-emerald-500/90 dark:text-emerald-500/80 font-medium"; // Less intense green
  } else if (val.includes("نهائيا") || val.includes("مفصول") || val.includes("فرار")) {
    textColorClass = "text-red-700 dark:text-red-500 font-bold"; // Strong Red
  } else if (val.includes("مؤقتا") || val.includes("إجازة")) {
    textColorClass = "text-red-500 dark:text-red-400 font-semibold"; // Medium Red
  } else if (val.includes("غير")) {
    textColorClass = "text-red-400 dark:text-red-300 font-medium"; // Light Red
  }

  return <span className={`text-xs ${textColorClass}`}>{val}</span>;
};

const getUniqueValues = (field: keyof Row) => {
  const set = new Set((testDataRaw as any[]).map(r => r[field]).filter(Boolean));
  return Array.from(set).sort() as string[];
};

const dropdownProps = (field: keyof Row) => ({
  cellEditor: "agRichSelectCellEditor",
  cellEditorParams: {
    values: getUniqueValues(field),
    searchType: "match",
    allowTyping: true,
    filterList: true,
    highlightMatch: true,
  },
  cellEditorPopup: true,
});

function Index() {
  const [rowData, setRowData] = useState<Row[]>(() => testDataRaw as Row[]);
  const gridRef = useRef<DataGridHandle>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate initial loading for Skeleton demonstration
  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 800);
    return () => clearTimeout(timer);
  }, []);

  const searchResults = useMemo(() => {
    if (!searchQuery) return [];
    
    const lowerQuery = searchQuery.toLowerCase();
    const filtered = rowData.filter(r => 
      Object.values(r).some(val => 
        val !== null && val !== undefined && String(val).toLowerCase().includes(lowerQuery)
      )
    );
    return filtered.slice(0, 50).map(r => ({
      id: String(r["الرقم العسكري"]),
      title: r["الأسم"],
      subtitle: r["الرتبة"] || "غير محدد",
      rawData: r
    }));
  }, [rowData, searchQuery]);

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

  const columnDefs = useMemo<(ColDef<Row> | ColGroupDef<Row>)[]>(() => [
    {
      headerName: "",
      valueGetter: "node.rowIndex + 1",
      width: 60,
      minWidth: 60,
      maxWidth: 60,
      pinned: "right",
      suppressMenu: true,
      suppressHeaderMenuButton: true,
      suppressMovable: true,
      sortable: false,
      filter: false,
      resizable: false,
    },
    {
      headerName: "البيانات الأساسية",
      children: [
        {
          headerName: "",
          width: 60,
          minWidth: 60,
          maxWidth: 60,
          checkboxSelection: true,
          headerCheckboxSelection: true,
          suppressMenu: true,
          suppressHeaderMenuButton: true,
          suppressMovable: true,
          sortable: false,
          filter: false,
          resizable: false,
        },
        {
          headerName: "الاسم",
          field: "الأسم",
          width: 220,
          rowDrag: true,
          filter: "agTextColumnFilter",
        },
        {
          headerName: "الرقم العسكري",
          field: "الرقم العسكري",
          width: 140,
          filter: "agTextColumnFilter",
        },
        {
          headerName: "الرقم الوطني",
          field: "الرقم الوطني",
          width: 150,
          filter: "agTextColumnFilter",
        },
        {
          headerName: "رقم التليفون",
          field: "رقم التليفون",
          width: 130,
          filter: "agTextColumnFilter",
        },
      ],
    },
    {
      headerName: "الرتبة والمنصب",
      children: [
        {
          headerName: "الرتبة",
          field: "الرتبة",
          width: 110,
          filter: "agSetColumnFilter",
          ...dropdownProps("الرتبة"),
        },
        {
          headerName: "الرتبة الجديدة",
          field: "الرتبة الجديدة",
          width: 130,
          filter: "agSetColumnFilter",
          ...dropdownProps("الرتبة الجديدة"),
        },
        {
          headerName: "المنصب",
          field: "المنصب",
          width: 160,
          filter: "agTextColumnFilter",
          ...dropdownProps("المنصب"),
        },
      ],
    },
    {
      headerName: "بيانات الوحدة",
      children: [
        {
          headerName: "الوحدة",
          field: "الوحدة",
          width: 120,
          filter: "agSetColumnFilter",
          ...dropdownProps("الوحدة"),
        },
        {
          headerName: "الإدارة / السرية",
          field: "الإدارة_السرية",
          width: 170,
          filter: "agSetColumnFilter",
          ...dropdownProps("الإدارة_السرية"),
        },
        {
          headerName: "القسم / فرع السرية",
          field: "القسم_فرع السرية",
          width: 170,
          filter: "agSetColumnFilter",
          ...dropdownProps("القسم_فرع السرية"),
        },
        {
          headerName: "نوع العمل",
          field: "نوع العمل",
          width: 120,
          filter: "agSetColumnFilter",
          ...dropdownProps("نوع العمل"),
        },
      ],
    },
    {
      headerName: "الحالة الوظيفية",
      children: [
        {
          headerName: "الحالة",
          field: "الحالة",
          width: 160,
          filter: "agSetColumnFilter",
          cellRenderer: StatusBadge,
          ...dropdownProps("الحالة"),
        },
        {
          headerName: "نوع الحالة",
          field: "نوع الحالة",
          width: 130,
          filter: "agSetColumnFilter",
          ...dropdownProps("نوع الحالة"),
        },
        {
          headerName: "المؤهل",
          field: "المؤهل",
          width: 120,
          filter: "agSetColumnFilter",
          ...dropdownProps("المؤهل"),
        },
      ],
    },
    {
      headerName: "المتغيرات الشهرية",
      children: [
        { headerName: "مارس 2026", field: "متغيرات مارس 2026", width: 120, filter: "agSetColumnFilter" },
        { headerName: "فبراير 2026", field: "متغيرات فبراير 2026", width: 120, filter: "agSetColumnFilter" },
        { headerName: "يناير 2026", field: "متغيرات يناير 2026", width: 120, filter: "agSetColumnFilter" },
        { headerName: "ديسمبر", field: "متغير شهر ديسمبر", width: 100, filter: "agSetColumnFilter" },
        { headerName: "نوفمبر", field: "متغير شهر نوفمبر", width: 100, filter: "agSetColumnFilter" },
        { headerName: "أكتوبر", field: "متغير شهر أكتوبر", width: 100, filter: "agSetColumnFilter" },
      ],
    },
    {
      headerName: "معلومات إضافية",
      children: [
        {
          headerName: "تاريخ الالتحاق",
          field: "تاريخ الالتحاق",
          width: 140,
          filter: "agDateColumnFilter",
        },
        {
          headerName: "ملاحظات",
          field: "ملاحظات",
          width: 250,
          filter: "agTextColumnFilter",
        },
      ],
    },
    {
      headerName: "الإجراءات",
      pinned: "left",
      width: 110,
      minWidth: 110,
      maxWidth: 110,
      editable: false,
      suppressMenu: true,
      suppressHeaderMenuButton: true,
      suppressHeaderFilterButton: true,
      suppressMovable: true,
      sortable: false,
      filter: false,
      resizable: false,
      cellRenderer: (p: any) => (
        <div className="flex items-center justify-center gap-1.5 h-full">
          <button className="p-1.5 text-muted-foreground hover:text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-md transition-colors" title="حذف">
            <Trash2 className="w-4 h-4" />
          </button>
          <button className="p-1.5 text-muted-foreground hover:text-blue-600 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-md transition-colors" title="تعديل">
            <Edit className="w-4 h-4" />
          </button>
          <button className="p-1.5 text-muted-foreground hover:text-emerald-600 hover:bg-emerald-100 dark:hover:bg-emerald-900/30 rounded-md transition-colors" title="عرض التفاصيل">
            <Eye className="w-4 h-4" />
          </button>
        </div>
      ),
    },
  ], []);

  return (
    <div className="flex h-screen w-full flex-col">
      <DataGrid 
        ref={gridRef}
        rowData={rowData} 
        columnDefs={columnDefs} 
        title="سجل الموظفين" 
        gridId="personnel-registry"
        isLoading={isLoading}
        searchTrigger={
          <button
            onClick={() => setSearchOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground bg-muted/50 hover:bg-muted border border-border rounded-md transition-colors w-64"
          >
            <Search className="w-4 h-4" />
            <span className="flex-1 text-right">البحث الشامل...</span>
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
        onSelectResult={(item: SearchResultItem) => {
          setSearchOpen(false);
          gridRef.current?.selectRowById(item.id, "الرقم العسكري");
        }}
        renderPreview={(item: SearchResultItem) => (
          <div className="flex flex-col h-full w-full bg-background pt-8 pb-6 px-8">
            <div className="flex flex-col items-center text-center">
              {item.rawData["الصورة"] ? (
                <img src={item.rawData["الصورة"]} alt="صورة الموظف" className="w-20 h-20 rounded-full object-cover mb-4 ring-2 ring-border/50 shadow-sm" />
              ) : (
                <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-4 ring-2 ring-border/50 shadow-sm">
                  <User className="w-8 h-8 text-muted-foreground/50" />
                </div>
              )}
              <h2 className="text-[17px] font-bold text-foreground">{item.title}</h2>
              <p className="text-[13px] text-muted-foreground mt-0.5">{item.subtitle}</p>
            </div>
            
            <div className="w-full pt-6 border-t border-border mt-4">
              <div className="grid grid-cols-2 gap-x-8 gap-y-6">
                
                <div className="flex items-center gap-3">
                  <IdCard className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">الرقم</span>
                  <span className="text-[13px] text-muted-foreground truncate">{item.rawData["الرقم العسكري"]}</span>
                </div>
                
                <div className="flex items-center gap-3">
                  <Briefcase className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">المنصب</span>
                  <span className="text-[13px] text-muted-foreground truncate">{item.rawData["المنصب"] || "-"}</span>
                </div>

                <div className="flex items-center gap-3">
                  <Building className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">الإدارة</span>
                  <span className="text-[13px] text-muted-foreground truncate">{item.rawData["الإدارة / السرية"] || "-"}</span>
                </div>

                <div className="flex items-center gap-3">
                  <Layers className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">القسم</span>
                  <span className="text-[13px] text-muted-foreground truncate">{item.rawData["القسم / فرع"] || "-"}</span>
                </div>

                <div className="flex items-center gap-3">
                  <Phone className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">الهاتف</span>
                  <span className="text-[13px] text-muted-foreground truncate">{item.rawData["رقم التليفون"] || "غير متوفر"}</span>
                </div>

                <div className="flex items-center gap-3">
                  <ShieldCheck className="w-[18px] h-[18px] text-primary" />
                  <span className="text-[13px] font-semibold text-foreground w-[60px]">الحالة</span>
                  <span className="text-[13px] text-blue-600 hover:underline cursor-pointer truncate">{item.rawData["الحالة"]}</span>
                </div>

              </div>
            </div>

            <div className="mt-auto pt-6 flex justify-center">
              <button 
                onClick={() => {
                  setSearchOpen(false);
                  gridRef.current?.selectRowById(item.id, "الرقم العسكري");
                }}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-colors shadow-sm"
              >
                تحديد في الجدول
              </button>
            </div>
          </div>
        )}
      />
    </div>
  );
}
