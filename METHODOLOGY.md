# Hosted Public Benchmark Methodology

**Version:** 1.1  
**Effective:** July 20, 2026

## Purpose

The hosted public benchmark measures server-side processing latency under a fixed, reproducible method. It is designed for verification and comparison, not for production processing or infrastructure stress testing.

## Fixed workload

Each hosted run uses:

- 100,000 measured iterations.
- 1,000 warmup iterations.
- One identical JSON payload for both measured implementations.
- One server-side execution environment.
- No client network time in the reported processing distributions.

Custom iteration and warmup values are rejected by the public endpoint to preserve comparability and control shared capacity.

## Reported values

The API reports:

- p50, p95, p99, and p999 latency.
- Mean, minimum, maximum, and standard deviation.
- The number of measured iterations.
- Comparative ratios calculated from matching distributions.
- Payload size.
- A SHA-256 payload fingerprint.
- Measurement timestamp and server description.

The client stores the complete responses and an aggregate summary in the local `results.json` file.

## Payload fingerprint

The payload fingerprint is calculated from the exact payload bytes. Matching fingerprints demonstrate that two runs used identical payload content.

It is not a machine, browser, GitHub account, or user fingerprint. The hosted service does not persist the payload solely because a fingerprint is returned.

## Network measurement

Reported server-processing distributions exclude client round-trip time. A locally measured HTTP duration includes network transit and intermediary processing and must not be presented as the server-processing latency.

## Repetition

The default client performs five runs with a short pause between runs. Repetition is recommended because shared-system conditions can affect absolute latency.

Publications should report:

- Repository commit or release.
- Measurement date and time.
- Methodology version.
- Payload fingerprint and size.
- Number of runs.
- p99 alongside other reported percentiles.
- Any errors, retries, exclusions, or capacity rejections.

Runs must not be selectively removed solely because their results are unfavourable. Any exclusion requires a documented technical reason.

## Hosted limits

The standard hosted allowance is:

- 5 run attempts per 15 minutes per key.
- 10 runs per day per key.
- 50 runs per calendar month per key.
- 1 concurrent run per key.
- 30 seconds maximum execution time.
- 500 atomically reserved runs per day across all public keys.
- 2 concurrent runs across the hosted service.

Capacity rejections should be retried only after the returned delay.

## Interpretation

Results apply to the documented payload, method, date, and server environment. They do not guarantee identical performance for every payload, workload, deployment, or production environment.

The p99 distribution is the primary tail-latency reference. Means may be included for completeness but must not replace percentile reporting.

## Intensive or local research

Researchers requiring intensive experiments must request a separate testing arrangement before testing or use an approved local option so their own infrastructure bears the compute load. Public-key limits remain applicable unless a written arrangement states otherwise.

See [Terms of Use](TERMS.md), [Acceptable Use](ACCEPTABLE_USE.md), and [Privacy](PRIVACY.md).
