import Link from "next/link";
import { NAV_ITEMS } from "@/lib/site";

/**
 * Top bar: wordmark, search and navigation.
 * Search is a plain form for now. It will go to /search once company data exists.
 */
export function SiteHeader() {
  return (
    <header className="border-b border-border bg-surface">
      <div className="flex flex-wrap items-center gap-x-6 gap-y-3 px-4 py-3.5 sm:px-8">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="text-[22px] leading-7 font-bold tracking-tight">
            tathya
          </span>
          <span
            lang="hi"
            className="font-devanagari text-sm font-medium text-accent"
          >
            तथ्य
          </span>
        </Link>

        <form
          role="search"
          action="/search"
          className="flex min-h-11 max-w-[520px] flex-[1_1_320px] items-center gap-2.5 rounded-control border border-border bg-bg px-3.5"
        >
          <label htmlFor="site-search" className="sr-only">
            Search companies
          </label>
          <input
            id="site-search"
            name="q"
            type="search"
            placeholder="Search companies by name or symbol"
            className="min-w-0 flex-1 bg-transparent outline-none placeholder:text-muted"
          />
        </form>

        <nav aria-label="Main" className="ml-auto flex flex-wrap gap-1">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex min-h-11 items-center rounded-control px-3.5 font-medium hover:bg-accent-soft hover:text-accent"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
