import type { Metadata } from "next";
import { EmptyState } from "@/components/empty-state";

export const metadata: Metadata = { title: "Search" };

export default function SearchPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-[28px] leading-[34px] font-semibold tracking-tight">
        Search
      </h1>
      <EmptyState title="No companies loaded yet">
        Company search works once the company list has been loaded into the
        database.
      </EmptyState>
    </div>
  );
}
