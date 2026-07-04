# NanoFDO Public Benchmark Results

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

182 bytes:

```json
{
  "request_id": "uuid-1234",
  "timestamp": "2026-07-04T12:00:00Z",
  "user": {
    "id": 12345,
    "role": "admin",
    "amount": 123,
    "metadata": { "source": "web", "ip": "127.0.0.1" }
  },
  "flags": ["fast", "verified"]
}
```

## Results

Average of 7 stable runs (out of 11 total runs). Runs executed under transient server load are excluded from the average but listed in the raw data section.

| Metric | NanoFDO | serde_json | speedup |
|--------|---------|------------|---------|
| p50    | 330 ns  | 970 ns     | 2.94x   |
| p95    | 334 ns  | 992 ns     | 2.97x   |
| p99    | 346 ns  | 1006 ns    | 2.91x   |
| p999   | 360 ns  | 2425 ns    | 6.74x   |
| mean   | 334 ns  | 975 ns     | 2.92x   |

## Raw data — stable runs

| Run | NanoFDO p50 | p95 | p99 | mean | serde_json p50 | p95 | p99 | mean |
|-----|-------------|-----|-----|------|----------------|-----|-----|------|
| 1   | 333 ns      | 337 ns | 343 ns | 335 ns | 968 ns | 988 ns | 1001 ns | 977 ns |
| 2   | 332 ns      | 337 ns | 342 ns | 335 ns | 967 ns | 988 ns | 1000 ns | 972 ns |
| 3   | 328 ns      | 332 ns | 338 ns | 331 ns | 969 ns | 993 ns | 1004 ns | 975 ns |
| 4   | 327 ns      | 330 ns | 337 ns | 330 ns | 966 ns | 990 ns | 1002 ns | 972 ns |
| 5   | 332 ns      | 337 ns | 394 ns | 338 ns | 988 ns | 1046 ns | 1118 ns | 1003 ns |
| 6   | 329 ns      | 333 ns | 339 ns | 333 ns | 964 ns | 986 ns | 1000 ns | 972 ns |
| 7   | 329 ns      | 333 ns | 339 ns | 333 ns | 964 ns | 986 ns | 1000 ns | 972 ns |

## Raw data — runs under server load

These runs were executed while the server was handling other activity. Absolute latencies doubled, but the relative speedup remained consistent.

| Run | NanoFDO p50 | p95 | p99 | mean | serde_json p50 | p95 | p99 | mean |
|-----|-------------|-----|-----|------|----------------|-----|-----|------|
| A   | 632 ns      | 752 ns | 827 ns | 630 ns | 1909 ns | 2194 ns | 2687 ns | 1912 ns |
| B   | 687 ns      | 784 ns | 886 ns | 697 ns | 2109 ns | 2365 ns | 2666 ns | 2099 ns |
| C   | 606 ns      | 725 ns | 776 ns | 608 ns | 1792 ns | 2235 ns | 2851 ns | 1835 ns |
| D   | 610 ns      | 708 ns | 751 ns | 612 ns | 1904 ns | 3028 ns | 3293 ns | 2034 ns |

## Notes

- **p999 is volatile.** It ranges from ~5x to ~12x depending on rare system interruptions during the 100,000-iteration run. Use p50/p95/p99 as the primary metrics.
- **Server load matters.** Transient load on the OVH server can double absolute latencies. The speedup ratio stays stable around 2.9–3.0x.
- **Reproducible.** Anyone can reproduce these results by registering at `POST https://api.nanofdo.com/api/v1/register` and calling `POST https://api.nanofdo.com/api/v1/parse` with the generated license key.

## License

Data collected under the NanoFDO Developer Edge tier (1,000,000 requests/month). This benchmark run consumed 20 requests.
