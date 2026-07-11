import { InputHTMLAttributes } from "react";

import { cn } from "@/lib/cn";

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-md border border-graph-line bg-white px-3 text-sm outline-none transition focus:border-graph-accent focus:ring-2 focus:ring-emerald-100",
        className,
      )}
      {...props}
    />
  );
}
