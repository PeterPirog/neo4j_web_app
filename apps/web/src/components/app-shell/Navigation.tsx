"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/cn";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/people", label: "People" },
  { href: "/relations", label: "Relations" },
];

const disabledLinks = ["Permissions", "AI / GraphRAG", "ML"];

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav aria-label="Main navigation" className="flex flex-wrap items-center gap-1">
      {links.map((link) => {
        const active = pathname === link.href;
        return (
          <Link
            className={cn(
              "rounded-md px-3 py-2 text-sm font-medium transition",
              active
                ? "bg-graph-ink text-white"
                : "text-graph-ink hover:bg-stone-100",
            )}
            href={link.href}
            key={link.href}
          >
            {link.label}
          </Link>
        );
      })}

      {disabledLinks.map((label) => (
        <span
          aria-disabled="true"
          className="rounded-md px-3 py-2 text-sm font-medium text-stone-400"
          key={label}
        >
          {label}
        </span>
      ))}
    </nav>
  );
}
