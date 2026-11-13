import type { Metadata } from "next";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
// Fonts are bundled from npm packages, so builds need no network access.
import "@fontsource-variable/inter";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "@fontsource/noto-sans-devanagari/devanagari-500.css";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Tathya", template: "%s | Tathya" },
  description:
    "A personal research and analysis workbench for Indian stocks. Not investment advice.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="flex min-h-full flex-col font-sans">
        <SiteHeader />
        <main className="mx-auto w-full max-w-[1280px] flex-1 px-4 py-8 sm:px-8">
          {children}
        </main>
        <SiteFooter />
      </body>
    </html>
  );
}
