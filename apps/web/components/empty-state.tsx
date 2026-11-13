/** One sentence saying why there is nothing to show, and what to do next. */
export function EmptyState({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-card border border-border bg-surface p-6">
      <h2 className="text-base leading-6 font-semibold">{title}</h2>
      <p className="mt-1 max-w-prose text-muted">{children}</p>
    </div>
  );
}
