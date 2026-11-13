-- 0001_init: reference data and daily market data.
-- Schema reference: docs/06-data-model.md

-- Sectors and industries --------------------------------------------------

CREATE TABLE sector (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name          text NOT NULL UNIQUE,
    macro_sector  text NOT NULL
);

CREATE TABLE industry (
    id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name       text NOT NULL UNIQUE,
    sector_id  bigint NOT NULL REFERENCES sector (id)
);

-- Companies ---------------------------------------------------------------

CREATE TABLE company (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isin          text NOT NULL UNIQUE,
    nse_symbol    text UNIQUE,
    bse_code      text UNIQUE,
    name          text NOT NULL,
    industry_id   bigint REFERENCES industry (id),
    listing_date  date,
    status        text NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'suspended', 'delisted')),
    created_at    timestamptz NOT NULL DEFAULT now(),
    CHECK (nse_symbol IS NOT NULL OR bse_code IS NOT NULL)
);

CREATE INDEX company_name_idx ON company (lower(name));

-- Indices -----------------------------------------------------------------

CREATE TABLE market_index (
    id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code  text NOT NULL UNIQUE,
    name  text NOT NULL,
    kind  text NOT NULL DEFAULT 'broad'
          CHECK (kind IN ('broad', 'sector', 'volatility'))
);

CREATE TABLE index_daily (
    index_id  bigint NOT NULL REFERENCES market_index (id),
    date      date NOT NULL,
    open      numeric(14, 2),
    high      numeric(14, 2),
    low       numeric(14, 2),
    close     numeric(14, 2) NOT NULL,
    PRIMARY KEY (index_id, date)
);

-- Daily prices ------------------------------------------------------------

CREATE TABLE price_daily (
    company_id    bigint NOT NULL REFERENCES company (id),
    date          date NOT NULL,
    open          numeric(14, 2) NOT NULL,
    high          numeric(14, 2) NOT NULL,
    low           numeric(14, 2) NOT NULL,
    close         numeric(14, 2) NOT NULL,
    adj_close     numeric(14, 4),
    volume        bigint NOT NULL DEFAULT 0,
    value_traded  numeric(20, 2),
    delivery_pct  numeric(6, 2),
    source        text NOT NULL,
    PRIMARY KEY (company_id, date),
    CHECK (high >= low)
);

CREATE INDEX price_daily_date_idx ON price_daily (date);

CREATE TABLE corporate_action (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id  bigint NOT NULL REFERENCES company (id),
    ex_date     date NOT NULL,
    type        text NOT NULL
                CHECK (type IN ('split', 'bonus', 'dividend', 'rights')),
    ratio       numeric(12, 6),
    amount      numeric(14, 4),
    UNIQUE (company_id, ex_date, type)
);

-- Pipeline bookkeeping ----------------------------------------------------

CREATE TABLE pipeline_run (
    id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    as_of_date   date NOT NULL,
    started_at   timestamptz NOT NULL DEFAULT now(),
    finished_at  timestamptz,
    status       text NOT NULL DEFAULT 'running'
                 CHECK (status IN ('running', 'succeeded', 'failed')),
    step_status  jsonb NOT NULL DEFAULT '{}'::jsonb,
    notes        text
);

CREATE TABLE provider_fetch (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id      bigint REFERENCES pipeline_run (id),
    provider    text NOT NULL,
    dataset     text NOT NULL,
    as_of_date  date NOT NULL,
    row_count   integer,
    status      text NOT NULL CHECK (status IN ('ok', 'failed', 'skipped')),
    error       text,
    fetched_at  timestamptz NOT NULL DEFAULT now()
);
