# nanofdo-public-benchmarks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![API](https://img.shields.io/badge/API-live-green.svg)](https://github.com/JoManix-OSS/nanofdo-public-benchmarks#live-endpoints)
[![Results](https://img.shields.io/badge/Results-2026--07--06-blue.svg)](RESULTS.md)

Public, reproducible parsing benchmarks for [NanoFDO](https://nanofdo.com).

This repository contains independent, server-side measurements of JSON parsing latency. Anyone can register for a free, benchmark-only key and reproduce the results in minutes. Hosted access is for evaluation and reproducibility, not production processing or load testing.

## Latest results snapshot

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 842 ns  | 2130 ns    | **2.58x** |
| p95    | 860 ns  | 2156 ns    | **2.55x** |
| p99    | 870 ns  | 2171 ns    | **2.54x** |
| mean   | 849 ns  | 2138 ns    | **2.57x** |

See [RESULTS.md](RESULTS.md) for the full dataset, raw runs, and methodology notes.

## About our numbers

NanoFDO publishes performance figures from several measurement contexts. They differ intentionally and each one answers a different question.

- **Public benchmark (this repository):** measures full server-side pipeline latency for a single JSON payload over 100,000 iterations. It is our conservative, independently reproducible reference point.
- **Live benchmark and Labs simulator:** measure steady-state throughput on repetitive traffic streams. These figures reflect the engine's behavior when the same structure is seen repeatedly.
- **Your actual gain** depends on the repetitiveness of your traffic: the more your payloads share a stable JSON structure, the closer you get to the upper range.
- **Independent verification:** download the local binaries and measure on your own hardware.

## Methodology & hosted allowance

**Fixed method.** Each hosted run uses 100,000 measured iterations and 1,000 warmup iterations. Custom values are rejected so public results remain comparable.

**Free hosted allowance.** A benchmark-only key provides **10 runs per day** and **50 runs per calendar month**, with 5 attempts per 15 minutes and 1 concurrent run per key. The shared hosted service accepts at most **500 reserved runs per day** across all public keys, with 2 concurrent runs globally and a 30-second execution limit.

**Sovereign metric.** The latency numbers reported here (`server_processing_ns`) are measured **server-side**, independently of the network. The total HTTP call time (RTT) you measure locally includes network and intermediary processing — that is **not** the NanoFDO processing latency.

See the full [methodology](METHODOLOGY.md). Intensive research requires prior approval or an approved local option.

## Live endpoints

- **Register** — `POST https://api.nanofdo.com/api/v1/register`
  - Returns a free key scoped exclusively to the public benchmark.
- **Benchmark** — `POST https://api.nanofdo.com/api/v1/parse`
  - Returns server-side parsing latency distributions (p50/p95/p99/p999) and a matching baseline.

## Quick start

```bash
pip install requests
python benchmark.py your-email@example.com 5
```

Results are saved to `results.json`. The access key is reused from `NANOFDO_BENCHMARK_KEY` or the ignored `.nanofdo-benchmark-key` file and is never written to the results file. One invocation accepts 1–5 runs to respect the burst limit.

To use a replacement key, set `NANOFDO_BENCHMARK_KEY`. To register again after an authorised revocation, delete `.nanofdo-benchmark-key` and rerun with your email.

Run the offline client tests with:

```bash
python -m unittest test_benchmark.py
```

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

## Usage, privacy, and security

By registering or using a hosted benchmark key, you agree to:

- [Terms of Use](TERMS.md)
- [Acceptable Use Policy](ACCEPTABLE_USE.md)
- [Privacy Notice](PRIVACY.md)
- [Benchmark Methodology](METHODOLOGY.md)

Use only synthetic, non-confidential payloads. Do not publish an access key or include sensitive information in a public issue. Private security and privacy reports may be sent to `support@nanofdo.com`.

## License

The repository source is MIT licensed. The MIT license does not grant unlimited access to the hosted API; hosted access is governed by the documents above.
