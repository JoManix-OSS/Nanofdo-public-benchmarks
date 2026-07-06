# nanofdo-public-benchmarks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![API](https://img.shields.io/badge/API-live-green.svg)](https://github.com/JoManix-OSS/nanofdo-public-benchmarks#live-endpoints)
[![Results](https://img.shields.io/badge/Results-2026--07--06-blue.svg)](RESULTS.md)

Public, reproducible parsing benchmarks for [NanoFDO](https://nanofdo.com).

This repository contains independent, server-side measurements of JSON parsing latency. Anyone can register for a free Developer Edge key and reproduce the results in minutes.

## Latest results snapshot

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 842 ns  | 2130 ns    | **2.58x** |
| p95    | 860 ns  | 2156 ns    | **2.55x** |
| p99    | 870 ns  | 2171 ns    | **2.54x** |
| mean   | 849 ns  | 2138 ns    | **2.57x** |

See [RESULTS.md](RESULTS.md) for the full dataset, raw runs, and methodology notes.

## Methodology & quota

**Free quota.** Registration gives **1,000,000 API requests per month**. One benchmark run consumes **1 API request**, even though the server executes 100,000 iterations to produce the latency distribution. Normal usage (a few dozen runs) represents less than 0.001% of the quota.

**Sovereign metric.** The latency numbers reported here (`server_processing_ns`) are measured **server-side**, independently of the network. The total HTTP call time (RTT) you measure locally includes the network, nginx, and Cloudflare — that is **not** the NanoFDO parsing latency.

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

- **p50 / p95 / p99** are the primary metrics. Recent runs show speedups in the **2.5–3.0x** range on this payload, depending on CPU frequency state and transient server load.
- **p999** is volatile (4–5x on this payload) and depends on rare system interruptions during the 100,000-iteration run. It is reported for completeness but should not be used as the headline figure.
- Transient load on the server can double absolute latencies while keeping the speedup ratio consistent. Repeat runs are recommended.

## About NanoFDO

NanoFDO is a high-performance JSON processing engine with an integrated L7 security layer. Independently measured product metrics:

- **1,764 OWASP vectors** embedded, **8/10 OWASP Top 10 2021** coverage
- **~107 ns/scan** security overhead
- **+0 ns** overhead on legitimate requests
- Zero-allocation hot path, sub-microsecond parsing

Learn more at [nanofdo.com](https://nanofdo.com).

## License

MIT
