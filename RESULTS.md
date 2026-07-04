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
- **Server load matters.** Transient load on the OVH server can double absolute latencies. The speedup ratio stays stable around 3.5x.
- **Reproducible.** Anyone can reproduce these results by registering at `POST https://api.nanofdo.com/api/v1/register` and calling `POST https://api.nanofdo.com/api/v1/parse` with the generated license key.

## License

Data collected under the NanoFDO Developer Edge tier (1,000,000 requests/month). This benchmark run consumed 23 requests.
