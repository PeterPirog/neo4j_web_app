import { SelectHTMLAttributes } from "react";

import { cn } from "@/lib/cn";

export function Select({
  className,
  ...props
}: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={cn(
        "h-10 w-full rounded-md border border-graph-line bg-white px-3 text-sm outline-none transition focus:border-graph-accent focus:ring-2 focus:ring-emerald-100",
        className,
      )}
      {...props}
    />
  );
}
