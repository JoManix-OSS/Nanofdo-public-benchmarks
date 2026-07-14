# NanoFDO Public Benchmark Results

## 2026-07-06 run

After fixing the CPU governor to `performance` on the OVH server, a fresh
5-run benchmark produced the following summary:

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 842 ns  | 2130 ns    | 2.58x   |
| p95    | 860 ns  | 2156 ns    | 2.55x   |
| p99    | 870 ns  | 2171 ns    | 2.54x   |
| p999   | 2269 ns | 3603 ns    | 1.60x   |
| mean   | 849 ns  | 2138 ns    | 2.57x   |

Raw data is available in `results.json`.

## About these numbers

NanoFDO publishes performance figures from several measurement contexts. They differ intentionally and each one answers a different question.

- **Public benchmark (this repository):** measures full server-side pipeline latency for a single JSON payload over 100,000 iterations. It is our conservative, independently reproducible reference point.
- **Live benchmark and Labs simulator:** measure steady-state throughput on repetitive traffic streams. These figures reflect the engine's behavior when the same structure is seen repeatedly.
- **Your actual gain** depends on the repetitiveness of your traffic: the more your payloads share a stable JSON structure, the closer you get to the upper range.
- **Independent verification:** download the local binaries and measure on your own hardware.

## Historical run — 2026-07-04

## Test date

2026-07-04

## Server

OVH KS-A — Intel Xeon E-2274G @ 4.0GHz — Roubaix, France

## Methodology

Server-side parsing latency measured over 100,000 iterations on the same JSON payload. The client RTT is intentionally excluded.

- Endpoint: `POST https://api.nanofdo.com/api/v1/parse`
- Iterations: 100,000
- Warmup: 1,000 (default)
- License tier: Developer Edge (1M requests/month)
- Benchmarks are executed inside a `spawn_blocking` task on the server to keep the async runtime responsive.

## Payload

468 bytes:

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-07-04T12:00:00Z",
  "service": "payment-gateway",
  "region": "eu-west-roubaix",
  "user": {
    "id": 987654321,
    "role": "admin",
    "amount": 12345,
    "currency": "EUR",
    "status": "active",
    "metadata": {
      "source": "web",
      "ip": "203.0.113.42",
      "user_agent": "Mozilla/5.0",
      "session_id": "sess-abc123"
    },
    "tags": ["premium", "verified", "eu"]
  },
  "flags": ["fast", "verified", "encrypted"],
  "context": { "trace_id": "trace-xyz789", "span_id": "span-123" }
}
```

## Results

Average of 3 runs on the payload above.

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 628 ns  | 2194 ns    | 3.49x   |
| p95    | 635 ns  | 2233 ns    | 3.51x   |
| p99    | 647 ns  | 2254 ns    | 3.48x   |
| p999   | 898 ns  | 3694 ns    | 4.12x   |
| mean   | 632 ns  | 2204 ns    | 3.49x   |

## Raw data

| Run | NanoFDO p50 | p95 | p99 | p999 | mean | serde_json p50 | p95 | p99 | p999 | mean |
|-----|-------------|-----|-----|------|------|----------------|-----|-----|------|------|
| 1   | 628 ns      | 634 ns | 655 ns | 1042 ns | 633 ns | 2183 ns | 2222 ns | 2243 ns | 3721 ns | 2196 ns |
| 2   | 628 ns      | 633 ns | 645 ns | 669 ns | 631 ns | 2190 ns | 2228 ns | 2249 ns | 3663 ns | 2197 ns |
| 3   | 629 ns      | 638 ns | 641 ns | 982 ns | 632 ns | 2208 ns | 2249 ns | 2270 ns | 3699 ns | 2219 ns |

## Notes

- **p999 is still the most volatile metric.** On this larger payload it stays in the 4–5x range, much more stable than on the smaller payload where it ranged from 5–12x.
- **Server load matters.** Transient load on the OVH server can double absolute latencies. The speedup ratio stays in the 2.5–3.0x range on the current configuration.
- **Reproducible.** Anyone can reproduce these results by registering at `POST https://api.nanofdo.com/api/v1/register` and calling `POST https://api.nanofdo.com/api/v1/parse` with the generated license key.

## License

Data collected under the NanoFDO Developer Edge tier (1,000,000 requests/month). This benchmark run consumed 23 requests.
