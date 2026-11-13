"""The AI layer: summaries, guidance extraction, filing classification, Ask Tathya.

See docs/05-architecture.md, "AI layer". Deferred until there are filings
and concall transcripts to run against (phase 5 in docs/08-roadmap.md).
Guardrails when this is implemented: grounded in retrieved text only,
always cite, never buy/sell language, cached by (company, question hash,
document version), spend logged per job.
"""
