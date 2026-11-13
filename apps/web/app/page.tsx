import { EmptyState } from "@/components/empty-state";

export default function HomePage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-[28px] leading-[34px] font-semibold tracking-tight">
          Market overview
        </h1>
        <p className="mt-1 text-muted">
          Indices, sector moves and market breadth will appear here.
        </p>
      </div>
      <EmptyState title="No market data yet">
        The data pipeline has not been run. Once end-of-day prices are loaded
        into the database, this page will show the latest trading day.
      </EmptyState>
    </div>
  );
}
