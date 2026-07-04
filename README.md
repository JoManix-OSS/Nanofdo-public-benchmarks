# nanofdo-public-benchmarks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![API](https://img.shields.io/badge/API-live-green.svg)](https://api.nanofdo.com/api/v1/parse)

Public, reproducible parsing benchmarks for [NanoFDO](https://nanofdo.com).

This repository contains independent, server-side measurements of JSON parsing latency. Anyone can register for a free Developer Edge key and reproduce the results in minutes.

## Latest results snapshot

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 628 ns  | 2194 ns    | **3.49x** |
| p95    | 635 ns  | 2233 ns    | **3.51x** |
| p99    | 647 ns  | 2254 ns    | **3.48x** |
| mean   | 632 ns  | 2204 ns    | **3.49x** |

See [RESULTS.md](RESULTS.md) for the full dataset, raw runs, and methodology notes.

## Live endpoints

- **Register** — `POST https://api.nanofdo.com/api/v1/register`
  - Returns a free Developer Edge license key (1M requests/month).
- **Benchmark** — `POST https://api.nanofdo.com/api/v1/parse`
  - Returns server-side parsing latency distributions (p50/p95/p99/p999) for NanoFDO and a `serde_json` baseline.

## Quick start

```bash
pip install requests
python benchmark.py your-email@example.com 5
```

Results are saved to `results.json`.

## How to reproduce manually

```bash
# 1. Register
curl -X POST https://api.nanofdo.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your-email@example.com"}'

# 2. Parse (use the returned license key)
curl -X POST https://api.nanofdo.com/api/v1/parse \
  -H "Content-Type: application/json" \
  -H "x-nanofdo-license-key: <LICENSE_KEY>" \
  -d '{"payload":"{\"user\":{\"role\":\"admin\",\"amount\":123}}"}'
```

## What is measured

- **Server-side latency only.** The API runs 100,000 iterations on the same JSON payload inside a dedicated blocking task. Network round-trip time is intentionally excluded from the reported distributions.
- **Real `serde_json` baseline.** Every run parses the same payload with `serde_json` on the same CPU, same thread, same server.
- **Distributions, not averages.** We report p50, p95, p99 and p999 so outliers are visible, not hidden behind a mean.

## Server

- **OVH KS-A**
- **Intel Xeon E-2274G @ 4.0GHz**
- **Roubaix, France**

## Interpreting the results

- **p50 / p95 / p99** are the primary metrics. They show stable speedups around **2.9–3.0x** on this payload.
- **p999** is volatile (5–12x) and depends on rare system interruptions during the 100,000-iteration run. It is reported for completeness but should not be used as the headline figure.
- Transient load on the server can double absolute latencies while keeping the speedup ratio consistent. Repeat runs are recommended.

## License

MIT
