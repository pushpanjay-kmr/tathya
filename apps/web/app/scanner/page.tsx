import type { Metadata } from "next";
import { EmptyState } from "@/components/empty-state";

export const metadata: Metadata = { title: "Scanner" };

export default function ScannerPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-[28px] leading-[34px] font-semibold tracking-tight">
        Scanner
      </h1>
      <EmptyState title="Not built yet">
        Ready-made scans, re-run every night, arrive in Phase 3 of the roadmap.
      </EmptyState>
    </div>
  );
}
