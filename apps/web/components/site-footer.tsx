import Link from "next/link";
import { DATA_NOTE, DISCLAIMER_SHORT } from "@/lib/site";

/** Persistent disclaimer. Shown on every page by the root layout. */
export function SiteFooter() {
  return (
    <footer className="border-t border-border px-4 py-5 text-xs leading-4 text-muted sm:px-8">
      <div className="flex flex-wrap justify-between gap-x-6 gap-y-2">
        <span>
          {DISCLAIMER_SHORT}{" "}
          <Link href="/disclaimer" className="font-semibold text-accent">
            Full disclaimer
          </Link>
        </span>
        <span>{DATA_NOTE}</span>
      </div>
    </footer>
  );
}
