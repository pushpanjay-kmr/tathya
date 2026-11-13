/** Navigation shown in the header. Routes are added as each module is built. */
export const NAV_ITEMS = [
  { label: "Markets", href: "/" },
  { label: "Scanner", href: "/scanner" },
  { label: "Screener", href: "/screener" },
] as const;

export const DISCLAIMER_SHORT =
  "Tathya is a personal research tool. Nothing here is investment advice or a recommendation to buy or sell any security.";

export const DATA_NOTE = "Data is end of day and may be incomplete or wrong.";
