# nanofdo-public-benchmarks

Public, reproducible parsing benchmarks for NanoFDO.

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

## Latest results

See [RESULTS.md](RESULTS.md).

## Methodology

Server-side parsing latency measured over 100,000 iterations on the same JSON payload. The client RTT is intentionally excluded.

Server: OVH KS-A — Intel Xeon E-2274G @ 4.0GHz — Roubaix, France.

## License

MIT
