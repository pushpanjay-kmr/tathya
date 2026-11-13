# Tathya web app

The Next.js application: every page you see in the browser.

## Run it

```
npm install
npm run dev
```

Then open http://localhost:3000.

## Where things are

| Path | What it holds |
|---|---|
| `app/` | Pages. Each folder is a URL: `app/scanner/page.tsx` is `/scanner` |
| `app/layout.tsx` | The frame around every page: header, footer, fonts |
| `app/globals.css` | Design tokens (colours, fonts, radii) for the Ledger and Terminal themes |
| `components/` | Reusable pieces of UI |
| `lib/` | Shared constants and helpers |

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Start the development server with live reload |
| `npm run build` | Build the production version and type-check |
| `npm run lint` | Check code style |
