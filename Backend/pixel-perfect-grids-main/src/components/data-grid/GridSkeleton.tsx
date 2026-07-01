import React from "react";
import { Skeleton } from "@/components/ui/skeleton";

export function GridSkeleton({ rows = 10 }: { rows?: number }) {
  return (
    <div className="w-full h-full bg-background flex flex-col overflow-hidden">
      {/* Rows Skeleton Only - AG Grid handles the real header */}
      <div className="flex flex-col flex-1 gap-0">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="flex items-center gap-4 p-3 border-b border-border/50">
            <Skeleton className="h-5 w-12 rounded-sm" />
            <Skeleton className="h-5 w-32 rounded-sm" />
            <Skeleton className="h-5 w-40 rounded-sm" />
            <Skeleton className="h-5 w-24 rounded-sm" />
            <Skeleton className="h-5 w-48 rounded-sm" />
            <div className="ml-auto flex gap-2">
              <Skeleton className="h-6 w-16 rounded-full" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
