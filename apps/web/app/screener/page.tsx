import type { Metadata } from "next";
import { EmptyState } from "@/components/empty-state";

export const metadata: Metadata = { title: "Screener" };

export default function ScreenerPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-[28px] leading-[34px] font-semibold tracking-tight">
        Screener
      </h1>
      <EmptyState title="Not built yet">
        Filtering the market with fields and formulas arrives in Phase 3 of the
        roadmap.
      </EmptyState>
    </div>
  );
}
