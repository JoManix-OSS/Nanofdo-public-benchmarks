# Public Benchmark Acceptable Use Policy

**Last updated:** July 18, 2026
**Effective:** July 18, 2026

## Allowed uses

The hosted public benchmark may be used to:

- Reproduce the published benchmark under the documented methodology.
- Perform occasional technical evaluation before adoption.
- Compare results across documented methodology versions.
- Conduct academic, journalistic, engineering, or security review using synthetic payloads.
- Publish accurate results with methodology, date, payload fingerprint, run count, and limitations.

## Standard limits

Each public benchmark key is limited to:

- 5 run attempts per 15-minute window.
- 10 completed or reserved runs per day.
- 50 completed or reserved runs per calendar month.
- 1 concurrent run.
- The fixed public methodology of 100,000 measured iterations and 1,000 warmup iterations.
- A maximum execution time of 30 seconds per hosted run.

The public hosted service is limited to 500 completed or reserved runs per day across all public keys and 2 concurrent runs. A temporary capacity rejection does not authorize retry flooding or quota circumvention.

Registration is limited to 3 attempts per source address per day. Additional network-level protections may apply.

## Prohibited uses

You must not:

- Use the endpoint for production processing or as a free hosted processing service.
- Run stress tests, denial-of-service tests, sustained load tests, or uncontrolled automation.
- Circumvent quotas, rate limits, concurrency limits, suspensions, or scope restrictions.
- Create multiple registrations, aliases, or identities to aggregate free capacity.
- Share, publish, sell, lease, or transfer a benchmark key.
- Submit real personal, confidential, regulated, secret, or production data.
- Probe unrelated endpoints or attempt unauthorized access.
- Misrepresent, selectively alter, or fabricate benchmark results.
- Use the service in violation of law, third-party rights, or GitHub's applicable terms.

## Responsible testing

Security research beyond ordinary benchmark reproduction requires prior written authorization. The absence of a technical block does not constitute authorization.

Report suspected vulnerabilities privately to `contact@buro66.com`. Do not include active keys, payloads containing sensitive data, or exploit details in a public GitHub issue.

## Enforcement

NanoFDO may rate-limit, reject, suspend, or revoke access when this policy is violated or when activity creates a security, capacity, legal, or operational risk.

Signals are reviewed in context. Shared academic or corporate networks are not treated as abuse solely because multiple legitimate users have the same public source address.

Questions or requests for a separate research testing arrangement may be sent to `contact@buro66.com` before intensive testing begins.
