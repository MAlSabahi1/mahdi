import React, { useState, useMemo } from "react";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { 
  Settings, 
  Eye, 
  EyeOff, 
  Lock, 
  Unlock, 
  Download, 
  X,
  Search,
  Pin,
  ArrowRightToLine,
  ArrowLeftToLine
} from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export type UserRole = "admin" | "hr" | "viewer";

export interface ColumnConfig {
  field: string;
  headerName: string;
  isVisible: boolean;
  isExportable: boolean;
  isEditable: boolean;
  pinned?: "left" | "right" | null;
  requiredRoles?: UserRole[];
}

interface GridSettingsDrawerProps {
  configs: ColumnConfig[];
  onConfigChange: (field: string, key: keyof ColumnConfig, value: any) => void;
  currentUserRole: UserRole;
  onRoleChange: (role: UserRole) => void;
}

export function GridSettingsDrawer({
  configs,
  onConfigChange,
  currentUserRole,
  onRoleChange,
}: GridSettingsDrawerProps) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredConfigs = useMemo(() => {
    if (!searchQuery) return configs;
    return configs.filter(col => 
      col.headerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      col.field.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [configs, searchQuery]);

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2 h-8 border-primary/30 bg-primary/5 hover:bg-primary/10 transition-all duration-300 group">
          <Settings className="w-4 h-4 text-primary group-hover:rotate-90 transition-transform duration-500" />
          <span className="hidden sm:inline font-bold text-primary">لوحة التحكم</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[400px] sm:w-[600px] flex flex-col p-0">
        <div className="p-6 pb-4 border-b bg-muted/20">
          <SheetHeader>
            <SheetTitle className="text-2xl font-bold flex items-center gap-3 text-primary">
              <Settings className="w-6 h-6" />
              لوحة تحكم الجدول
            </SheetTitle>
            <SheetDescription className="text-sm mt-1.5">
              إدارة متقدمة لخصائص العرض، التصدير، والصلاحيات مع دعم التثبيت.
            </SheetDescription>
          </SheetHeader>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Role Simulator */}
          <div className="p-4 bg-card rounded-xl border shadow-sm flex flex-col gap-3">
            <div className="flex items-center gap-2 text-sm font-bold text-foreground">
              <Lock className="w-4 h-4 text-primary" />
              محاكي الصلاحيات (Role Simulator)
            </div>
            <Select value={currentUserRole} onValueChange={(val) => onRoleChange(val as UserRole)}>
              <SelectTrigger className="w-full bg-background">
                <SelectValue placeholder="اختر الصلاحية" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="admin">مدير النظام الأعلى (Admin)</SelectItem>
                <SelectItem value="hr">إدارة الموارد البشرية (HR)</SelectItem>
                <SelectItem value="viewer">مستخدم للقراءة فقط (Viewer)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-4">
            <div className="relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input 
                placeholder="ابحث عن عمود لتعديله..." 
                className="pl-3 pr-9 h-10 bg-background"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            <Tabs defaultValue="all" className="w-full">
              <TabsList className="grid w-full grid-cols-3 h-10">
                <TabsTrigger value="all" className="font-semibold">الأساسية</TabsTrigger>
                <TabsTrigger value="security" className="font-semibold">الصلاحيات</TabsTrigger>
                <TabsTrigger value="export" className="font-semibold">التصدير والتثبيت</TabsTrigger>
              </TabsList>
              
              <div className="mt-6 space-y-3">
                {filteredConfigs.map((col) => (
                  <div key={col.field} className="flex flex-col gap-3 p-4 border rounded-xl bg-card shadow-sm hover:border-primary/40 hover:shadow-md transition-all duration-200">
                    <div className="flex items-center justify-between">
                      <div className="font-bold text-primary text-[15px]">{col.headerName}</div>
                      <div className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-md font-mono">{col.field}</div>
                    </div>
                    
                    <TabsContent value="all" className="mt-0 outline-none">
                      <div className="flex items-center justify-between pt-2 border-t border-border/50">
                        <Label className="text-sm font-semibold flex items-center gap-2">
                          ظهور في الجدول
                        </Label>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className={`w-9 h-9 rounded-full transition-all duration-300 ${col.isVisible ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/20 hover:scale-110' : 'bg-muted/50 text-muted-foreground hover:bg-muted opacity-70 grayscale hover:grayscale-0'}`}
                          onClick={() => onConfigChange(col.field, "isVisible", !col.isVisible)}
                          title={col.isVisible ? "ظاهر" : "مخفي"}
                        >
                          {col.isVisible ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
                        </Button>
                      </div>
                    </TabsContent>

                    <TabsContent value="security" className="mt-0 outline-none">
                      <div className="flex items-center justify-between pt-2 border-t border-border/50">
                        <div className="flex flex-col">
                          <Label className="text-sm font-semibold flex items-center gap-2">
                            صلاحية التعديل
                          </Label>
                          <span className="text-[11px] text-muted-foreground mt-1">تتأثر بصلاحيات النظام</span>
                        </div>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className={`w-9 h-9 rounded-full transition-all duration-300 ${col.isEditable ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/20 hover:scale-110' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 hover:bg-rose-500/20 hover:scale-110'}`}
                          onClick={() => onConfigChange(col.field, "isEditable", !col.isEditable)}
                          disabled={currentUserRole !== "admin" && currentUserRole !== "hr"}
                          title={col.isEditable ? "مفتوح للتعديل" : "مقفول"}
                        >
                          {col.isEditable ? <Unlock className="w-5 h-5" /> : <Lock className="w-5 h-5" />}
                        </Button>
                      </div>
                    </TabsContent>

                    <TabsContent value="export" className="mt-0 outline-none">
                      <div className="flex flex-col gap-4 pt-2 border-t border-border/50">
                        <div className="flex items-center justify-between">
                          <Label className="text-sm font-semibold flex items-center gap-2">
                            تضمين في ملف Excel
                          </Label>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className={`w-9 h-9 rounded-full transition-all duration-300 ${col.isExportable ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 hover:bg-blue-500/20 hover:scale-110' : 'bg-muted/50 text-muted-foreground hover:bg-muted opacity-70 grayscale hover:grayscale-0'}`}
                            onClick={() => onConfigChange(col.field, "isExportable", !col.isExportable)}
                            title={col.isExportable ? "يُصدّر" : "مستثنى"}
                          >
                            {col.isExportable ? <Download className="w-5 h-5" /> : <X className="w-5 h-5" />}
                          </Button>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <Label className="text-sm font-semibold flex items-center gap-2">
                            <Pin className="w-4 h-4 text-indigo-500" />
                            تثبيت العمود (Pinning)
                          </Label>
                          <div className="flex items-center gap-1 bg-muted p-1 rounded-lg">
                            <Button 
                              variant={col.pinned === "right" ? "default" : "ghost"} 
                              size="sm" 
                              className="h-7 px-2 text-xs"
                              onClick={() => onConfigChange(col.field, "pinned", col.pinned === "right" ? null : "right")}
                            >
                              <ArrowRightToLine className="w-3 h-3 mr-1" /> يمين
                            </Button>
                            <Button 
                              variant={col.pinned === "left" ? "default" : "ghost"} 
                              size="sm" 
                              className="h-7 px-2 text-xs"
                              onClick={() => onConfigChange(col.field, "pinned", col.pinned === "left" ? null : "left")}
                            >
                              <ArrowLeftToLine className="w-3 h-3 mr-1" /> يسار
                            </Button>
                          </div>
                        </div>
                      </div>
                    </TabsContent>
                  </div>
                ))}
                
                {filteredConfigs.length === 0 && (
                  <div className="text-center py-10 text-muted-foreground">
                    <Search className="w-10 h-10 mx-auto mb-3 opacity-20" />
                    <p>لم يتم العثور على أي عمود مطابق للبحث</p>
                  </div>
                )}
              </div>
            </Tabs>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
