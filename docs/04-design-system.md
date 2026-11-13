# 04. Design system

Status: **draft**. Two visual directions are proposed below. One will be chosen after mockups of the home page in both.

## Brand

| | |
|---|---|
| Name | Tathya (तथ्य, "fact") |
| Line | Facts before conviction |
| Personality | Calm, exact, unhurried. A well-kept ledger, not a ticker tape |
| Voice | Plain and specific. States what the data shows and where it came from. Never urges action |

### Wordmark

Lower-case `tathya` in the UI typeface at semibold weight, with the Devanagari `तथ्य` available as a secondary mark for the about page and favicon exploration. Final logo work happens with the mockups.

### Writing rules

- Say "passed the scan", not "buy signal".
- Say "as of 12 Nov 2026", not "today" or "live".
- Numbers use the Indian system: lakh and crore, with grouping `1,23,45,678`. Market cap in ₹ Cr or ₹ L Cr.
- Percentages carry a sign when they are changes: `+1.2%`, `-0.6%`.
- Use an en dash only for missing values in tables, shown as `–`.

## Direction A: "Ledger" (light-first)

A research-report feel. Warm paper background, ink text, one deep accent. Reads well for long sessions and in print.

| Token | Value | Use |
|---|---|---|
| `bg` | `#FAF8F4` | Page |
| `surface` | `#FFFFFF` | Cards, tables |
| `border` | `#E6E1D8` | Dividers |
| `text` | `#1C1B19` | Body |
| `text-muted` | `#6B665E` | Labels, captions |
| `accent` | `#1F4E5F` | Links, active states, brand |
| `accent-soft` | `#E3EEF1` | Selected chips, highlights |

## Direction B: "Terminal" (dark-first)

A dense workstation feel. Near-black background, cool grey text, one bright accent. Best for scanning large tables.

| Token | Value | Use |
|---|---|---|
| `bg` | `#0E1116` | Page |
| `surface` | `#161B22` | Cards, tables |
| `border` | `#262D38` | Dividers |
| `text` | `#E6EAF0` | Body |
| `text-muted` | `#8B95A5` | Labels, captions |
| `accent` | `#F2B84B` | Links, active states, brand |
| `accent-soft` | `#3A2F17` | Selected chips, highlights |

Whichever direction wins, the other becomes the alternate theme, so both light and dark ship.

## Semantic colours (both directions)

| Token | Light | Dark | Use |
|---|---|---|---|
| `up` | `#0B8A4A` | `#35C27B` | Positive change |
| `down` | `#C93A3A` | `#F06A6A` | Negative change |
| `flat` | `#6B665E` | `#8B95A5` | No change |
| `warn` | `#B7791F` | `#E0A840` | Caution, stale data |
| `danger` | `#9B1C1C` | `#F28B82` | Red flags |
| `info` | `#1F4E5F` | `#6FB6CC` | Notes, derived-data markers |

Rules:

- Colour is never the only signal. Changes always carry a sign, and red-flag items carry an icon and a label.
- All text and background pairs meet WCAG AA contrast (4.5:1 for body text).
- Heat scales for sector tiles use 5 steps each side of neutral, capped at plus or minus 3% for the 1D view.

## Typography

| Role | Typeface | Notes |
|---|---|---|
| Interface and body | Inter | Tabular numerals switched on everywhere |
| Numbers in dense tables | Inter with `tnum`, or IBM Plex Mono for code-like values | Right-aligned |
| Formula input | IBM Plex Mono | |
| Devanagari | Noto Sans Devanagari | Wordmark and any Hindi text |

| Token | Size / line height | Use |
|---|---|---|
| `display` | 28 / 34, semibold | Page titles |
| `title` | 20 / 28, semibold | Section headings |
| `subtitle` | 16 / 24, medium | Card headings |
| `body` | 14 / 20 | Default |
| `table` | 13 / 18 | Table cells |
| `caption` | 12 / 16 | Labels, footnotes |

## Spacing, radius, elevation

- Spacing scale: 4, 8, 12, 16, 24, 32, 48.
- Radius: 6 px for controls, 10 px for cards.
- Elevation: borders rather than shadows. One soft shadow level for popovers only.
- Page max width 1440 px, 12-column grid, 24 px gutters.
- Table row height: 36 px default, 28 px in compact mode.

## Components

| Component | Notes |
|---|---|
| Index tile | Name, level, change, sparkline. Whole tile is the click target |
| Stat | Label over value, optional delta |
| Chip | Filter and scan chips. Shows count. Selected state uses `accent-soft` |
| Segmented control | Period switch (1D to 1Y) |
| Data table | Sticky header, pinned company column, sortable, right-aligned numbers, compact mode |
| Company cell | Symbol in medium weight, full name muted beneath |
| Delta | Signed, coloured, with an arrow glyph |
| Breadth bar | Three-segment bar: up, flat, down |
| Score badge | Number plus grade, with a 5-bar pillar strip |
| Verdict tag | Small label for rule outcomes. Always paired with a "how this is computed" link |
| Derived-data marker | A small `info` icon on any computed or AI-generated value |
| Source link | Document name and date, opens the original filing |
| Formula input | Monospace, autocomplete for field names, inline error position |
| Empty and error states | Illustration-free: one sentence and one action |
| Disclaimer bar | Persistent footer line |

## Charts

- Price: candles with volume below, 50-day and 200-day moving averages, crosshair with date and OHLC.
- Sparklines: no axes, coloured by net change for the period.
- Bar and scatter: thin gridlines, direct labels in preference to legends, at most 6 series colours.
- Every chart states its "as of" date.

## Accessibility

- Full keyboard navigation. `/` focuses search, `g` then a letter jumps between sections.
- Visible focus rings using `accent`.
- Tables expose proper header associations for screen readers.
- Motion is limited to 150 ms fades and respects `prefers-reduced-motion`.

## Next steps

1. Mock up the home page in both directions.
2. Choose one; record it in the [decision log](10-decisions.md).
3. Mock up the stock page, scanner and screener in the chosen direction.
4. Export tokens to the Tailwind config when the scaffold is created.
